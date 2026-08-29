"""Streamlit 기반 MCST API 디버그 카탈로그 뷰어."""
# ruff: noqa: E402,I001

from __future__ import annotations

from dataclasses import dataclass
import json
import os
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
for module_name, module in list(sys.modules.items()):
    if module_name != "mcst" and not module_name.startswith("mcst."):
        continue
    module_file = getattr(module, "__file__", None)
    if module_file is not None and not Path(module_file).resolve().is_relative_to(SRC):
        del sys.modules[module_name]

try:
    import pandas as pd
    import streamlit as st
except ModuleNotFoundError as exc:  # pragma: no cover - 선택 실행 도구
    raise SystemExit('Streamlit UI를 쓰려면 `pip install -e ".[debug-ui]"`를 실행하세요.') from exc

from mcst import (
    DatasetKind,
    DebugRun,
    McstClient,
    get_api_catalog,
    jsonable,
    save_fixture,
)
from mcst import culture as culture_module
from mcst import data_go as data_go_module
from mcst.debug import DEFAULT_EXCLUDE_FIELDS, default_assertion

# "Data source" 셀렉트박스에 노출할, debug_fetch()가 실제로 실행 가능한 카탈로그
# kind만 나열합니다. FILE_DOWNLOAD(csv 스크레이핑)와 LINK(외부 링크만 존재)는
# 호출 가능한 파라미터화된 API가 아니므로 이 디버그 UI 범위에서 제외합니다.
DATA_SOURCES: tuple[tuple[str, DatasetKind], ...] = (
    ("KCISA OpenAPI (api.kcisa.kr)", DatasetKind.KCISA_OPEN_API),
    ("data.go.kr ODCloud 자동변환 API (api.odcloud.kr)", DatasetKind.DATA_GO_FILE_API),
)


@dataclass(frozen=True)
class ParameterSpec:
    """디버그 UI에서 요청 파라미터 입력 폼을 만들기 위한 최소 명세."""

    name: str
    required: bool
    label: str
    placeholder: str = ""
    help: str = ""
    default: str = ""


def main() -> None:
    st.set_page_config(page_title="MCST API Debug", layout="wide")
    st.title("MCST API Debug")

    source_label = st.sidebar.selectbox("Data source", [label for label, _ in DATA_SOURCES])
    kind = dict(DATA_SOURCES)[source_label]

    catalog_rows = get_api_catalog(kind=kind)
    if not catalog_rows:
        st.sidebar.error("이 data source에는 등록된 API가 없습니다.")
        st.stop()
    labels = [row["label"] for row in catalog_rows]
    selected_label = st.sidebar.selectbox("API", labels)
    entry = catalog_rows[labels.index(selected_label)]

    what_line, returns_line = _api_description_lines(entry, kind)
    st.sidebar.caption(what_line)
    st.sidebar.caption(returns_line)

    env_names = _env_names_for_kind(kind)
    env_match = _first_process_env(env_names)

    st.sidebar.subheader("Environment")
    env_mode = st.sidebar.radio(
        "Service key source",
        ["env", "manual"],
        index=0 if env_match else 1,
        horizontal=True,
        key=f"env_mode:{kind.value}",
    )
    if env_match:
        st.sidebar.caption(f"env 사용 시 `{env_match[0]}` 값을 사용합니다.")
    else:
        st.sidebar.caption(f"확인한 env var: {', '.join(env_names)} (현재 프로세스에 없음)")

    st.sidebar.subheader("Auth")
    if env_mode == "env" and env_match:
        effective_api_key = env_match[1]
        st.sidebar.caption("serviceKey: env 값을 사용합니다.")
    else:
        effective_api_key = st.sidebar.text_input(
            "serviceKey",
            value="",
            type="password",
            placeholder="직접 입력",
            help=(
                "실제 쿼리 파라미터명은 `serviceKey`입니다. "
                f"사용 가능한 env: {', '.join(env_names)}"
            ),
            key=f"service_key:{kind.value}:{entry['slug']}",
        )
    _service_key_links(entry)

    timeout = st.sidebar.number_input(
        "Timeout",
        min_value=1.0,
        max_value=60.0,
        value=10.0,
        step=1.0,
        help="API 요청 timeout seconds입니다.",
    )
    fixture_base_dir = _fixture_base_dir_sidebar()

    tabs = st.tabs(
        [
            "Raw Response",
            "Pydantic Model",
            "Processed Result",
            "Validation Errors",
            "Debug Trace",
            "Fixture / Testcase",
        ]
    )

    with tabs[0]:
        _raw_response_tab(kind, entry, effective_api_key, timeout=float(timeout))
    with tabs[1]:
        _pydantic_model_tab(kind, entry)
    with tabs[2]:
        _processed_result_tab(kind, entry)
    with tabs[3]:
        _validation_errors_tab(kind, entry)
    with tabs[4]:
        _debug_trace_tab(kind, entry, env_names, catalog_rows)
    with tabs[5]:
        _fixture_tab(fixture_base_dir, kind, entry)


