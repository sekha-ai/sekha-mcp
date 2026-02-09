# Sekha MCP Server

> **Model Context Protocol Server for Sekha Memory**

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![CI Status](https://github.com/sekha-ai/sekha-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/sekha-ai/sekha-mcp/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/sekha-ai/sekha-mcp/branch/main/graph/badge.svg)](https://codecov.io/gh/sekha-ai/sekha-mcp)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org)

coming very soon:

[![PyPI](https://img.shields.io/pypi/v/sekha-mcp.svg)](https://pypi.org/project/sekha-mcp/)

---

## 🆕 v0.2.0 Release - Multi-Provider Support

**Sekha MCP v0.2.0** is now compatible with the new Sekha v0.2.0 multi-provider architecture!

**What's New:**
- ✅ Works with Sekha v0.2.0 controller's multi-provider routing
- ✅ Automatic provider fallback (Ollama, OpenAI, Anthropic, etc.)
- ✅ Vision support (GPT-4o, Kimi 2.5) - just include images!
- ✅ Cost-aware model selection
- ✅ Multi-dimensional embeddings (per-dimension ChromaDB collections)
- ✅ **Claude Desktop & Claude Code support** - memory in both apps!
- ✅ **No API changes** - fully backward compatible!

---

## What is Sekha MCP?

MCP (Model Context Protocol) server that exposes Sekha memory tools to any MCP-compatible client:

- ✅ **Claude Desktop** - Anthropic's desktop app
- ✅ **Claude Code** - VS Code extension (works with Ollama, Anthropic, or any provider)
- ✅ **Any MCP client** - Standard protocol implementation

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

**Complete guide: [docs.sekha.dev/integrations/mcp](https://docs.sekha.dev/integrations/mcp/)**

- [Claude Desktop Integration](https://docs.sekha.dev/integrations/claude-desktop/)
- [Claude Code Integration](https://docs.sekha.dev/integrations/claude-code/)
- [MCP Tools Reference](https://docs.sekha.dev/api-reference/mcp-tools/)
- [Getting Started](https://docs.sekha.dev/getting-started/quickstart/)

---

## 🚀 Quick Start

### 1. Install Sekha

```bash
# Deploy Sekha v0.2.0 stack with multi-provider support
git clone https://github.com/sekha-ai/sekha-docker.git
cd sekha-docker
docker compose -f docker/docker-compose.prod.yml up -d
```

### 2. Configure Your MCP Client

#### Option A: Claude Desktop

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
        "ghcr.io/sekha-ai/sekha-mcp:v0.2.0"
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

#### Option B: Claude Code (VS Code Extension)

Add to VS Code `settings.json` or workspace config:

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
        "ghcr.io/sekha-ai/sekha-mcp:v0.2.0"
      ],
      "env": {
        "CONTROLLER_URL": "http://localhost:8080",
        "CONTROLLER_API_KEY": "your-mcp-api-key-here"
      }
    }
  }
}
```

**Claude Code Configuration:**

Claude Code lets you choose your LLM provider separately from memory:

```json
{
  // Sekha provides memory (via MCP)
  "mcpServers": {
    "sekha": { /* config above */ }
  },
  
  // Configure your LLM provider (Claude Code supports multiple)
  "claudeCode.apiProvider": "ollama",  // or "anthropic"
  "claudeCode.ollamaUrl": "http://localhost:11434",
  "claudeCode.ollamaModel": "llama3.1:8b"
}
```

**This means:**
- Use **Ollama (or other LLM) locally** for generation (fast, private, free)
- Use **Sekha MCP** for memory (persistent across sessions)
- Best of both worlds!

### 3. Restart Your Client

- **Claude Desktop**: Restart the app
- **Claude Code**: Reload VS Code window (`Cmd+Shift+P` → "Reload Window")

Sekha memory tools will now appear!

**See setup guides:**
- [Claude Desktop setup](https://docs.sekha.dev/integrations/claude-desktop/)
- [Claude Code setup](https://docs.sekha.dev/integrations/claude-code/)

---

## 🎯 Use Cases

### Claude Desktop - Interactive Conversations
- Full-featured desktop app with Sekha memory
- Perfect for brainstorming, research, general chat
- Uses Anthropic's Claude models

### Claude Code - Development Workflow Examples
- VS Code extension with code-aware features
- Use with **Ollama** for fast, local, private coding
- Or use with Anthropic/OpenAI for powerful cloud models
- Sekha memory works with **any provider** you configure

### API Integration - Programmatic Access
- Use [sekha-proxy](https://github.com/sekha-ai/sekha-proxy) for OpenAI-compatible API
- Multi-provider routing via LLM bridge
- Same memory as Claude apps

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
- `messages` (array) - Message array (supports images in v0.2.0!)
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
- Provider stats (v0.2.0) - which models are being used

**[Full API Reference](https://docs.sekha.dev/api-reference/mcp-tools/)**

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│  MCP Clients                                │
│  - Claude Desktop (Anthropic)               │
│  - Claude Code (Ollama/Anthropic/etc.)      │
│  - Any MCP-compatible client                │
└────────────────┬────────────────────────────┘
                 │
                 ▼
        ┌────────────────┐
        │  Sekha MCP     │ ← This repository
        │  Server        │
        └────────┬───────┘
                 │
                 ▼
        ┌────────────────┐
        │  Controller    │ ← Memory APIs
        │  (Rust)        │
        └────────┬───────┘
                 │
                 ▼
        ┌────────────────┐
        │  ChromaDB      │ ← Vector storage
        │  Redis         │ ← Cache
        └────────────────┘

Separate from LLM routing:
┌─────────────────────────────────────────────┐
│  API Clients → Proxy → Bridge → Providers   │
│  (OpenAI SDK compatible)                    │
└─────────────────────────────────────────────┘
```

**Key Points:**
- MCP provides **memory tools only**
- Claude Desktop/Code handle their own LLM connections
- Controller stores all conversations regardless of source
- Same memory accessible from Claude apps and API

---

## 🔗 Links

- **Main Repo:** [sekha-controller](https://github.com/sekha-ai/sekha-controller)
- **Proxy (API):** [sekha-proxy](https://github.com/sekha-ai/sekha-proxy)
- **Docker Deploy:** [sekha-docker](https://github.com/sekha-ai/sekha-docker)
- **Docs:** [docs.sekha.dev](https://docs.sekha.dev)
- **Website:** [sekha.dev](https://sekha.dev)
- **Discord:** [discord.gg/sekha](https://discord.gg/gZb7U9deKH)

---

## 📝 Changelog

### v0.2.0 (2026-02-04)

**Added:**
- Compatible with Sekha v0.2.0 multi-provider architecture
- Support for vision models (images in conversations)
- Multi-dimensional embedding support
- Provider statistics in memory_stats
- **Explicit Claude Code documentation and examples**
- **Ollama + Sekha workflow guide**

**Changed:**
- Version bumped to 0.2.0
- Updated documentation for v0.2.0 features
- Clarified MCP works with any compatible client

**Maintained:**
- Full backward compatibility with v1.x API
- No breaking changes to MCP tools
- Works with both v0.1.x and v0.2.0 controllers

### v0.1.0 (2025)

- Initial release with 7 MCP tools
- Claude Desktop integration
- Basic memory operations

---

## 📝 License

AGPL-3.0 - **[License Details](https://docs.sekha.dev/about/license/)**
```