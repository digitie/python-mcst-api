from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from mcst import (  # noqa: E402
    CultureOpenApiClient,
    DataGoFileApiClient,
    DatasetKind,
    get_api_catalog,
    jsonable,
    save_fixture,
)
from mcst.debug import DebugRun, default_assertion  # noqa: E402


def main() -> None:
    st.set_page_config(page_title="MCST API Debug", layout="wide")
    st.title("MCST API Debug")

    with st.sidebar:
        st.header("Run")
        surface = st.selectbox("Function group", ["KCISA OpenAPI", "ODCloud File API"])
        timeout = st.number_input("Timeout seconds", min_value=1.0, max_value=60.0, value=10.0)

    if surface == "KCISA OpenAPI":
        _render_culture(timeout=float(timeout))
    else:
        _render_data_go(timeout=float(timeout))


def _render_culture(*, timeout: float) -> None:
    datasets = _catalog_options(DatasetKind.KCISA_OPEN_API)
    with st.sidebar:
        dataset = _select_dataset(datasets)
        dataset_slug = str(dataset["slug"])
        service_key = _service_key_input(dataset)
        keyword = st.text_input("Keyword")
        page_no = st.number_input("Page", min_value=1, value=1, step=1)
        num_of_rows = st.number_input("Rows", min_value=1, max_value=1000, value=10, step=1)
        params = _json_params()
        run_clicked = st.button("Run", type="primary")

    if run_clicked:
        client = CultureOpenApiClient(
            service_keys={dataset_slug: service_key} if service_key else None,
            timeout=timeout,
        )
        st.session_state["debug_run"] = client.debug_request(
            dataset_slug,
            keyword=keyword or None,
            page_no=int(page_no),
            num_of_rows=int(num_of_rows),
            params=params,
        )
    _render_debug_run()


def _render_data_go(*, timeout: float) -> None:
    datasets = _catalog_options(DatasetKind.DATA_GO_FILE_API)
    with st.sidebar:
        dataset = _select_dataset(datasets)
        dataset_slug = str(dataset["slug"])
        service_key = _service_key_input(dataset)
        page_no = st.number_input("Page", min_value=1, value=1, step=1)
        per_page = st.number_input("Rows", min_value=1, max_value=1000, value=10, step=1)
        params = _json_params()
        run_clicked = st.button("Run", type="primary")

    if run_clicked:
        client = DataGoFileApiClient(
            service_keys={dataset_slug: service_key} if service_key else None,
            timeout=timeout,
        )
        st.session_state["debug_run"] = client.debug_request(
            dataset_slug,
            page_no=int(page_no),
            per_page=int(per_page),
            params=params,
        )
    _render_debug_run()


def _json_params() -> dict[str, Any]:
    raw = st.text_area("Extra params JSON", value="{}", height=90)
    try:
        parsed = json.loads(raw or "{}")
    except json.JSONDecodeError as exc:
        st.error(f"Invalid params JSON: {exc}")
        return {}
    if not isinstance(parsed, dict):
        st.error("Extra params JSON must be an object.")
        return {}
    return parsed


