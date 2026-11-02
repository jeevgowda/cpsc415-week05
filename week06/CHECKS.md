# Week 6 checks: image set, critique checked, reviewed PR

Prompt family: one product (a white ceramic mug printed "MORNING"), five views, seeds 6101–6105
(`prompts.json`). Generator `black-forest-labs/flux.2-klein-4b`; critic `minimax/minimax-m3`; second critic
`xiaomi/mimo-v2.6-flash`. All runs on November 2, 2026.

## No-key tests

`pytest week06/tests` before `critique.py` existed: collection error, `ModuleNotFoundError` (red, as intended).
With the checker written: **11 passed in 0.01 s**.

## Linter (`ruff check .`)

- `week06/`: **All checks passed.**
- The whole repository: 18 findings, none in `week06/`. They are in my Week 5 files (`eval_receipts.py`: 4 unused
  imports (F401) and an unsorted import block; `parser.py`, `test_parser.py`: `str.removeprefix` suggestions
  (FURB188), unsorted imports, and a blind `except Exception` (BLE001); `test_checker.py`: unused `msg`
  (RUF059)) and in the course's `guard.py` (EXE002, PIE810), which is copied verbatim. I left the Week 5
  files as they were submitted.

## Per image (FLUX.2 klein, critic MiniMax M3)

| Image | Cost | Gen s | Checker verdict | Title read | Match |
|---|---|---|---|---|---|
| mug-01-front | $0.014 | 4.3 | ok | MORNING | yes |
| mug-02-topdown | $0.014 | 4.1 | ok | MORNING | yes |
| mug-03-handle | $0.014 | 4.0 | ok | MORNING | yes |
| mug-04-angle | $0.014 | 3.3 | ok | MORNING | yes |
| mug-05-lifestyle | $0.014 | 3.1 | ok | MORNING | yes |

Generation total **$0.070** (`usage.cost` from each reply, in `images/manifest.json`). Every critique was JSON,
answered every requirement, and invented none; all finished with `stop`. MiniMax used 925–1,738 input and
196–399 output tokens per checklist.

**Looking at the images** (opened before the critiques were read; the descriptions below were checked against each image): FLUX spelled "MORNING" correctly on all five, letter by letter.
But **mug-03 and mug-04 have two handles**, one on each side, which a one-handled mug for sale does not have.
mug-04 is also shot straight on, not at the three-quarter angle the prompt asked for. MiniMax passed both.

## Seed check

`mug-01-front` regenerated with seed 6101 (`images-seed/`, $0.014, 3.9 s). **Looking:** the same picture:
same mug, handle, lettering, and framing. **`cmp`:** the files differ (`differ: char 24`; 122,162 vs 123,035
bytes). A seed fixes the picture on this model, not the JPEG bytes, so compare by eye or by the title read,
never by hash.

## Comparison image model

`google/gemini-3.1-flash-lite-image`, same prompt and seed as mug-01 (`images-nb/`): **$0.03362** from
`usage.cost`, 4.5 s, `image/jpeg`. 2.4× FLUX's price. **Looking:** one white mug, one handle, plain white
background, "MORNING" spelled correctly. It meets all four requirements of mug-01, as FLUX's mug-01 did.

## Step 5: the critic checked

### The second model (`critique.py --compare critique.json critique-mimo.json`)

MiMo: 2/5 pass. MiniMax: 5/5 pass. Both read "MORNING" on all five (MiMo's text reads were 4 tokens each).
3 images, 5 disagreements:

| Image | Requirement | MiniMax | MiMo | What I saw |
|---|---|---|---|---|
| mug-02 | The mug is seen from above | met | unmet ("at an angle… text readable") | A high angle looking down into the coffee, but not directly overhead, since the side and the word are fully visible. The prompt said "directly above"; **MiMo is closer to right.** |
| mug-03 | There is exactly one mug | met | unmet ("a single mug but with two handles") | There is exactly one mug, **with two handles**. MiniMax is right on the letter of the requirement; **MiMo found the real defect** and filed it under the wrong requirement. |
| mug-03 | The handle fills a large part of the image | met | unmet | It is a full mug shot, not a handle close-up; the handles are at the edges. **MiMo is right.** |
| mug-04 | There is exactly one mug | met | unmet (two handles) | Same as mug-03: one mug, **two handles**. MiMo found the defect. |
| mug-04 | Seen at an angle, not straight on | met | unmet ("viewed straight-on") | Straight on and symmetric. **MiMo is right.** |

MiniMax was wrong on 3 of 5 disagreements and missed a real product defect on two images. MiMo was wrong
only on the literal "exactly one mug", and even there it was pointing at the real problem.

### The open-ended critique

_(pending: run in my own terminal)_

### Which check caught what

_(pending)_

## Review

PR: https://github.com/Kuany4953/Product-listing-generator/pull/10, branch `week06-jeevan-mugs`.
Commits on the branch: spec line → `tests/test_lab_images.py` (red: `images/mug/` missing) → the image set (green).
Gate (pre-push: ruff and the no-key tests): **passed**, 124 passed and 1 skipped.

The earlier PR #7 (generation, storage with C2PA, grid, Retry) merged on November 1 without the reviewer's
output or an approval; this PR is the one that carries my image set and goes through the full review.

**Reviewer findings by pass:**
- `minimax/minimax-m3` (default): **No findings.** Exit **0**. $0.00486.
- `xiaomi/mimo-v2.6-flash` (second opinion): exit 2, because the reply had no NONE line in the required form.
  The raw findings were:
  - **Pass 2** (×2): the spec's "Model comparison" table is still empty and should be filled from these critiques.
  - **Pass 3**: `test_the_mug_set_is_committed` is redundant with the parametrized test.

**Fixed:** nothing; no finding called for a code change.

**Pushed back on (replies on the PR):**
- The pass-2 findings are out of scope. That table is defined as the *basket* set's comparison, filled from
  Kuany's run. Filling it with mug numbers would silently change the spec, which is itself a pass-1 problem.
- The pass-3 test is not redundant. Without it, the parametrized test passes on the basket manifest alone, and
  it is the test that went red first.

**Last exit code:** _(pending)_. **Approved by:** _(pending: teammate approval on GitHub)_.

## Cost

Generation $0.070 + seed check $0.014 + Gemini $0.0336 + both critics' runs (tokens recorded in the critique
files) + reviewer $0.0064 = about **$0.14**.
