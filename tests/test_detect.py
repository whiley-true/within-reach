"""``within-reach detect`` and ``detect_all``: the IDE's verification checklist, run headlessly and without writing anything."""
import json
import os
from pathlib import Path

import pytest
from click.testing import CliRunner

from test_system_verify import _make_local_files, _make_reach_install, _make_steam_install
from within_reach import cli, system_verify
from within_reach.cli import detect_all, main


def _machine(tmp_path: Path) -> dict:
    """A fake machine: Steam with one account and Reach installed, an MCC local-files folder, and tesseract on PATH."""
    steam = _make_steam_install(tmp_path, ("1234", "Whiley"))
    _make_reach_install(steam)
    _make_local_files(tmp_path, "reachstr")
    return {"home": tmp_path, "steam_default": steam, "username": "whiley", "which": lambda name: "C:/tools/tesseract.exe"}


def _by_key(report: list[dict]) -> dict[str, dict]:
    return {row["key"]: row for row in report}


def test_every_step_is_reported_in_checklist_order(tmp_path: Path) -> None:
    report = detect_all(**_machine(tmp_path))

    assert [row["key"] for row in report] == [step.env_key for step in system_verify.STEPS]
    assert all(set(row) == {"key", "label", "outcome", "value", "detail", "choices"} for row in report)


def test_tesseract_and_the_folders_are_found_and_later_steps_derive_from_earlier_ones(tmp_path: Path) -> None:
    found = _by_key(detect_all(**_machine(tmp_path)))

    assert found[system_verify.TESSERACT_KEY]["outcome"] == "found" and "tesseract" in found[system_verify.TESSERACT_KEY]["value"]
    assert found[system_verify.STEAM_KEY]["outcome"] == "found"
    assert found[system_verify.REACH_KEY]["outcome"] == "found" and "haloreach" in found[system_verify.REACH_KEY]["value"]
    assert found[system_verify.STANDARD_VARIANTS_KEY]["value"].replace("\\", "/").endswith("haloreach/game_variants")


def test_a_machine_with_nothing_reports_missing_steps_with_where_it_looked(tmp_path: Path) -> None:
    found = _by_key(detect_all(which=lambda name: None, home=tmp_path, steam_default=tmp_path / "no-steam", username="x"))

    assert found[system_verify.TESSERACT_KEY]["outcome"] == "missing" and found[system_verify.TESSERACT_KEY]["detail"]
    assert found[system_verify.STEAM_KEY]["outcome"] == "missing"


def test_several_candidates_are_listed_and_left_to_the_user(tmp_path: Path) -> None:
    steam = _make_steam_install(tmp_path, ("1111", "One"), ("2222", "Two"))
    _make_reach_install(steam)
    _make_local_files(tmp_path, "reachstr")

    found = _by_key(detect_all(home=tmp_path, steam_default=steam, username="u", which=lambda n: "t"))

    account = found[system_verify.STEAM_ACCOUNT_KEY]
    assert account["outcome"] == "choice" and {c["value"] for c in account["choices"]} == {"1111", "2222"}


def test_detecting_never_touches_the_callers_files(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    home = tmp_path / "home"
    work = tmp_path / "work"
    work.mkdir()
    monkeypatch.chdir(work)
    machine = _machine(tmp_path)
    before = sorted(str(p) for p in tmp_path.rglob("*"))

    detect_all(**machine)

    assert sorted(str(p) for p in tmp_path.rglob("*")) == before and not (work / ".in-reach").exists() and not home.exists()


def test_the_scratch_folder_is_removed(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    import tempfile

    made = []
    real = tempfile.TemporaryDirectory

    def recording(*args, **kwargs):
        directory = real(*args, **kwargs)
        made.append(directory.name)
        return directory

    monkeypatch.setattr(cli.tempfile, "TemporaryDirectory", recording)

    detect_all(**_machine(tmp_path))

    assert made and not any(os.path.exists(d) for d in made)


# -- the command ------------------------------------------------------------------------------------------------------


def _report(outcomes: dict[str, str]) -> list[dict]:
    return [
        {"key": key, "label": key.title(), "outcome": outcome, "value": "v" if outcome == "found" else "", "detail": "looked here", "choices": []}
        for key, outcome in outcomes.items()
    ]


def test_detect_prints_a_line_per_step_and_exits_0_when_nothing_is_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(cli, "detect_all", lambda: _report({"A": "found", "B": "choice"}))

    result = CliRunner().invoke(main, ["detect"])

    assert result.exit_code == 0 and "ok A: v" in result.output and "?? B: looked here" in result.output


def test_detect_exits_1_when_a_step_found_nothing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(cli, "detect_all", lambda: _report({"A": "found", "B": "missing"}))

    result = CliRunner().invoke(main, ["detect"])

    assert result.exit_code == 1 and "-- B: looked here" in result.output


def test_detect_json_is_versioned(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(cli, "detect_all", lambda: _report({"A": "found"}))

    data = json.loads(CliRunner().invoke(main, ["detect", "--format", "json"]).output)

    assert data["schema"] == 1 and data["steps"][0]["key"] == "A"


def test_help_lists_detect() -> None:
    assert "detect" in CliRunner().invoke(main, ["--help"]).output
