# Deepagents Upgrade Assessment (2026-03-03)

## Executive Summary

As of **March 3, 2026**, this project is on:

- `deepagents-cli==0.0.21`
- `deepagents==0.4.1`

Latest releases on PyPI are:

- `deepagents-cli==0.0.25` (released **2026-02-20**)
- `deepagents==0.4.4` (released **2026-02-26**)

Recommendation: **upgrade to `deepagents-cli==0.0.25` first**, and accept its pinned dependency `deepagents==0.4.3` for stability. Do not force `deepagents==0.4.4` in the same step unless we intentionally break/override the CLI pin and validate thoroughly.

## 1. Current vs Latest Matrix

| Package | Local | Latest (PyPI) | Delta | Notes |
|---|---:|---:|---:|---|
| deepagents-cli | 0.0.21 | 0.0.25 | +4 patch versions | Includes dependency updates; one intermediate yanked release (0.0.24) |
| deepagents | 0.4.1 | 0.4.4 | +3 patch versions | One intermediate yanked release (0.4.2) |

## 2. Resolved Dependency Differences

### 2.1 deepagents-cli: 0.0.21 -> 0.0.25

Key `requires_dist` changes from PyPI metadata:

1. `deepagents==0.4.1` -> `deepagents==0.4.3`
2. `textual>=6.0.0,<8.0.0` -> `textual>=8.0.0,<9.0.0`
3. `langchain-openai>=1.1.7,<2.0.0` -> `>=1.1.8,<2.0.0`
4. Added optional provider dependency:
   - `langchain-openrouter>=0.0.1,<2.0.0` (extras)

Impact:

- The **Textual major range shift** is the most meaningful runtime compatibility change for CLI/TUI behavior.
- CLI now expects a newer deepagents line (`0.4.3`), so partial upgrades need care.

### 2.2 deepagents: 0.4.1 -> 0.4.4

Observed dependency delta from PyPI metadata:

1. `langchain-anthropic>=1.3.2,<2.0.0` -> `>=1.3.3,<2.0.0`

Impact:

- Small visible dependency bump, but functional changes can still exist in package internals.

## 3. Release Signal & Risk Notes

### 3.1 Yanked Releases

From PyPI release metadata:

- `deepagents-cli 0.0.24` was yanked with reason: **"pins incorrect SDK version"**
- `deepagents 0.4.2` was yanked with reason: **"Reverting migration to skill tool"**

Interpretation:

- Maintainers made rapid corrections around dependency pinning and skill-tool migration.
- This suggests we should prefer a conservative, pinned upgrade path and avoid custom pin overrides in the first step.

### 3.2 Compatibility Risk for This Repo

1. **CLI/TUI behavior risk (medium)** due to Textual range jump (`<8` -> `>=8,<9`).
2. **Agent framework behavior risk (low-medium)** due to deepagents patch changes.
3. **Provider integration risk (low)**; existing model routing should mostly remain compatible, but runtime checks are still required.

## 4. Upgrade Options

### Option A (Recommended): Stable aligned upgrade

- Target:
  - `deepagents-cli==0.0.25`
  - `deepagents==0.4.3` (as pinned by CLI)

Pros:

- Follows maintainer-tested dependency alignment.
- Minimizes resolver conflicts and hidden breakages.

Cons:

- Does not reach `deepagents==0.4.4` immediately.

### Option B: Force latest SDK now

- Target:
  - `deepagents-cli==0.0.25`
  - override `deepagents==0.4.4`

Pros:

- Fastest to latest SDK.

Cons:

- Conflicts with current CLI pin expectation (`==0.4.3`).
- Higher risk; requires explicit pin override strategy and extra regression effort.

### Option C: No upgrade now

Pros:

- Zero immediate change risk.

Cons:

- Misses fixes and compatibility updates from `0.0.22-0.0.25` and `0.4.2-0.4.4`.

## 5. Decision Checklist

Use this checklist before choosing:

1. Is short-term stability more important than being on absolute latest SDK?
2. Are we willing to spend extra effort validating Textual behavior after upgrade?
3. Do we want one-step safe upgrade first, then evaluate `deepagents 0.4.4` separately?

If answers are stability-first, pick **Option A**.

## 6. Proposed Rollout (if approved)

1. Update dependency target to `deepagents-cli==0.0.25`.
2. Re-lock dependencies (`uv lock` / `uv sync`) and verify resolved `deepagents==0.4.3`.
3. Run regression suite:
   - `uv run pytest`
   - `uv run ruff check .`
   - `uv run mypy clawdcut`
4. Manual smoke run for CLI entry flow (`clawdcut`) and basic agent interaction.
5. If all stable, optionally open a second pass to evaluate `deepagents==0.4.4`.

## 7. Evidence (Source of Truth)

### 7.1 Local versions

- `uv pip show deepagents-cli deepagents`
- `uv.lock` entries show:
  - `deepagents-cli==0.0.21`
  - `deepagents==0.4.1`

### 7.2 PyPI metadata snapshots

- `https://pypi.org/pypi/deepagents-cli/json`
- `https://pypi.org/pypi/deepagents/json`
- `https://pypi.org/pypi/deepagents-cli/0.0.21/json`
- `https://pypi.org/pypi/deepagents-cli/0.0.25/json`
- `https://pypi.org/pypi/deepagents/0.4.1/json`
- `https://pypi.org/pypi/deepagents/0.4.4/json`

### 7.3 Key extracted facts

- Latest versions: CLI `0.0.25`, SDK `0.4.4`
- CLI pin moved from `deepagents==0.4.1` to `deepagents==0.4.3`
- Yanked release reasons:
  - CLI `0.0.24`: `pins incorrect SDK version`
  - SDK `0.4.2`: `Reverting migration to skill tool`
