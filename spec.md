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

---

# Week 6: image set

Source: `intent/image-set.md`. Code lives in `week06/`.

**Approved by:** Jeevan Gowda Kumaraswamy, November 2, 2026

## Component: generator (`week06/generate.py`)
- **Language decision:** Python 3.13. Team Project 1 is Python/FastAPI, the course's request shapes are
  Python, and the `openrouter` SDK wraps the Image API so I do not hand-write the request (Week 5 used
  `urllib`; the image endpoint's reply shape is easier through the SDK).
- **Model decision:** default `black-forest-labs/flux.2-klein-4b`: takes a seed, about $0.014 per image,
  a few seconds per call, and it is Team Project 1's image model. Comparison:
  `google/gemini-3.1-flash-lite-image`, priced per image token (about $0.03–0.04 per image), to see whether
  a costlier model meets the same requirements and spells "MORNING" right.
- **Request:** OpenRouter Image API through `client.images.generate(model, prompt, aspect_ratio, seed)`.
- **Writes** `images/manifest.json`: for each image the name, prompt, seed, requirements, expected text,
  model, aspect ratio, file, media type, the cost from the reply's `usage.cost`, and the seconds.

## Component: critic-checker (`week06/critique.py`)
- **Language decision:** Python 3.13, the same reasons; the checker is plain code with no SDK so its tests
  need no key.
- **Model decision:** critic `minimax/minimax-m3` (the class vision model, reasoning on). It is checked by a
  second model, `xiaomi/mimo-v2.6-flash` (a different company's model, cheaper, reasoning off via
  `reasoning={"effort": "none"}`), and the code lists where they disagree.
- **Request:** the chat endpoint with the image as a base64 data URL content part (Week 5's request), and a
  checklist prompt that asks for one JSON object `{"checks": [{"requirement", "met", "evidence"}]}`.
  A second, narrow question asks the model to write the printed text exactly as printed.

## Dependencies
| Package | Reason |
|---|---|
| `openrouter` | The OpenRouter SDK: one client and one key for the Image API (`client.images.generate`) and the chat endpoint with an image part (`client.chat.send`). Team Project 1 uses the same SDK. |
| `pytest` | Runs the no-key checker tests. Development only. |
| `ruff` | Linter; findings recorded in `week06/CHECKS.md`. Development only. |

## Behaviors
1. **A critique that is not JSON is a failed critique, not a crash.** `extract_json` returns `None` for a
   reply with no JSON object; `check` then reports every requirement as missing and `ok: false`.
2. **JSON inside prose or code fences is extracted**, not rejected.
3. **A requirement the critic did not answer counts as a problem** (`missing`), even if every answered item passed.
4. **A requirement the critic invented counts as a problem** (`extra`).
5. **An unmet requirement is reported by name** (`unmet`). Anything other than `met: true` is unmet.
6. **Requirement text is matched ignoring case and punctuation**, so "the mug is white." answers "The mug is white".
7. **Expected text is compared in code, not by the critic.** The narrow read is compared with
   `expected_text` ignoring case and punctuation; "MORNING" vs "MORNlNG" is a mismatch.
8. **Two critiques are compared in code.** `--compare a.json b.json` lists every image and requirement where
   the two models' verdicts or text reads differ. No key needed.
9. **No key, no call.** Without `OPENROUTER_API_KEY`, `generate.py` and `critique.py` exit with one line and
   bill nothing; tests that would call a model are skipped.
10. **Every billed call is recorded**: the generation cost from `usage.cost` in the manifest, and the
    critique's token usage and finish reason in the critique file.
