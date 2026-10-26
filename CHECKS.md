# Verification Checks - Week 5 Receipts

| Check | Expected | Observed | Pass/fail |
|---|---|---|---|
| 1. Unit Tests (Parser & Checker) | All offline tests pass successfully | Ran `test_parser.py` and `test_checker.py`; 4/4 tests passed cleanly without API keys. | Pass |
| 2. Vision Extraction (Claude 3.5 Haiku) | Extracts valid JSON fields from receipt images | Successfully parsed sample image fields with token counts recorded. | Pass |
| 3. Vision Extraction (GPT-4o-mini) | Extracts valid JSON fields or flags non-JSON | Successfully evaluated extraction output and formatting behavior. | Pass |
| 4. Arithmetic Checker Verification | Flags discrepancies instead of trusting model | Checker independently computed line items + tax vs reported total, catching math errors. | Pass |
| 5. Guardrail Hook Validation | Pre-commit hook active and blocking secrets | Guardrail script tested and confirmed active under `.claude/hooks/guard.py`. | Pass |
