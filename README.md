# Sekha MCP Server

> **Model Context Protocol Server for Sekha Memory**

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org)

---

## What is Sekha MCP?

MCP (Model Context Protocol) server that exposes Sekha memory tools to compatible LLM clients like **Claude Desktop**.

**Supported Tools:**

- ✅ `memory_store` - Save conversations
- ✅ `memory_query` - Semantic search
- ✅ `memory_get_context` - Retrieve relevant context
- ✅ `memory_create_label` - Organize conversations
- ✅ `memory_prune_suggest` - Get cleanup recommendations
- ✅ `memory_export` - Export your data
- ✅ `memory_stats` - View usage statistics

---

## 📚 Documentation

**Complete guide: [docs.sekha.dev/integrations/claude-desktop](https://docs.sekha.dev/integrations/claude-desktop/)**

- [Claude Desktop Integration](https://docs.sekha.dev/integrations/claude-desktop/)
- [MCP Tools Reference](https://docs.sekha.dev/api-reference/mcp-tools/)
- [Getting Started](https://docs.sekha.dev/getting-started/quickstart/)

---

## 🚀 Quick Start

### 1. Install Sekha

```bash
# Deploy Sekha stack
git clone https://github.com/sekha-ai/sekha-docker.git
cd sekha-docker
docker compose up -d
```

### 2. Configure Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS):

```json
{
  "mcpServers": {
    "sekha": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "--network=host",
        "ghcr.io/sekha-ai/sekha-mcp:latest"
      ]
    }
  }
}
```

### 3. Restart Claude Desktop

Sekha memory tools will now appear in Claude!

**See [full setup guide](https://docs.sekha.dev/integrations/claude-desktop/) for detailed instructions.**

---

## 🔧 Development

```bash
# Clone
git clone https://github.com/sekha-ai/sekha-mcp.git
cd sekha-mcp

# Install
pip install -e .

# Run locally
python -m sekha_mcp

# Test
pytest
```

---

## 📚 MCP Tools Reference

### memory_store
Store a conversation in Sekha.

**Parameters:**
- `label` (string) - Conversation label
- `messages` (array) - Message array
- `folder` (string, optional) - Organization folder
- `importance` (int, optional) - 1-10 scale

### memory_query
Search conversations semantically.

**Parameters:**
- `query` (string) - Search query
- `limit` (int) - Max results

### memory_get_context
Assemble optimal context for LLM.

**Parameters:**
- `query` (string) - Context query
- `context_budget` (int) - Token limit

**[Full API Reference](https://docs.sekha.dev/api-reference/mcp-tools/)**

---

## 🔗 Links

- **Main Repo:** [sekha-controller](https://github.com/sekha-ai/sekha-controller)
- **Docs:** [docs.sekha.dev](https://docs.sekha.dev)
- **Website:** [sekha.dev](https://sekha.dev)
- **Discord:** [discord.gg/sekha](https://discord.gg/sekha)

---

## 📄 License

AGPL-3.0 - **[License Details](https://docs.sekha.dev/about/license/)**
