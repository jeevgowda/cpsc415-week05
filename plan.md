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
