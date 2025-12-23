"""
モックメソッドの戻り値を設定する方法を示します。
"""

import pytest
from unittest.mock import Mock

@pytest.fixture
def api_mock():
    """APIクライアントのモック"""
    mock = Mock()
    """メソッド毎に戻り値を設定する。"""
    # getメソッドの戻り値を設定する。
    mock.get.return_value = {"status": "ok", "data": [1, 2, 3]}
    # postメソッドの戻り値を設定する。
    mock.post.return_value = {"id": 123, "created": True}
    return mock

def test_get_data(api_mock):
    """GETリクエストのモックをテスト"""
    result = api_mock.get()
    print("")
    print(f"api_mock.get() の結果: {result}")
    print(f"result の型: {type(result)}")
    assert result["status"] == "ok"
    assert len(result["data"]) == 3

def test_post_data(api_mock):
    """POSTリクエストのモックをテスト"""
    result = api_mock.post()
    print("")
    print(f"api_mock.post() の結果: {result}")
    print(f"result の型: {type(result)}")
    assert result["id"] == 123
    assert result["created"] is True