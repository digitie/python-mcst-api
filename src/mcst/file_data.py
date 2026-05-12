"""선별된 문체부 파일데이터 다운로드 클라이언트입니다."""

from __future__ import annotations

import csv
from collections.abc import Iterator
from pathlib import Path

from ._http import HttpClient, SessionLike
from .catalog import ALL_DATASETS, CatalogEntry, DatasetKind, get_dataset
from .exceptions import McstRequestError


class FileDataClient:
    """선별된 파일데이터를 다운로드하고 읽습니다."""

    def __init__(
        self,
        *,
        timeout: float = 20.0,
        retries: int = 3,
        session: SessionLike | None = None,
    ) -> None:
        self._http = HttpClient(timeout=timeout, retries=retries, session=session)

    def datasets(self) -> tuple[CatalogEntry, ...]:
        """다운로드 또는 연결 URL이 있는 항목을 반환합니다."""

        return tuple(entry for entry in ALL_DATASETS.values() if entry.file_url)

    def download(self, dataset: str | CatalogEntry) -> bytes:
        """선별된 파일데이터 또는 연결 원천 URL을 다운로드합니다."""

        entry = _resolve_download(dataset)
        if not entry.file_url:
            raise McstRequestError(f"{entry.slug} does not have a file URL")
        return self._http.get_bytes(entry.file_url)

    def save(
        self,
        dataset: str | CatalogEntry,
        path: str | Path,
        *,
        overwrite: bool = False,
    ) -> Path:
        """데이터셋을 `path`로 다운로드합니다."""

        target = Path(path)
        if target.exists() and not overwrite:
            raise FileExistsError(str(target))
        data = self.download(dataset)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        return target

    def read_csv(
        self,
        dataset: str | CatalogEntry,
        *,
        encoding: str | None = None,
    ) -> list[dict[str, str]]:
        """CSV 파일을 다운로드해 딕셔너리 목록으로 파싱합니다."""

        return list(self.iter_csv(dataset, encoding=encoding))

    def iter_csv(
        self,
        dataset: str | CatalogEntry,
        *,
        encoding: str | None = None,
    ) -> Iterator[dict[str, str]]:
        """다운로드한 CSV 파일의 행을 순회합니다."""

        entry = _resolve_download(dataset)
        if entry.kind == DatasetKind.LINK:
            raise McstRequestError(f"{entry.slug} is a link entry, not a direct CSV")
        raw = self.download(entry)
        text = _decode_csv_bytes(raw, encoding)
        reader = csv.DictReader(text.splitlines())
        for row in reader:
            yield dict(row)


def _resolve_download(dataset: str | CatalogEntry) -> CatalogEntry:
    if isinstance(dataset, CatalogEntry):
        return dataset
    return get_dataset(dataset)


def _decode_csv_bytes(data: bytes, encoding: str | None) -> str:
    encodings = (encoding,) if encoding else ("utf-8-sig", "utf-8", "cp949", "euc-kr")
    last_error: UnicodeDecodeError | None = None
    for candidate in encodings:
        if candidate is None:
            continue
        try:
            return data.decode(candidate)
        except UnicodeDecodeError as exc:
            last_error = exc
    if last_error is not None:
        raise last_error
    return data.decode()
