# Plan: Week 5 Receipt Processor & Tests

## Files to Create
- `intent/receipts.md`, `spec.md`, `plan.md`
- `parser.py` & `checker.py`
- `test_parser.py`, `test_checker.py` (offline tests needing no key)
- `eval_receipts.py` (online eval against `expected.json`)
- `.claude/hooks/guard.py` & `.claude/settings.json`
- `CHECKS.md` & `README.md`

## Build Order
1. Commit pre-code artifacts (`intent/`, `spec.md`, `plan.md`).
2. Write unit tests (`test_parser.py`, `test_checker.py`) before implementation code.
3. Implement `parser.py` and `checker.py` to pass unit tests (Red-Green loop).
4. Implement `.claude/hooks/guard.py`.
5. Run eval suite and populate `CHECKS.md`.

## Proof & Evaluation Strategy
- Offline unit tests run without API keys. Online eval runs against `images/expected.json` and personal `my-receipts/` data.

---

# Week 6

Implements the "Week 6: image set" section of `spec.md` for `intent/image-set.md`.

## Files under `week06/`
| File | What it is |
|---|---|
| `critique.py` | Checker (plain code: `extract_json`, `check`, `text_matches`, `disagreements`) and the critic (billed). |
| `tests/test_checker.py` | No-key tests; written first and seen to fail. |
| `tests/conftest.py` | Lets the tests import `critique.py`. |
| `generate.py` | The generator: prompts.json → images + `manifest.json`. |
| `prompts.json` | Five mug prompts, one family, fixed seeds 6101–6105, 3–4 requirements each, expected text "MORNING". |
| `images/` | The five FLUX images and `manifest.json`. |
| `images-seed/` | One prompt regenerated with the same seed (the seed check). |
| `images-nb/` | The same prompt on the comparison model. |
| `critique.json`, `critique-mimo.json` | Both critics' output. |
| `CHECKS.md` | Every measured result, the critic-checked record, the linter, and the Review section. |

## Order of work
1. Checker: tests first, run red, write the checker, run green, `ruff check .`, commit.
2. Generator and critic, `prompts.json`.
3. Generate five images; look at them myself; critique with MiniMax; record. Seed check and comparison model. Commit.
4. Critique with MiMo; `--compare`; decide each disagreement by looking; one open-ended critique in my own
   terminal; three sentences on which check to keep. Commit.
5. The team repository: branch, image set and manifest, gate, PR, reviewer, findings comment, teammate approval.
   Review section in `CHECKS.md`; tag `week06-submitted`; push.

## Risks
- **The critic says a requirement is unmet and it is actually met** (or the reverse). *Which test notices:*
  no no-key test can, because only the image knows. The **second model** (`--compare`) flags it as a
  disagreement, and **I look**. The no-key test `test_disagreements_between_two_critics` proves the
  comparison reports it.
- **Cost of one eval run, and running it in a loop by mistake.** One run is 5 generations (about $0.07) plus
  5 checklist and 5 text-read calls (about $0.01–0.02) per critic: about $0.10 with both critics. No test
  calls a model, so `pytest` in a loop costs nothing; the billed scripts are run by hand and print the cost.
  A shell loop over `generate.py` would cost about $0.07 per iteration, which is why the scripts are one-shot.
- **What the same seed guarantees.** Same model, prompt, seed, and aspect ratio should give the same picture.
  It does not promise the same bytes (JPEG encoding can differ). *How I check:* regenerate one prompt with its
  seed, look at both, and `cmp` the files; record both answers.
- **mimo returns an empty reply** with reasoning on: the per-model table sets `effort: none`.

## Proof
**No-key tests** (`pytest week06/tests`, free, under a second):
| Test | Proves |
|---|---|
| all met → ok | the happy path |
| one unmet, named | behavior 5 |
| one requirement missing from the reply | behavior 3 |
| one requirement invented | behavior 4 |
| loose requirement matching | behavior 6 |
| reply is not JSON → failed, no crash | behavior 1 |
| JSON inside prose and fences | behavior 2 |
| "MORNING" vs "MORNlNG" mismatch; case/punctuation ignored; `None` fails | behavior 7 |
| two critiques disagree on a requirement and on the text | behavior 8 |

**The billed eval** (needs the key; run by hand, once):
| Run | Proves | Cost |
|---|---|---|
| 5 FLUX generations | images, seeds, manifest with cost | ~$0.07 |
| 5 critiques (checklist + text read) on MiniMax | the checker on real critiques | ~$0.02 |
| 5 critiques on MiMo + `--compare` | where the critic is wrong | ~$0.01 |
| 1 same-seed regeneration | the seed check | ~$0.014 |
| 1 comparison-model generation | cost and requirements on Gemini | ~$0.04 |
| 1 open-ended critique (my terminal) | what an unchecked critique claims | ~$0.002 |

Expected total: **about $0.16**.

## Approved by
Jeevan Gowda Kumaraswamy, November 2, 2026
