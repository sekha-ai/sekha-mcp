# Sekha LLM Bridge

Python service for LLM operations (embeddings, summarization, importance scoring, entity extraction).

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Start Ollama (if not running)
ollama serve

# Pull required models
ollama pull nomic-embed-text:latest
ollama pull llama3.1:8b

# Start the bridge
python main.py

# Or with Docker
docker build -t sekha-llm-bridge .
docker run -p 5001:5001 --network host sekha-llm-bridge



# Sekha MCP Server

Model Context Protocol server for Project Sekha, providing memory management tools for AI assistants.

## Features

- **6 MCP Tools** for memory operations
- Forwards requests to Sekha Controller (Rust core)
- Standard MCP protocol compliance
- Easy integration with Claude Desktop, Cline, etc.

## Quick Start

### Installation

Clone repository
git clone https://github.com/sekha-ai/sekha-mcp.git
cd sekha-mcp

Install dependencies
pip install -e .

Or with UV (recommended)
uv pip install -e .


### Configuration


Create .env file
cp .env.example .env

Edit configuration
nano .env


### Running

Start MCP server (stdio mode)
python main.py

Or using entry point
sekha-mcp


## MCP Tools

### 1. memory_store
Store a new conversation in Sekha memory.

{
"label": "Project Planning",
"folder": "/work/projects",
"messages": [
{"role": "user", "content": "Let's plan the new feature"},
{"role": "assistant", "content": "Sure! Here's a breakdown..."}
],
"importance_score": 8
}


### 2. memory_search
Search conversations semantically.


{
"query": "database optimization discussions",
"limit": 10,
"filter_labels": ["Engineering"]
}


### 3. memory_update
Update conversation metadata.

{
"conversation_id": "123e4567-e89b-12d3-a456-426614174000",
"label": "Updated Title",
"importance_score": 9
}


### 4. memory_get_context
Retrieve full conversation with all messages.

{
"conversation_id": "123e4567-e89b-12d3-a456-426614174000"
}


### 5. memory_prune
Get pruning suggestions for old conversations.

{
"threshold_days": 30,
"importance_threshold": 5.0
}


## Integration

### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

{
"mcpServers": {
"sekha-memory": {
"command": "python",
"args": ["/path/to/sekha-mcp/main.py"],
"env": {
"CONTROLLER_URL": "http://localhost:8080",
"CONTROLLER_API_KEY": "your_api_key_here"
}
}
}
}


### Cline (VS Code Extension)

Add to MCP settings:


{
"sekha-memory": {
"command": "python",
"args": ["/path/to/sekha-mcp/main.py"]
}
}


## Development

### Running Tests

Install dev dependencies
pip install -e ".[dev]"

Run tests
pytest

With coverage
pytest --cov=src --cov-report=html


### Code Quality


Format code
black src/ tests/

Lint
ruff src/ tests/


## Architecture

┌──────────────┐
│ Claude/Cline │
│ (MCP Client)│
└──────┬───────┘
│ MCP Protocol (stdio)
▼
┌──────────────┐
│ Sekha MCP │
│ Server │
└──────┬───────┘
│ HTTP/REST
▼
┌──────────────┐
│ Sekha │
│ Controller │
│ (Rust Core) │
└──────────────┘


## Troubleshooting

**MCP server not connecting?**
- Verify Sekha Controller is running (`http://localhost:8080/health`)
- Check API key in `.env` matches controller configuration
- View logs: server outputs to stderr

**Tool calls failing?**
- Test controller directly: `curl http://localhost:8080/mcp/tools/memory_store`
- Verify authentication header is correct
- Check network connectivity

## License
AGPL-v3

