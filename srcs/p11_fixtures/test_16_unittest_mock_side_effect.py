"""
side_effect を使った動的な動作を示します。
"""

import pytest
from unittest.mock import Mock

"""
関数を使った動的な動作を示します。
"""
@pytest.fixture
def calculator():
    """計算機のモック"""
    mock = Mock()
    # Mockメソッドの戻り値を関数で設定する。
    mock.add.side_effect = lambda x, y: x + y
    mock.multiply.side_effect = lambda x, y: x * y
    return mock

def test_calculator_add(calculator):
    """加算のモックをテスト"""
    result = calculator.add(3, 5)
    assert result == 8

def test_calculator_multiply(calculator):
    """乗算のモックをテスト"""
    result = calculator.multiply(4, 6)
    assert result == 24

"""
例外を発生させるモックを作成します。
"""
@pytest.fixture
def error():
    """エラーを発生させるモック"""
    mock = Mock()
    mock.method.side_effect = ValueError("Something went wrong!")
    return mock

def test_error_handling(error):
    """例外が発生することを確認"""
    with pytest.raises(ValueError, match="Something went wrong!"):
        error.method()

"""
イテレータを使った動的な動作をするモックを示します。
"""
@pytest.fixture
def sequence():
    """連続した値を返すモック"""
    mock = Mock()
    # Mockメソッドの戻り値をイテレータで設定する。
    mock.get_next.side_effect = [1, 2, 3, StopIteration]
    return mock

def test_sequence(sequence):
    """連続した値を取得"""
    assert sequence.get_next() == 1
    assert sequence.get_next() == 2
    assert sequence.get_next() == 3