def _clean_service_key(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip().strip('"').strip("'").strip()
    return cleaned or None


def _catalog_options(kind: DatasetKind) -> tuple[dict[str, Any], ...]:
    return get_api_catalog(kind=kind)


def _select_dataset(datasets: tuple[dict[str, Any], ...]) -> dict[str, Any]:
    labels = {str(item["label"]): item for item in datasets}
    selected_label = st.selectbox("Dataset", list(labels))
    dataset = labels[selected_label]
    st.caption(f"slug: `{dataset['slug']}`")
    return dataset


def _service_key_input(dataset: dict[str, Any]) -> str | None:
    dataset_slug = str(dataset["slug"])
    service_key_url = str(dataset.get("detail_url") or "")
    if service_key_url:
        st.link_button("서비스키 발급/활용신청", service_key_url, use_container_width=True)
    raw = st.text_input(
        "Service key for selected API",
        type="password",
        key=f"service_key:{dataset_slug}",
    )
    cleaned = _clean_service_key(raw)
    if raw and cleaned != raw:
        st.caption("앞뒤 공백과 감싸는 따옴표는 요청 전에 자동 제거됩니다.")
    return cleaned


def _render_debug_run() -> None:
    debug_run = st.session_state.get("debug_run")
    if not isinstance(debug_run, DebugRun):
        st.info("왼쪽에서 데이터셋과 입력값을 고른 뒤 Run을 누르세요.")
        return

    raw_tab, parsed_tab, processed_tab, errors_tab, trace_tab, fixture_tab = st.tabs(
        [
            "Raw Response",
            "Pydantic Model",
            "Processed Result",
            "Validation Errors",
            "Debug Trace",
            "Fixture",
        ]
    )

    with raw_tab:
        _render_result_or_error(debug_run, debug_run.response, "Raw response")

    with parsed_tab:
        _render_result_or_error(debug_run, debug_run.parsed, "Pydantic model")

    with processed_tab:
        _render_result_or_error(debug_run, debug_run.processed, "Processed result")

    with errors_tab:
        _render_error(debug_run)

    with trace_tab:
        catalog_entry = _catalog_entry_for_run(debug_run)
        if catalog_entry:
            st.subheader("Catalog entry")
            _render_catalog_entry(catalog_entry)
        st.subheader("Trace")
        for index, item in enumerate(debug_run.trace, start=1):
            st.write(f"{index}. {item}")

    with fixture_tab:
        _render_fixture_form(debug_run)


def _render_json_and_table(value: Any) -> None:
    data = jsonable(value)
    st.json(data)
    rows = data.get("items") if isinstance(data, dict) else None
    if isinstance(rows, list) and rows:
        st.dataframe(pd.json_normalize(rows, sep="."), use_container_width=True)


def _render_result_or_error(debug_run: DebugRun, value: Any, label: str) -> None:
    if debug_run.error and value in (None, {}, []):
        st.warning(f"{label}는 실행 실패로 생성되지 않았습니다. Validation Errors 탭을 확인하세요.")
        return
    _render_json_and_table(value)


def _render_error(debug_run: DebugRun) -> None:
    if not debug_run.error:
        st.success("오류가 없습니다.")
        return

    st.error(debug_run.error["message"])
    if debug_run.error.get("failure_kind") == "network":
        st.info(
            "상위 API 호스트에 도달하기 전 네트워크 계층에서 실패했습니다. "
            "DNS 해석 실패라면 서비스키 검증까지 진행되지 않은 상태입니다. "
            "Service key 입력값의 앞뒤 공백은 자동으로 제거됩니다."
        )
    st.json(debug_run.error)


def _catalog_entry_for_run(debug_run: DebugRun) -> dict[str, Any] | None:
    dataset = debug_run.input.get("dataset")
    if not isinstance(dataset, str):
        return None
    for item in get_api_catalog(include_links=True):
        if item["slug"] == dataset:
            return item
    return None


def _render_catalog_entry(entry: dict[str, Any]) -> None:
    st.markdown(f"**{entry['title']}**")
    rows = [
        {"항목": "slug", "값": entry["slug"]},
        {"항목": "provider", "값": entry["provider"]},
        {"항목": "kind", "값": entry["kind"]},
        {"항목": "source", "값": entry["source"]},
        {"항목": "endpoint_url", "값": entry.get("endpoint_url") or ""},
        {"항목": "file_url", "값": entry.get("file_url") or ""},
        {"항목": "detail_url", "값": entry["detail_url"]},
        {"항목": "tags", "값": ", ".join(entry.get("tags") or [])},
    ]
    st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
    with st.expander("Catalog JSON"):
        st.json(entry)


def _render_fixture_form(debug_run: DebugRun) -> None:
    if debug_run.error:
        st.warning("오류가 있는 실행 결과는 fixture로 저장하지 않는 편이 안전합니다.")

    case_name = st.text_input("Case name")
    description = st.text_area("Description")
    assertion_mode = st.selectbox(
        "Assertion mode",
        ["snapshot", "schema_only", "required_fields", "count"],
    )
    exclude_fields_raw = st.text_input("Exclude fields", value="fetched_at, request_id, updated_at")
    required_fields_raw = st.text_input("Required fields", value="")
    overwrite = st.checkbox("Overwrite existing fixture", value=False)

    assertion = default_assertion()
    assertion["mode"] = assertion_mode
    assertion["exclude_fields"] = [
        item.strip() for item in exclude_fields_raw.split(",") if item.strip()
    ]
    assertion["required_fields"] = [
        item.strip() for item in required_fields_raw.split(",") if item.strip()
    ]

    st.caption("미리보기")
    st.json(
        {
            "function": debug_run.function,
            "input": jsonable(debug_run.input),
            "assertion": assertion,
        }
    )

    if st.button("Save as fixture"):
        if not case_name.strip():
            st.error("Case name을 입력하세요.")
            return
        try:
            path = save_fixture(
                debug_run,
                base_dir=PROJECT_ROOT / "tests" / "fixtures",
                case_name=case_name,
                description=description,
                assertion=assertion,
                overwrite=overwrite,
            )
        except FileExistsError as exc:
            st.error(str(exc))
        except ValueError as exc:
            st.error(str(exc))
        else:
            st.success(f"Saved: {path}")


if __name__ == "__main__":
    main()
