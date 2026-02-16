# Security Policy

## Supported Versions

We release security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.2.x   | :white_check_mark: |
| 0.1.x   | :white_check_mark: |
| < 0.1   | :x:                |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability in Sekha MCP, please report it responsibly.

### How to Report

**Please do NOT open a public GitHub issue for security vulnerabilities.**

Instead, report vulnerabilities privately:

1. **Email**: Send details to [security@sekha-ai.dev](mailto:security@sekha-ai.dev)
2. **Include**:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### What to Expect

- **Acknowledgment**: Within 48 hours
- **Initial assessment**: Within 1 week
- **Fix timeline**: Depends on severity
  - Critical: 1-7 days
  - High: 1-2 weeks
  - Medium: 2-4 weeks
  - Low: Next release cycle

### Disclosure Policy

We follow coordinated disclosure:

1. You report the vulnerability privately
2. We confirm and develop a fix
3. We release the fix
4. We publicly disclose the vulnerability (with credit to you, if desired)

## Security Best Practices

When using Sekha MCP:

### API Keys
- **Never commit** `CONTROLLER_API_KEY` to version control
- Store credentials in environment variables or secret management systems
- Rotate API keys regularly

### Network Security
- Use HTTPS for Controller connections in production
- Configure firewall rules appropriately
- Limit network access to trusted clients only

### Docker Security
- Use specific version tags, not `:latest`
- Run containers as non-root user (already configured)
- Keep base images updated

### MCP Configuration
- Review MCP client configurations in Claude Desktop/Code
- Ensure `CONTROLLER_URL` points to trusted endpoints
- Monitor MCP tool usage and access logs

## Dependencies

We monitor dependencies for known vulnerabilities:

- Automated updates via Dependabot
- Regular security audits
- Critical patches applied promptly

## Questions?

For general security questions (not vulnerabilities), contact:
- **Email**: [dev@sekha-ai.dev](mailto:dev@sekha-ai.dev)
- **Discord**: [Join our Discord](https://discord.gg/gZb7U9deKH)

Thank you for helping keep Sekha MCP secure! 🔒
