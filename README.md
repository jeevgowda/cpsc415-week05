# Week 5: Receipts to Data, with Tests

## Overview
A zero-dependency Python receipt digitization pipeline (`parser.py` and `checker.py`) utilizing vision-capable LLMs to extract structured transaction data from images, paired with an independent arithmetic validation checker, security guardrail, and offline unit test suite.

## Harness & Model Configuration
- **Harness:** Custom Python evaluation script (`eval_receipts.py`).
- **Primary Model:** `anthropic/claude-3.5-haiku` via OpenRouter.
- **Secondary Model:** `openai/gpt-4o-mini` via OpenRouter.

## How to Build & Run
1. Set OpenRouter API key:
   export OPENROUTER_API_KEY="your-key"
2. Run offline unit tests (no key required):
   python3 -m unittest test_parser.py test_checker.py
3. Run evaluation suite:
   python3 eval_receipts.py
