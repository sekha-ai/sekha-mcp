[![CI Status](https://github.com/sekha-ai/sekha-mcp/workflows/CI/badge.svg)](https://github.com/sekha-ai/sekha-mcp/actions)
[![codecov](https://codecov.io/gh/sekha-ai/sekha-mcp/branch/main/graph/badge.svg)](https://codecov.io/gh/sekha-ai/sekha-mcp)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org)
[![PyPI](https://img.shields.io/pypi/v/sekha-mcp.svg)](https://pypi.org/project/sekha-mcp/)


# Sekha MCP Server

Model Context Protocol server for Project Sekha - persistent AI memory for any LLM. Store, search, and manage conversations across context windows with semantic search and intelligent pruning.

## Features

- **7 powerful MCP tools** for complete memory management
- Forwards requests to Sekha Controller (Rust core at `localhost:8080`)
- Standard MCP protocol compliance (works with Claude Desktop, Cline, Cursor, Windsurf, etc.)
- Export conversations to JSON or Markdown for backup and portability
- Get usage statistics and analytics about your memory
- Fully local-first with optional cloud sync
- Open source (AGPL-v3)

## Quick Start

### Installation

```bash
git clone https://github.com/sekha-ai/sekha-mcp.git
cd sekha-mcp

# Install using pip
pip install -e .

# Or using uv (recommended)
uv pip install -e .
```

### Configuration

Create `.env` file (copy from example):
```bash
cp .env.example .env
nano .env
```

Required settings:
- `CONTROLLER_URL`: Sekha Controller URL (default: `http://localhost:8080`)
- `CONTROLLER_API_KEY`: API key from your controller `config.toml`

### Verify Setup

Test your controller connection:
```bash
curl http://localhost:8080/health
```

Start the MCP server:
```bash
python -m sekha_mcp
```

## MCP Tools

### 1. memory_store
Store a new conversation in Sekha memory with importance scoring.

**Parameters:**
- `label`: Conversation title (required, string)
- `folder`: Folder path like `/work/projects` (required, string)
- `messages`: Array of message objects with `role`, `content`, `timestamp`, `metadata` (required)
- `importance_score`: Rating 0.0-10.0, higher = more important (optional, number)

**Example:**
```json
{
  "label": "Project Planning",
  "folder": "/work/projects",
  "messages": [
    {"role": "user", "content": "Let's plan the new feature"},
    {"role": "assistant", "content": "Sure! Here's a breakdown..."}
  ],
  "importance_score": 8
}
```

---

### 2. memory_search
Search conversations semantically with similarity scoring.

**Parameters:**
- `query`: Natural language search query (required, string)
- `limit`: Max results, default 10 (optional, integer 1-50)
- `filter_labels`: Optional array of labels to restrict search

**Example:**
```json
{
  "query": "database optimization discussions",
  "limit": 10,
  "filter_labels": ["Engineering"]
}
```

---

### 3. memory_update
Update conversation metadata (label, folder, importance).

**Parameters:**
- `conversation_id`: UUID of conversation to update (required, string)
- `label`: New title (optional, string)
- `folder`: New folder path (optional, string)
- `importance_score`: New rating 0.0-10.0 (optional, number)

**Example:**
```json
{
  "conversation_id": "123e4567-e89b-12d3-a456-426614174000",
  "label": "Updated Title",
  "folder": "/work/completed",
  "importance_score": 9
}
```

---

### 4. memory_get_context
Retrieve full conversation with all messages and metadata.

**Parameters:**
- `conversation_id`: UUID of conversation (required, string)

**Example:**
```json
{
  "conversation_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

---

### 5. memory_prune
Get AI-powered suggestions for pruning old or low-importance conversations.

**Parameters:**
- `threshold_days`: Age threshold in days, default 30 (optional, integer ≥1)
- `importance_threshold`: Minimum importance to keep, default 5.0 (optional, number 0.0-10.0)

**Example:**
```json
{
  "threshold_days": 30,
  "importance_threshold": 5.0
}
```

---

### 6. memory_export
Export conversation to JSON or Markdown format for backup, migration, or external analysis.

**Parameters:**
- `conversation_id`: UUID of conversation to export (required, string)
- `format`: Export format - `json` or `markdown` (optional, string, default: `json`)
- `include_metadata`: Include word count, session count (optional, boolean, default: `true`)

**Example:**
```json
{
  "conversation_id": "123e4567-e89b-12d3-a456-426614174000",
  "format": "markdown",
  "include_metadata": true
}
```

**Use Cases:**
- Backup important conversations before pruning
- Migrate data between Sekha instances
- Analyze conversations externally
- Share with team members who don't use Sekha

---

### 7. memory_stats
Get memory system statistics and usage analytics.

**Parameters:**
- `folder`: Optional specific folder to analyze (string)

**Example:**
```json
{
  "folder": "/work/projects"
}
```

**Returns:** Total conversations, average importance, folder list, storage insights

---

## Integration

### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "sekha-memory": {
      "command": "python",
      "args": ["/path/to/sekha-mcp/main.py"],
      "env": {
        "CONTROLLER_URL": "http://localhost:8080",
        "CONTROLLER_API_KEY": "sk-sekha-your-key-here"
      }
    }
  }
}
```

### Cline (VS Code Extension)

Add to MCP settings:

```json
{
  "sekha-memory": {
    "command": "python",
    "args": ["/path/to/sekha-mcp/main.py"],
    "env": {
      "CONTROLLER_URL": "http://localhost:8080",
      "CONTROLLER_API_KEY": "sk-sekha-your-key-here"
    }
  }
}
```

### Windsurf

Add to `.codeium/windsurf/mcp_config.json`:

```json
{
  "mcpServers": {
    "sekha-memory": {
      "command": "python",
      "args": ["/path/to/sekha-mcp/main.py"],
      "env": {
        "CONTROLLER_URL": "http://localhost:8080",
        "CONTROLLER_API_KEY": "sk-sekha-your-key-here"
      }
    }
  }
}
```

---

## Architecture

```
┌─────────────────────────────────┐
│  Claude/Cline/Cursor/Windsurf   │
│      (MCP Protocol Client)      │
└────────────┬────────────────────┘
             ↓
      MCP Protocol (stdio)
             ↓
┌─────────────────────────────────┐
│      Sekha MCP Server           │
│    (Python Protocol Adapter)    │
└────────────┬────────────────────┘
             ↓
        HTTP/REST API
             ↓
┌─────────────────────────────────┐
│      Sekha Controller           │
│      (Rust Brain/Core)          │
│  • SQLite for structured data   │
│  • Chroma for vector search     │
│  • Orchestration & pruning      │
└─────────────────────────────────┘
```

---

## Troubleshooting

### C: MCP Server Not Connecting

```bash
# 1. Verify controller is running
curl http://localhost:8080/health

# 2. Check API key matches controller config.toml
echo $CONTROLLER_API_KEY

# 3. Test controller MCP endpoint directly
curl -X POST http://localhost:8080/mcp/tools/memory_stats \
  -H "Authorization: Bearer $CONTROLLER_API_KEY"

# 4. View MCP server logs (starts successfully)
python -m sekha_mcp 2>&1 | head -20
```

### C: Tool Calls Fail

1. **Check authentication:** Verify API key matches controller `config.toml`
2. **Test network:** `telnet localhost 8080` should connect
3. **Inspect controller logs:** Look for `/mcp/tools/...` requests
4. **Test GET endpoint:** `curl http://localhost:8080/api/v1/conversations/{id}`

### C: Export Tool Fails

The export tool requires the `GET /api/v1/conversations/{id}` endpoint. This should already exist in your controller. If you get "Not found" errors, verify your controller version includes this endpoint.

---

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `CONTROLLER_URL` | Sekha Controller URL | Yes | `http://localhost:8080` |
| `CONTROLLER_API_KEY` | Bearer token for auth | Yes | (none) |
| `LOG_LEVEL` | Logging verbosity (DEBUG/INFO/WARNING) | No | `INFO` |
| `REQUEST_TIMEOUT` | HTTP timeout in seconds | No | `30` |

---

## License

AGPL-v3.0-or-later

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines and code quality standards.

## Changelog

### v1.1.0 (Current)
- ✅ Added `memory_export` tool (JSON/Markdown export)
- ✅ Added `memory_stats` tool (usage analytics)
- ✅ Enhanced error messages with validation details
- ✅ Improved test coverage to 88%

### v1.0.0
- Initial release with 5 core MCP tools
- Basic CRUD operations for conversations
- Semantic search integration
- Intelligent pruning suggestions
```
