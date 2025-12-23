import pytest
from unittest.mock import Mock

@pytest.fixture
def basic_mock():
    """基本的なモックオブジェクトを返すフィクスチャ"""
    return Mock()

def test_basic_mock(basic_mock):
    """基本的なモックの動作を確認"""
    # 存在しないメソッドを呼び出してもエラーにならない
    # これにより、便利にフィクスチャでモックを利用できる。
    result = basic_mock.some_method()
    print("")
    print(f"basic_mock.some_method() の結果: {result}")
    print(f"result の型: {type(result)}")
    assert result is not None
    assert isinstance(result, Mock)

    # Mockメソッドの戻り値もMockオブジェクトになる。
    # これにより、モックメソッドをネストして利用できる。
    result2 = result.some_method2()
    print("")
    print(f"result2.some_method2() の結果: {result2}")
    print(f"result2 の型: {type(result2)}")
    assert result2 is not None
    assert isinstance(result2, Mock)