# Changelog

All notable changes to the Sekha MCP Server will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-02-04

### Added
- Compatible with Sekha v0.2.0 multi-provider architecture
- Support for vision models (images in conversations via GPT-4o, Kimi 2.5)
- Multi-dimensional embedding support (per-dimension ChromaDB collections)
- Provider statistics in `memory_stats` tool
- Explicit Claude Code documentation and examples
- Ollama + Sekha workflow guide
- Claude Desktop and Claude Code support documentation
- Automatic provider fallback (Ollama, OpenAI, Anthropic, etc.)
- Cost-aware model selection

### Changed
- Version bumped to 0.2.0
- Updated documentation for v0.2.0 features
- Clarified MCP works with any compatible client
- Enhanced README with comprehensive setup guides

### Maintained
- Full backward compatibility with v1.x API
- No breaking changes to MCP tools
- Works with both v0.1.x and v0.2.0 controllers

## [0.1.0] - 2025

### Added
- Initial release with 7 MCP tools:
  - `memory_store` - Save conversations
  - `memory_search` - Semantic search
  - `memory_get_context` - Retrieve relevant context
  - `memory_update` - Update conversation metadata
  - `memory_prune` - Get cleanup recommendations
  - `memory_export` - Export your data
  - `memory_stats` - View usage statistics
- Claude Desktop integration
- Basic memory operations
- Docker container support
- Standard MCP protocol implementation
- AGPL-3.0-or-later license

[0.2.0]: https://github.com/sekha-ai/sekha-mcp/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/sekha-ai/sekha-mcp/releases/tag/v0.1.0
