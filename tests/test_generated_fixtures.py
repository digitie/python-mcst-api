from __future__ import annotations

import json
from pathlib import Path

import pytest

from mcst.replay import replay_case
from tests.utils import assert_case

FIXTURE_DIR = Path(__file__).parent / "fixtures"


def all_fixture_files() -> list[Path]:
    return sorted(FIXTURE_DIR.glob("*/*.json"))


@pytest.mark.parametrize(
    "fixture_path",
    all_fixture_files(),
    ids=lambda path: f"{path.parent.name}/{path.stem}",
)
def test_generated_fixtures(fixture_path: Path) -> None:
    case = json.loads(fixture_path.read_text(encoding="utf-8"))

    actual = replay_case(case)
    expected = case["processed"]
    assertion = case.get("assertion", {"mode": "snapshot"})

    assert_case(actual, expected, assertion)
