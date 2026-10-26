# Specification: Receipt Processor Components

## Component 1: Reader (Vision Model)
- **Language/Library Decision:** Python 3 standard library (`urllib.request`, `json`, `os`, `pathlib`, `base64`) chosen to eliminate external package vulnerabilities and simplify cross-platform execution.
- **Model Comparison:** Evaluates two models via OpenRouter: Primary Model (`anthropic/claude-3.5-haiku`) and Secondary Model (`openai/gpt-4o-mini`).
- **Harness:** Custom zero-dependency Python script acting as the evaluation harness.

## Component 2: Checker
- **Role:** Programmatically validates extracted line items against reported totals independently, avoiding blind trust in LLM outputs.

## Numbered Behaviors & Error Handling
1. **Behavior 1 (Successful Extraction):** Clean receipt images return complete JSON fields (`vendor`, `date`, `items`, `tax`, `total`).
2. **Behavior 2 (Non-JSON Reply):** If the model wraps output in markdown text or conversational prose, the parser strips fences and validates JSON structure.
3. **Behavior 3 (Inconsistent Receipt):** The checker flags arithmetic mismatches when line items and tax do not sum to the reported total.
4. **Behavior 4 (Missing Year):** When receipts omit temporal data, the reader flags incomplete date fields rather than guessing.

## External Dependencies
- OpenRouter API (accessed exclusively via Python standard library `urllib.request`, zero pip dependencies).
