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

Server name used in examples: `code-it-yourself-silly`

Assumes project path:
- Windows: `C:\\path\\to\\code-it-yourself-silly`
- macOS/Linux: `/path/to/code-it-yourself-silly`

### Cursor / Windsurf / VS Code + Cline / Claude Desktop

Use this same `mcpServers` object format:

```json
{
  "mcpServers": {
    "code-it-yourself-silly": {
      "command": "C:\\path\\to\\code-it-yourself-silly\\.venv\\Scripts\\python.exe",
      "args": ["C:\\path\\to\\code-it-yourself-silly\\server.py"]
    }
  }
}
```

### VS Code + Continue

Add/update in `.continue/config.json`:

```json
{
  "mcpServers": [
    {
      "name": "code-it-yourself-silly",
      "command": "C:\\path\\to\\code-it-yourself-silly\\.venv\\Scripts\\python.exe",
      "args": ["C:\\path\\to\\code-it-yourself-silly\\server.py"]
    }
  ]
}
```

### macOS/Linux variant

Use this command path in all snippets above:

```json
{
  "command": "/path/to/code-it-yourself-silly/.venv/bin/python",
  "args": ["/path/to/code-it-yourself-silly/server.py"]
}
```
