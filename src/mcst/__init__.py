"""선별된 문화체육관광부 공개 데이터셋과 API용 Python 클라이언트입니다."""

from __future__ import annotations

from .catalog import (
    ALL_DATASETS,
    CULTURE_OPEN_APIS,
    FILE_DATASETS,
    CatalogEntry,
    DatasetKind,
    SourcePortal,
    catalog_entry_to_dict,
    dataset_label,
    get_api_catalog,
    get_dataset,
    iter_api_catalog,
)
from .client import McstClient
from .culture import CultureOpenApiClient
from .data_go import DataGoFileApiClient
from .debug import DebugRun, jsonable, redact_sensitive, save_fixture
from .exceptions import (
    McstAuthError,
    McstError,
    McstNetworkError,
    McstNoDataError,
    McstParseError,
    McstRequestError,
    McstServerError,
)
from .file_data import FileDataClient
from .models import CultureRecord, Page, RawRecord
from .replay import replay_case

__all__ = [
    "ALL_DATASETS",
    "CULTURE_OPEN_APIS",
    "FILE_DATASETS",
    "CatalogEntry",
    "CultureOpenApiClient",
    "CultureRecord",
    "DataGoFileApiClient",
    "DebugRun",
    "DatasetKind",
    "FileDataClient",
    "McstAuthError",
    "McstClient",
    "McstError",
    "McstNetworkError",
    "McstNoDataError",
    "McstParseError",
    "McstRequestError",
    "McstServerError",
    "Page",
    "RawRecord",
    "SourcePortal",
    "catalog_entry_to_dict",
    "dataset_label",
    "get_api_catalog",
    "get_dataset",
    "iter_api_catalog",
    "jsonable",
    "redact_sensitive",
    "replay_case",
    "save_fixture",
]
