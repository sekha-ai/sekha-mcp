# Sekha MCP Server

> **Model Context Protocol Server for Sekha Memory**

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![CI Status](https://github.com/sekha-ai/sekha-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/sekha-ai/sekha-mcp/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/sekha-ai/sekha-mcp/branch/main/graph/badge.svg)](https://codecov.io/gh/sekha-ai/sekha-mcp)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org)


coming very soon:

[![PyPI](https://img.shields.io/pypi/v/sekha-mcp.svg)](https://pypi.org/project/sekha-mcp/)

---

## 🆕 v2.0 Release - Multi-Provider Support

**Sekha MCP v2.0** is now compatible with the new Sekha v2.0 multi-provider architecture!

**What's New:**
- ✅ Works with Sekha v2.0 controller's multi-provider routing
- ✅ Automatic provider fallback (Ollama, OpenAI, Anthropic, etc.)
- ✅ Vision support (GPT-4o, Kimi 2.5) - just include images!
- ✅ Cost-aware model selection
- ✅ Multi-dimensional embeddings (per-dimension ChromaDB collections)
- ✅ **No API changes** - fully backward compatible!

**Migration:** See [V2_MIGRATION.md](./V2_MIGRATION.md) for upgrade instructions.

---

## What is Sekha MCP?

MCP (Model Context Protocol) server that exposes Sekha memory tools to compatible LLM clients like **Claude Desktop**.

**Supported Tools:**

- ✅ `memory_store` - Save conversations
- ✅ `memory_search` - Semantic search
- ✅ `memory_get_context` - Retrieve relevant context
- ✅ `memory_update` - Update conversation metadata
- ✅ `memory_prune` - Get cleanup recommendations
- ✅ `memory_export` - Export your data
- ✅ `memory_stats` - View usage statistics

**Total: 7 MCP tools**

---

## 📚 Documentation

**Complete guide: [docs.sekha.dev/integrations/claude-desktop](https://docs.sekha.dev/integrations/claude-desktop/)**

- [Claude Desktop Integration](https://docs.sekha.dev/integrations/claude-desktop/)
- [MCP Tools Reference](https://docs.sekha.dev/api-reference/mcp-tools/)
- [Getting Started](https://docs.sekha.dev/getting-started/quickstart/)
- **[v2.0 Migration Guide](./V2_MIGRATION.md)** - Upgrade to multi-provider support

---

## 🚀 Quick Start

### 1. Install Sekha

```bash
# Deploy Sekha v2.0 stack with multi-provider support
git clone https://github.com/sekha-ai/sekha-docker.git
cd sekha-docker
git checkout feature/v2.0-provider-registry
docker compose -f docker-compose.v2.yml up -d
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
        "ghcr.io/sekha-ai/sekha-mcp:v2.0"
      ],
      "env": {
        "CONTROLLER_URL": "http://localhost:8080",
        "CONTROLLER_API_KEY": "your-mcp-api-key-here"
      }
    }
  }
}
```

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`  
**Linux:** `~/.config/Claude/claude_desktop_config.json`

### 3. Restart Claude Desktop

Sekha memory tools will now appear in Claude!

**See [full setup guide](https://docs.sekha.dev/integrations/claude-desktop/) for detailed instructions.**

---

## 🔧 Development

```bash
# Clone
git clone https://github.com/sekha-ai/sekha-mcp.git
cd sekha-mcp

# Checkout v2.0 branch
git checkout feature/v2.0-provider-registry

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
- `messages` (array) - Message array (supports images in v2.0!)
- `folder` (string, optional) - Organization folder
- `importance` (int, optional) - 1-10 scale

### memory_search
Search conversations semantically.

**Parameters:**
- `query` (string) - Search query
- `limit` (int) - Max results
- `folder` (string, optional) - Search within folder

### memory_get_context
Assemble optimal context for LLM.

**Parameters:**
- `query` (string) - Context query
- `context_budget` (int) - Token limit
- `folders` (array, optional) - Limit to specific folders

### memory_update
Update conversation metadata.

**Parameters:**
- `conversation_id` (string) - Conversation UUID
- `label` (string, optional) - New label
- `folder` (string, optional) - New folder
- `importance` (int, optional) - New importance (1-10)
- `status` (string, optional) - active/archived

### memory_prune
Get cleanup recommendations.

**Parameters:**
- `min_age_days` (int, optional) - Minimum age
- `max_importance` (int, optional) - Max importance to consider
- `limit` (int, optional) - Max suggestions

### memory_export
Export conversations.

**Parameters:**
- `format` (string) - json or markdown
- `folder` (string, optional) - Export specific folder

### memory_stats
Get memory usage statistics.

**Parameters:** None

**Returns:**
- Total conversations
- Total messages
- Storage usage
- Folder breakdown
- Provider stats (v2.0) - which models are being used

**[Full API Reference](https://docs.sekha.dev/api-reference/mcp-tools/)**

---

## 🔗 Links

- **Main Repo:** [sekha-controller](https://github.com/sekha-ai/sekha-controller)
- **v2.0 Migration:** [V2_MIGRATION.md](./V2_MIGRATION.md)
- **Docs:** [docs.sekha.dev](https://docs.sekha.dev)
- **Website:** [sekha.dev](https://sekha.dev)
- **Discord:** [discord.gg/sekha](https://discord.gg/gZb7U9deKH)

---

## 📝 Changelog

### v2.0.0 (2026-02-04)

**Added:**
- Compatible with Sekha v2.0 multi-provider architecture
- Support for vision models (images in conversations)
- Multi-dimensional embedding support
- Provider statistics in memory_stats

**Changed:**
- Version bumped to 2.0.0
- Updated documentation for v2.0 features

**Maintained:**
- Full backward compatibility with v1.x API
- No breaking changes to MCP tools
- Works with both v1.x and v2.0 controllers

### v1.0.0 (2025)

- Initial release with 7 MCP tools
- Claude Desktop integration
- Basic memory operations

---

## 📝 License

AGPL-3.0 - **[License Details](https://docs.sekha.dev/about/license/)**
