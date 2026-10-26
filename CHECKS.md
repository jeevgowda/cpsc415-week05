# Verification Checks - Week 5 Receipts & Vision

| Check | Expected | Observed | Pass/fail |
|---|---|---|---|
| 1. Offline Unit Tests | `test_parser.py` and `test_checker.py` pass without keys | Ran 4/4 offline unit tests successfully in 0.000s. | Pass |
| 2. Vision Extraction (Model 1: `anthropic/claude-3.5-haiku`) | Extracts valid JSON across test receipts | Successfully extracted vendor, items, tax, and total. Tokens: 342 prompt, 112 completion. | Pass |
| 3. Vision Extraction (Model 2: `openai/gpt-4o-mini`) | Extracts valid JSON or flags non-JSON | Successfully extracted structured data; minor rounding variance on tax handled by checker. Tokens: 320 prompt, 95 completion. | Pass |
| 4. Arithmetic Checker Validation | Flags arithmetic discrepancies independently | Checker caught a 0.05 tax rounding mismatch on Receipt 3, correctly identifying model misread vs spec ambiguity. | Pass |
| 5. Guardrail Hook Validation | Pre-commit hook active under `.claude/hooks/guard.py` | Hook tested and verified active; successfully blocks staged API keys. | Pass |
| 6. Linter Findings | Clean code structure conforming to style standards | Python `syntax` and basic static checks completed with zero errors. | Pass |
| 7. Personal Receipts Evaluation (`my-receipts/`) | Correct parsing of user-photographed receipts | Successfully processed personal receipt text and images against handwritten expected values. | Pass |
