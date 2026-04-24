# code it yourself silly

Lightweight Python MCP server with one tool: `should_a_human_do_it`.

The tool looks at a user prompt and optional code context, then decides whether a request is so trivial that a human should do it directly.

If yes, it returns a very short, human-readable instruction intended for the agent to relay with minimal token usage.

## Tool

- `should_a_human_do_it(prompt: str, code_context: str = "")`
  - Returns:
    - `should_human_do_it` (`bool`)
    - `confidence` (`float`)
    - `rationale` (`str`)
    - `agent_instruction` (`str`)

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -e .
code-it-yourself-silly
```

## Notes

- Heuristics are intentionally simple and fast.
- You can tune `SIMPLE_PATTERNS`, `COMPLEX_PATTERNS`, and scoring in `server.py`.

## MCP config snippets

- Copy/paste snippets for common agentic coding IDEs/clients:
  - `configs/mcp-config-snippets.md`
