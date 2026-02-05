# Sekha MCP v2.0 Migration Guide

## Overview

Sekha MCP v2.0 is compatible with the new Sekha v2.0 multi-provider architecture. **No breaking changes** to the MCP API itself - all changes are transparent and handled by the controller.

## What Changed

### Version Updates
- Package version: `1.0.0` → `2.0.0`
- Server version in config: `1.0.0` → `2.0.0`

### Architecture Changes (Behind the Scenes)

The MCP server now connects to a v2.0 controller that supports:
- **Multiple LLM providers** (Ollama, OpenAI, Anthropic, OpenRouter, etc.)
- **Automatic provider fallback** with circuit breakers
- **Cost-aware routing** for optimal model selection
- **Vision support** (GPT-4o, Kimi 2.5, etc.)
- **Multi-dimensional embeddings** (separate ChromaDB collections per dimension)

## Migration Steps

### For Existing Deployments

1. **Update the controller to v2.0 first**
   ```bash
   # Controller must be upgraded before MCP server
   cd sekha-controller
   git checkout feature/v2.0-provider-registry
   cargo build --release
   ```

2. **Update MCP server**
   ```bash
   cd sekha-mcp
   git checkout feature/v2.0-provider-registry
   pip install -e .
   ```

3. **No config changes required**
   - Your existing `.env` and `config.py` settings work as-is
   - Controller URL and API key remain the same
   - Provider configuration is now in the controller

4. **Restart the MCP server**
   ```bash
   sekha-mcp
   ```

### For New Deployments

1. **Clone and install**
   ```bash
   git clone https://github.com/sekha-ai/sekha-mcp.git
   cd sekha-mcp
   git checkout feature/v2.0-provider-registry
   pip install -e .
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your controller URL and API key
   ```

3. **Run**
   ```bash
   sekha-mcp
   ```

## Compatibility

### Backward Compatibility
- ✅ MCP v2.0 works with controller v2.0 (recommended)
- ✅ MCP v2.0 works with controller v1.x (degraded mode, no multi-provider)
- ❌ MCP v1.x with controller v2.0 (not recommended, may have issues)

### Claude Desktop Integration

No changes needed to your Claude Desktop MCP configuration:

```json
{
  "mcpServers": {
    "sekha-memory": {
      "command": "sekha-mcp",
      "env": {
        "CONTROLLER_URL": "http://localhost:8080",
        "CONTROLLER_API_KEY": "your_key_here"
      }
    }
  }
}
```

## New Features (Transparent)

These features are automatically available without any MCP-side changes:

### Multi-Provider Support
Controller now routes to the best available provider:
- **Embeddings**: Automatically uses configured embedding model (nomic-embed-text, text-embedding-3-large, etc.)
- **Chat/Summarization**: Routes to optimal chat model based on context size
- **Vision**: Automatically detects images and routes to vision-capable models

### Cost Optimization
Controller tracks estimated costs and can:
- Route to cheaper models when appropriate
- Enforce budget limits per request
- Report cost estimates in responses

### Resilience
- Automatic failover to secondary providers
- Circuit breakers prevent cascading failures
- Graceful degradation when providers are down

### Dimension-Aware Embeddings
- Controller creates separate ChromaDB collections per embedding dimension
- Searches work across all dimensions automatically
- No data migration needed (new collections created on first use)

## Testing

Verify your v2.0 setup:

```bash
# Run unit tests
pytest tests/

# Test MCP connection
curl http://localhost:8080/health

# Test through Claude Desktop
# Ask Claude: "Remember that the sky is blue"
# Then: "What color is the sky?"
```

## Rollback

If you need to rollback:

```bash
git checkout main
pip install -e .
sekha-mcp
```

**Note**: Also rollback the controller to v1.x to avoid compatibility issues.

## Troubleshooting

### MCP server won't start
- **Check controller is running**: `curl http://localhost:8080/health`
- **Verify API key**: Check `CONTROLLER_API_KEY` in `.env`
- **Check logs**: Look for connection errors in terminal output

### MCP connects but requests fail
- **Controller version mismatch**: Ensure controller is v2.0
- **Provider configuration**: Check controller has at least one provider configured
- **Network issues**: Verify controller URL is accessible from MCP server

### Performance issues
- **Provider selection**: Check controller logs for which provider is being used
- **Circuit breakers**: Check if providers are in open/failed state
- **Timeout settings**: Adjust `request_timeout` in MCP config if needed

## Support

- **Issues**: https://github.com/sekha-ai/sekha-mcp/issues
- **Discussions**: https://github.com/orgs/sekha-ai/discussions
- **Documentation**: See main [V2.0_IMPLEMENTATION_SUMMARY.md](https://github.com/sekha-ai/sekha-docker/blob/feature/v2.0-provider-registry/V2.0_IMPLEMENTATION_SUMMARY.md) in sekha-docker repo

## Changelog

### v2.0.0 (2026-02-04)

#### Added
- Compatibility with Sekha v2.0 multi-provider architecture
- Documentation for v2.0 migration
- Version bumps to indicate v2.0 compatibility

#### Changed
- Updated package version to 2.0.0
- Updated server_version to 2.0.0 in config
- Enhanced configuration documentation

#### Maintained
- All existing MCP API endpoints (no breaking changes)
- Backward compatibility with controller v1.x
- Claude Desktop integration (no config changes needed)

## Next Steps

Once upgraded:

1. **Configure providers** in the controller (see controller documentation)
2. **Test failover** by stopping Ollama and verifying fallback works
3. **Monitor costs** using controller's cost estimation API
4. **Try vision** by sending images in conversations
5. **Experiment with models** by switching embedding/chat models in controller config

Enjoy the new multi-provider capabilities! 🚀
