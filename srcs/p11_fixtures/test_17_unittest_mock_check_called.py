"""
呼び出しの検証を示します。
"""

import pytest
from unittest.mock import Mock, call

@pytest.fixture
def logger():
    """ロガーのモック"""
    return Mock()

def test_logging(logger):
    """ログが正しく呼び出されることを確認"""
    logger.info("Test message")
    
    # 1回呼ばれたことを確認
    logger.info.assert_called_once()
    
    # 引数を確認
    logger.info.assert_called_with("Test message")

def test_multiple_calls(logger):
    """複数回の呼び出しを確認"""
    logger.debug("First")
    logger.debug("Second")
    
    # 2回呼ばれたことを確認
    assert logger.debug.call_count == 2
    
    # すべての呼び出しを確認
    logger.debug.assert_any_call("First")
    logger.debug.assert_any_call("Second")

"""
複数のAPI呼び出しを検証するモックを示します。
"""

@pytest.fixture
def api_client():
    """APIクライアントのモック"""
    return Mock()

def test_api_calls(api_client):
    """複数のAPI呼び出しを検証"""
    api_client.get("/users")
    api_client.post("/users", json={"name": "Alice"})
    api_client.get("/users/1")
    
    # 呼び出しの順序と引数を確認
    expected_calls = [
        call.get("/users"),
        call.post("/users", json={"name": "Alice"}),
        call.get("/users/1")
    ]
    api_client.assert_has_calls(expected_calls)