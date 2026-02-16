# Contributing to Sekha MCP

Thank you for your interest in contributing to Sekha MCP! We welcome contributions from the community.

## How to Contribute

### Reporting Issues

- Use the [GitHub issue tracker](https://github.com/sekha-ai/sekha-mcp/issues)
- Search existing issues before creating a new one
- Include relevant details: version, environment, reproduction steps

### Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/YOUR-USERNAME/sekha-mcp.git
   cd sekha-mcp
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add tests for new functionality
   - Update documentation as needed

4. **Run tests**
   ```bash
   pytest
   pytest --cov=sekha_mcp --cov-report=html
   ```

5. **Format and lint**
   ```bash
   black .
   ruff check .
   ```

6. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

   Use conventional commits format:
   - `feat:` - New features
   - `fix:` - Bug fixes
   - `docs:` - Documentation changes
   - `test:` - Test additions/changes
   - `refactor:` - Code refactoring
   - `chore:` - Build/tooling changes

7. **Push and create a pull request**
   ```bash
   git push origin feature/your-feature-name
   ```

### Development Setup

```bash
# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=sekha_mcp --cov-report=html
```

### Code Style

- **Python**: Follow PEP 8
- **Line length**: 100 characters
- **Formatter**: Black
- **Linter**: Ruff
- **Type hints**: Encouraged but not required

### Testing Guidelines

- Write unit tests for new functionality
- Maintain test coverage above 85%
- Use pytest fixtures for common test setup
- Mock external dependencies (Controller API)

### Documentation

- Update README.md for user-facing changes
- Add docstrings to new functions/classes
- Update CHANGELOG.md following Keep a Changelog format

### Review Process

1. Maintainers will review your PR
2. Address feedback and requested changes
3. Once approved, your PR will be merged

## Development Resources

- **MCP Protocol**: [Model Context Protocol Docs](https://modelcontextprotocol.io/)
- **Sekha Docs**: [docs.sekha.dev](https://docs.sekha.dev)
- **Architecture**: [Architecture Overview](https://docs.sekha.dev/architecture/overview/)

## Questions?

- **Discord**: [Join our Discord](https://discord.gg/gZb7U9deKH)
- **Email**: [dev@sekha-ai.dev](mailto:dev@sekha-ai.dev)

Thank you for contributing! 🎉
