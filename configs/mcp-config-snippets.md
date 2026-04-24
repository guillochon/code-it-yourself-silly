# MCP config snippets

Server name used in examples: `code-it-yourself-silly`

Assumes project path:
- Windows: `C:\\path\\to\\code-it-yourself-silly`
- macOS/Linux: `/path/to/code-it-yourself-silly`

## Cursor / Windsurf / VS Code + Cline / Claude Desktop

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

## VS Code + Continue

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

## macOS/Linux variant

Use this command path in all snippets above:

```json
{
  "command": "/path/to/code-it-yourself-silly/.venv/bin/python",
  "args": ["/path/to/code-it-yourself-silly/server.py"]
}
```