def _raw_response_tab(
    kind: DatasetKind, entry: dict[str, Any], api_key: str, *, timeout: float
) -> None:
    st.subheader(entry["title"])
    st.caption(f"slug={entry['slug']} · kind={kind.value} · provider={entry['provider']}")

    key_prefix = f"{kind.value}:{entry['slug']}"
    try:
        submitted, params, keyword, page_no, num_of_rows, missing = _request_form(
            entry, key_prefix
        )
    except ValueError as exc:
        st.error(str(exc))
        return

    preview: dict[str, Any] = {**params, "pageNo": page_no, "numOfRows": num_of_rows}
    if keyword:
        preview["keyword"] = keyword
    st.subheader("Request params preview")
    st.json(preview)

    if not submitted:
        return
    if missing:
        st.error("필수 파라미터를 입력하세요: " + ", ".join(missing))
        return
    if not api_key:
        st.error("serviceKey가 비어 있습니다. Auth 섹션에서 입력하거나 env를 사용하세요.")
        return

    client = McstClient(service_keys={entry["slug"]: api_key}, timeout=timeout, retries=0)
    try:
        run = client.debug_fetch(
            entry["slug"],
            params=params,
            keyword=keyword,
            page_no=page_no,
            num_of_rows=num_of_rows,
            timeout=timeout,
        )
    finally:
        client.close()

    _store_run(kind, entry, run)
    if run.error:
        st.error(run.error.get("message", "요청이 실패했습니다."))
    st.json(jsonable(run.response))


def _request_form(
    entry: dict[str, Any], key_prefix: str
) -> tuple[bool, dict[str, Any], str | None, int, int, list[str]]:
    required_specs, optional_specs = _parameter_specs(entry)

    with st.form(f"request-form:{key_prefix}"):
        st.subheader("Required parameters")
        if required_specs:
            required_values = _render_param_grid(required_specs, key_prefix=key_prefix)
        else:
            st.caption("이 API에는 카탈로그에 등록된 필수 파라미터가 없습니다.")
            required_values = {}

        st.subheader("Optional parameters")
        if optional_specs:
            optional_values = _render_param_grid(optional_specs, key_prefix=key_prefix)
        else:
            st.caption("이 API에는 카탈로그에 등록된 선택 파라미터가 없습니다.")
            optional_values = {}

        page_no, num_of_rows = _render_common_options(key_prefix)

        extra_text = st.text_area(
            "Extra params JSON",
            value="{}",
            height=110,
            help=(
                "카탈로그 메타데이터에 없는 추가 쿼리 파라미터를 JSON object로 넣습니다"
                "(예: ODCloud `cond[컬럼::eq]` 필터)."
            ),
            key=f"{key_prefix}:extra",
        )
        submitted = st.form_submit_button("Run selected API")

    values = {**required_values, **optional_values}
    missing = [spec.name for spec in required_specs if not str(values.get(spec.name, "")).strip()]
    keyword = values.pop("keyword", "").strip() or None
    extra = _parse_extra_params(extra_text)
    params = {**values, **extra}
    params = {key: value for key, value in params.items() if str(value).strip()}
    return submitted, params, keyword, int(page_no), int(num_of_rows), missing


def _parameter_specs(
    entry: dict[str, Any],
) -> tuple[tuple[ParameterSpec, ...], tuple[ParameterSpec, ...]]:
    required = tuple(
        ParameterSpec(
            name=name,
            required=True,
            label=name,
            help="카탈로그에 등록된 필수 요청 파라미터입니다.",
        )
        for name in entry["required_params"]
    )
    optional = tuple(
        ParameterSpec(
            name=name,
            required=False,
            label=name,
            help="카탈로그에 등록된 선택 요청 파라미터입니다.",
        )
        for name in entry["optional_params"]
    )
    return required, optional


