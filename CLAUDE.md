# within-reach

## What this is

`within-reach` is the small library for what surrounds a running Halo: MCC and doesn't belong in the Megalo tooling: **system
detection** (is Tesseract OCR on `PATH`; where are Steam, Halo: MCC, Reach and the gametype/map folders), **hot reload** (getting a
rebuilt game variant into a running game) and **screen capture / OCR** (reading what the game window shows). It is a sister
package of `in-reach` (library + CLI) and `in-reach-ide` (the IDE); the IDE imports it now (`within_reach.system_verify` is
"Verify System Settings"), and `in-reach` will. It must not depend on either of them -- which is why it carries its own small
`env_file.py` (`.env` reader/writer) and `vdf.py` (Steam config parser), copies of the ones in `in_reach.app`.

**Status:** system detection is real and moved here from `in_reach.app.system_verify` (the same API, so the IDE only changed an
import). `hot-reload` and `grab` are placeholders that exit 2 with "not implemented yet". The old prototypes (`../in-reach-v1 (dis)`, `../in-reach-v2 (dis)`) held earlier experiments; read them
for what was tried, and port deliberately, piece by piece -- don't copy wholesale.

## Development

- Install: `pip install -e ".[dev]"`; tests: `python -m pytest tests -q` (Windows).
- New behaviour needs tests (`.claude/rules/tests-required.md`); never commit unless asked (`.claude/rules/no-auto-commit.md`).
- Releases use the same GitHub flow as `in-reach`: `development` -> `release/vX.Y.Z` (Cut Release workflow) -> PR into `main`
  (tests, bump label, branch source enforced) -> tag, GitHub Release, sync back, PyPI (trusted publishing). The version
  lives in `pyproject.toml` and `src/within_reach/__init__.py`; the package is pure Python (one `py3-none-any` wheel + sdist).
- Keep this file current as features land (`.claude/rules/keep-claude-md-current.md`).

## This repo's actual scope right now

- `src/within_reach/system_verify.py` -- the headless model behind the IDE's "Verify System Settings": the thirteen `STEPS`
  (Tesseract on `PATH`, Steam, Halo MCC, Reach, the hot-reload folder, the standard/hopper variant and map folders, the Steam
  account, the personal gametype and map folders, in-reach's own maps folder), each keyed by the `.env` key it fills in;
  `VerifyRun.check(step)` resolves one step without writing (`Outcome.FOUND` / `CHOICE` / `MISSING`), `accept(step, value)`
  writes the answer plus anything derived (accepting the personal gametype folder *creates* Halo's matching maps folder --
  a real side effect on the machine), `verified_keys`/`clear_entries` read and blank the keys. Nothing here prompts: whatever
  drives it (the IDE's `verify_dialog`) owns the asking.
- `src/within_reach/env_file.py`, `vdf.py` -- what `system_verify` needs (a `.env` reader/writer; a Steam VDF reader).
- `src/within_reach/cli.py` -- the `within-reach` click entry point: `detect [--format json]` runs the whole checklist against
  this machine in a scratch `.env` (so it changes nothing of yours, and deliberately never calls `accept`) and exits 1 if a
  step found nothing; `hot-reload` and `grab` are placeholders.
- `tests/` -- the detection tests (moved with it), `detect`, the CLI and release-gate (`.github/scripts/check_dist.py`) tests.
