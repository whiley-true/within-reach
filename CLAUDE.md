# within-reach

## What this is

`within-reach` is the small library for two things that don't belong in the Megalo tooling: **hot reload** (getting a rebuilt
game variant into a running Halo: MCC) and **screen capture / OCR** (reading what the game window shows). It is a sister
package of `in-reach` (library + CLI) and `in-reach-ide` (the IDE); those two will import it as a dependency. It must not
depend on either of them.

**Status: scaffold only.** `src/within_reach/cli.py` has `hot-reload` and `grab` commands that exit 2 with "not implemented
yet". Nothing else exists. The old prototypes (`../in-reach-v1 (dis)`, `../in-reach-v2 (dis)`) held earlier experiments; read them
for what was tried, and port deliberately, piece by piece -- don't copy wholesale.

## Development

- Install: `pip install -e ".[dev]"`; tests: `python -m pytest tests -q` (Windows).
- New behaviour needs tests (`.claude/rules/tests-required.md`); never commit unless asked (`.claude/rules/no-auto-commit.md`).
- Releases use the same GitHub flow as `in-reach`: `development` -> `release/vX.Y.Z` (Cut Release workflow) -> PR into `main`
  (tests, bump label, branch source enforced) -> tag, GitHub Release, sync back, PyPI (trusted publishing). The version
  lives in `pyproject.toml` and `src/within_reach/__init__.py`; the package is pure Python (one `py3-none-any` wheel + sdist).
- Keep this file current as features land (`.claude/rules/keep-claude-md-current.md`).

## This repo's actual scope right now

- `src/within_reach/cli.py` -- the `within-reach` click entry point (placeholder commands).
- `tests/` -- CLI and release-gate (`.github/scripts/check_dist.py`) tests.
