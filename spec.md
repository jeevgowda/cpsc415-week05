# Specification: Receipt Processor Components

## Component 1: Reader (Vision Model)
- **Language/Library Decision:** Python 3 standard library (`urllib.request`, `json`, `os`, `pathlib`).
- **Model Comparison:** Compares `anthropic/claude-3.5-haiku` and `openai/gpt-4o-mini` via OpenRouter for image-to-text JSON extraction.

## Component 2: Checker
- **Role:** Programmatically validates extracted line items against reported totals, flagging arithmetic discrepancies.

## Numbered Behaviors
1. **Behavior 1 (Successful Extraction):** Clean receipt images return complete JSON fields.
2. **Behavior 2 (Non-JSON Reply):** If model outputs markdown/text prose, parser handles or flags failure.
3. **Behavior 3 (Inconsistent Receipt):** Checker flags arithmetic mismatches between line items and reported totals.
4. **Behavior 4 (Missing Year):** Reader infers or flags incomplete temporal data.

## Dependencies
- OpenRouter API (Zero external pip packages; standard library only).
