# Build stage
FROM python:3.14-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml README.md ./
COPY src/ ./src/

# Install package
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .

# Runtime stage
FROM python:3.14-slim

LABEL org.opencontainers.image.source="https://github.com/sekha-ai/sekha-mcp"
LABEL org.opencontainers.image.description="Sekha MCP Server - Model Context Protocol for Sekha Memory"
LABEL org.opencontainers.image.licenses="AGPL-3.0"
LABEL org.opencontainers.image.version="0.2.0"

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.14/site-packages /usr/local/lib/python3.14/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Create non-root user
RUN useradd -m -u 1000 sekha && \
    chown -R sekha:sekha /app

USER sekha

# Set environment defaults
ENV CONTROLLER_URL=http://localhost:8080
ENV CONTROLLER_API_KEY=""
ENV LOG_LEVEL=INFO

# Health check (MCP over stdio doesn't expose HTTP, so this is basic)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import sekha_mcp; print('OK')" || exit 1

# Run MCP server
CMD ["python", "-m", "sekha_mcp"]