def _render_param_grid(specs: tuple[ParameterSpec, ...], *, key_prefix: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for index in range(0, len(specs), 2):
        columns = st.columns(2)
        for column, spec in zip(columns, specs[index : index + 2], strict=False):
            with column:
                values[spec.name] = st.text_input(
                    spec.label,
                    value=spec.default,
                    placeholder=spec.placeholder,
                    help=spec.help or None,
                    key=f"{key_prefix}:param:{spec.name}",
                )
    return values


def _render_common_options(key_prefix: str) -> tuple[int, int]:
    col1, col2 = st.columns(2)
    with col1:
        page_no = st.number_input(
            "pageNo",
            min_value=1,
            value=1,
            step=1,
            help="페이지 번호입니다.",
            key=f"{key_prefix}:pageNo",
        )
    with col2:
        num_of_rows = st.number_input(
            "numOfRows",
            min_value=1,
            max_value=1000,
            value=10,
            step=1,
            help=(
                "페이지당 row 수입니다"
                "(ODCloud data source에서는 내부적으로 perPage로 매핑됩니다)."
            ),
            key=f"{key_prefix}:numOfRows",
        )
    return int(page_no), int(num_of_rows)


def _parse_extra_params(text: str) -> dict[str, Any]:
    try:
        payload = json.loads(text or "{}")
    except json.JSONDecodeError as exc:
        raise ValueError(f"Extra params JSON is invalid: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError("Extra params JSON must be an object")
    reserved = {"serviceKey", "ServiceKey", "pageNo", "numOfRows", "page", "perPage", "keyword"}
    return {key: value for key, value in payload.items() if key not in reserved}


def _pydantic_model_tab(kind: DatasetKind, entry: dict[str, Any]) -> None:
    run = _current_run(kind, entry)
    if run is None:
        st.info("Raw Response 탭에서 선택한 API를 실행하면 여기에서 Pydantic 모델을 확인합니다.")
        return
    if run.error:
        st.warning("실행 중 오류가 있습니다. Validation Errors 탭을 확인하세요.")
    st.json(jsonable(run.parsed))


def _processed_result_tab(kind: DatasetKind, entry: dict[str, Any]) -> None:
    run = _current_run(kind, entry)
    if run is None:
        st.info("Raw Response 탭에서 API를 실행하면 처리된 결과를 표시합니다.")
        return

    data = jsonable(run.processed)
    items = data.get("items") if isinstance(data, dict) else None
    if isinstance(items, list) and items:
        st.caption(
            f"page_no={data.get('page_no')} · num_of_rows={data.get('num_of_rows')} "
            f"· total_count={data.get('total_count')} · endpoint={data.get('endpoint')}"
        )
        st.dataframe(pd.json_normalize(items, sep="."), width="stretch", hide_index=True)
    else:
        st.json(data)


def _validation_errors_tab(kind: DatasetKind, entry: dict[str, Any]) -> None:
    run = _current_run(kind, entry)
    if run is None:
        st.info("아직 실행된 API가 없습니다.")
        return
    if not run.error:
        st.success("현재 실행 결과에서 validation error 또는 exception이 없습니다.")
        return
    st.error(run.error.get("message", "알 수 없는 오류입니다."))
    st.json(run.error)


def _debug_trace_tab(
    kind: DatasetKind,
    entry: dict[str, Any],
    env_names: tuple[str, ...],
    catalog_rows: tuple[dict[str, Any], ...],
) -> None:
    run = _current_run(kind, entry)

    st.subheader("Catalog")
    st.dataframe(catalog_rows, width="stretch", hide_index=True)

    st.subheader("Selected API")
    st.json(entry)
    st.link_button("서비스키 발급/활용신청", entry["detail_url"])
    st.caption(f"credential env: {', '.join(env_names)}")

    if run is not None:
        st.subheader("Trace")
        for index, item in enumerate(run.trace, start=1):
            st.write(f"{index}. {item}")

        st.subheader("Request")
        st.json(jsonable(run.request))

        st.subheader("Response")
        response = jsonable(run.response)
        if isinstance(response, dict):
            st.caption(
                f"status_code={response.get('status_code')} · "
                f"elapsed_ms={response.get('elapsed_ms')}"
            )
        st.json(response)


def _fixture_tab(fixture_base_dir: str, kind: DatasetKind, entry: dict[str, Any]) -> None:
    run = _current_run(kind, entry)
    if run is None:
        st.info("Raw Response 탭에서 API를 실행한 뒤 fixture를 저장할 수 있습니다.")
        st.caption("Fixture base dir")
        st.code(fixture_base_dir, language=None)
        return

    key_prefix = f"fixture:{kind.value}:{entry['slug']}"
    with st.expander("Save as fixture", expanded=True):
        case_name = st.text_input(
            "Case name", value=f"{entry['slug']}_normal", key=f"{key_prefix}:case"
        )
        description = st.text_area(
            "Description", value=f"{entry['title']} 정상 케이스", key=f"{key_prefix}:desc"
        )
        assertion_mode = st.selectbox(
            "Assertion mode",
            ["snapshot", "schema_only", "required_fields", "count"],
            key=f"{key_prefix}:mode",
        )
        exclude_fields_raw = st.text_input(
            "Exclude fields",
            value=", ".join(DEFAULT_EXCLUDE_FIELDS),
            key=f"{key_prefix}:exclude",
        )
        required_fields_raw = st.text_input(
            "Required fields", value="", key=f"{key_prefix}:required"
        )
        overwrite = st.checkbox(
            "Overwrite existing fixture", value=False, key=f"{key_prefix}:overwrite"
        )

        assertion = default_assertion()
        assertion["mode"] = assertion_mode
        assertion["exclude_fields"] = [
            value.strip() for value in exclude_fields_raw.split(",") if value.strip()
        ]
        assertion["required_fields"] = [
            value.strip() for value in required_fields_raw.split(",") if value.strip()
        ]

        st.subheader("Fixture preview")
        st.json(
            {
                "function": run.function,
                "input": jsonable(run.input),
                "assertion": assertion,
            }
        )

        if st.button("Save as fixture", key=f"{key_prefix}:save"):
            if not case_name.strip():
                st.error("Case name을 입력하세요.")
            else:
                try:
                    path = save_fixture(
                        run,
                        base_dir=fixture_base_dir,
                        case_name=case_name,
                        description=description,
                        assertion=assertion,
                        overwrite=overwrite,
                    )
                except (FileExistsError, ValueError) as exc:
                    st.error(str(exc))
                else:
                    st.success(f"Saved: {path}")


def _service_key_links(entry: dict[str, Any]) -> None:
    st.sidebar.caption("Service key links")
    st.sidebar.link_button(
        "서비스키 발급/활용신청", entry["detail_url"], use_container_width=True
    )
    spec_url = entry.get("spec_url")
    if spec_url and spec_url != entry["detail_url"]:
        st.sidebar.link_button("API 명세서", spec_url, use_container_width=True)


def _env_names_for_kind(kind: DatasetKind) -> tuple[str, ...]:
    if kind == DatasetKind.KCISA_OPEN_API:
        return culture_module.DEFAULT_ENV_NAMES
    return data_go_module.DEFAULT_ENV_NAMES


def _first_process_env(names: tuple[str, ...]) -> tuple[str, str] | None:
    for name in names:
        raw = os.getenv(name)
        if raw is None:
            continue
        cleaned = raw.strip().strip('"').strip("'").strip()
        if cleaned:
            return name, cleaned
    return None


def _fixture_base_dir_sidebar() -> str:
    st.sidebar.subheader("Fixtures")
    candidates = _fixture_dir_candidates()
    options = [str(path) for path in candidates]
    custom_label = "Custom..."
    selected = st.sidebar.selectbox("Fixture base dir", [*options, custom_label])
    if selected == custom_label:
        selected = st.sidebar.text_input(
            "Custom fixture base dir",
            value=str((ROOT / "tests" / "fixtures").resolve()),
        )
    st.sidebar.caption(selected)
    return selected


def _fixture_dir_candidates() -> list[Path]:
    preferred = [
        ROOT / "tests" / "fixtures",
        ROOT / "tests",
        ROOT / "examples",
        ROOT,
    ]
    candidates: list[Path] = []
    for path in preferred:
        resolved = path.resolve()
        if resolved not in candidates:
            candidates.append(resolved)
    return candidates


def _api_description_lines(entry: dict[str, Any], kind: DatasetKind) -> tuple[str, str]:
    if kind == DatasetKind.KCISA_OPEN_API:
        what = f"{entry['title']} — {entry['provider']} 제공 KCISA(culture.go.kr) OpenAPI입니다."
    else:
        what = f"{entry['title']} — {entry['provider']} 제공 data.go.kr ODCloud 자동변환 API입니다."
    tags = ", ".join(entry.get("tags") or []) or "없음"
    returns = f"반환: 페이지네이션된 레코드 목록(JSON). 태그: {tags}."
    return what, returns


def _selection_key(kind: DatasetKind, entry: dict[str, Any]) -> str:
    return f"{kind.value}:{entry['slug']}"


def _store_run(kind: DatasetKind, entry: dict[str, Any], run: DebugRun) -> None:
    st.session_state["last_run"] = {"selection_key": _selection_key(kind, entry), "run": run}


def _current_run(kind: DatasetKind, entry: dict[str, Any]) -> DebugRun | None:
    stored = st.session_state.get("last_run")
    if not isinstance(stored, dict):
        return None
    if stored.get("selection_key") != _selection_key(kind, entry):
        return None
    run = stored.get("run")
    return run if isinstance(run, DebugRun) else None


if __name__ == "__main__":
    main()
