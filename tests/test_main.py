"""Minimal tests for main.py - verify structure only, never execute"""

import os

import pytest


def test_main_file_exists():
    """Verify main.py file exists at correct location"""
    main_path = "src/sekha_mcp/main.py"
    assert os.path.exists(main_path), f"main.py should exist at {main_path}"


def test_main_has_correct_structure():
    """Verify main.py has expected structure without importing or running"""
    with open("src/sekha_mcp/main.py") as f:
        content = f.read()

    # Check for expected imports
    assert "from .server import main" in content, "Should import main from server"
    assert "import asyncio" in content or "from asyncio" in content

    # Check for __main__ block
    assert 'if __name__ == "__main__"' in content
    assert "main()" in content  # Should call main()


def test_main_can_be_imported():
    """Test that main module can be imported without running it"""
    try:
        import sekha_mcp.main as main_module

        assert hasattr(main_module, "main")
        # Don't call the function, just verify it exists
    except Exception as e:
        pytest.fail(f"Should be able to import main module: {e}")


def test_server_import_works():
    """Verify we can import server module (the real main function)"""
    try:
        from sekha_mcp.server import main

        assert callable(main)
    except Exception as e:
        pytest.fail(f"Should be able to import server.main: {e}")


@pytest.mark.asyncio
async def test_main_is_coroutine():
    """Test that main is an async function"""
    import inspect

    from sekha_mcp.server import main

    assert inspect.iscoroutinefunction(main)
