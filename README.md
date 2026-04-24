# code it yourself silly

Lightweight Python MCP server with one tool: `triage_code_request`.

The tool looks at a user prompt and optional code context, then decides whether a request is so trivial that a human should do it directly.

If yes, it returns a very short, human-readable instruction intended for the agent to relay with minimal token usage.

## Tool

- `triage_code_request(prompt: str, code_context: str = "")`
  - Returns:
    - `manual_recommended` (`bool`)
    - `confidence` (`float`)
    - `explanation` (`str`)
    - `recommended_action` (`str`)

## Getting clients to actually call it

Some clients are conservative about tool use. Make this tool easier to select by:

- Keeping clear action-oriented tool names.
- Adding a client custom instruction that explicitly asks for a pre-flight triage call.

Example custom instruction (Copilot/agent instructions):

```text
Before implementing any coding task, call `triage_code_request` with the user prompt
and any available code context. If it returns manual_recommended=true and confidence>=0.7,
present `recommended_action` first and ask the user to confirm before proceeding.
```

## Run locally

Prerequisite: install `uv` first.
- Docs + install instructions: https://docs.astral.sh/uv/getting-started/installation/

```bash
uv sync
uv run code-it-yourself-silly
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
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "C:\\path\\to\\code-it-yourself-silly",
        "server.py"
      ]
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
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "C:\\path\\to\\code-it-yourself-silly",
        "server.py"
      ]
    }
  ]
}
```

### macOS/Linux variant

Use this command path in all snippets above:

```json
{
  "command": "uv",
  "args": [
    "run",
    "--directory",
    "/path/to/code-it-yourself-silly",
    "server.py"
  ]
}
```
