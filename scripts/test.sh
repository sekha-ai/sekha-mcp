#!/bin/bash
set -e

echo "🛠️  Running Sekha MCP Test Suite..."

TEST_TYPE=${1:-"all"}

case $TEST_TYPE in
  "lint")
    echo "🔍 Running linters..."
    ruff check .
    black --check .
    ;;
  "unit")
    echo "Running unit tests..."
    pytest tests/ -v
    ;;
  "all"|*)
    echo "Running linting and all tests..."
    ruff check .
    black --check .
    pytest tests/ -v --cov=src --cov-report=html
    ;;
esac

echo "✅ Tests complete!"