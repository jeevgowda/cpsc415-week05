# CLAUDE.md: cpsc415-week05

Jeevan Gowda Kumaraswamy's Week 5 (receipt reader) and Week 6 (image set) labs for CPSC 415.
The chain is intent/ → spec.md → plan.md → tests → code; read those before changing anything.

## Working rules

- No API key, token, or `.env` file is ever committed; the key is `OPENROUTER_API_KEY` in the environment.
- Every dependency is named in `spec.md` with its reason before it is installed; `.claude/hooks/guard.py` enforces it.
- Week 6: the image-set lab lives in week06/. Stages assigned: intent, spec,
  plan, tests, and (in the team repository only) a reviewed pull request.
  Commit to main here; branches and PRs are for the team repository.
- Image generation and vision calls are billed. One generation per prompt,
  one critique per image, fixed seeds. Never loop over the model inside a test.
- The critique is model output. The code compares it with the requirements;
  it does not trust it.
