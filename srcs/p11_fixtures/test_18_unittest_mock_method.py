"""
関数のメソッドをモックする方法を示します。
"""

import pytest
from unittest.mock import Mock

"""
関数のメソッドをモックする方法を示します。
"""
def custom_validation(value):
    """カスタムバリデーション関数"""
    if value < 0:
        raise ValueError("Value must be positive")
    return value * 2

@pytest.fixture
def validator():
    """
    mock.add.side_effect = lambda x, y: x + y
    より複雑なカスタム関数を使うことができる。
    """
    mock = Mock()
    mock.validate = custom_validation
    return mock

def test_validation_success(validator):
    """正常な値のバリデーション"""
    result = validator.validate(5)
    assert result == 10

def test_validation_error(validator):
    """エラーケースのバリデーション"""
    with pytest.raises(ValueError, match="Value must be positive"):
        validator.validate(-1)


"""
クラスのメソッドをモックする方法を示します。
"""
class Database:
    def connect(self):
        return "Connected" # specで保証されるのはメソッド名だけで、メソッドの中身は利用されない。
    
    def query(self, sql):
        return [{"id": 1, "name": "Alice"}] # specで保証されるのはメソッド名だけで、メソッドの中身は利用されない。

@pytest.fixture
def database():
    """
    spec=クラス名 は、クラスのメソッドをモックし、メソッドが存在しない場合はエラーを発生させる。
    これは、テスト対象のクラスが存在することを保証するために使用する。

    # spec なしの場合
    mock1 = Mock()
    mock1.connect()  # ✅ OK
    mock1.unknown_method()  # ✅ OK（エラーにならない）

    # spec ありの場合
    mock2 = Mock(spec=Database)
    mock2.connect()  # ✅ OK（Database に存在する）
    mock2.query("SELECT *")  # ✅ OK（Database に存在する）
    mock2.unknown_method()  # ❌ AttributeError（Database に存在しない）

    specで保証されるのはメソッド名だけで、メソッドの中身は利用されない。
    """

    mock = Mock(spec=Database)
    
    # メソッドをカスタム関数で置き換え
    def mock_query(sql):
        if "SELECT" in sql:
            return [{"id": 1, "name": "Test User"}]
        return []
    
    mock.query = mock_query
    mock.connect.return_value = "Mock Connected"
    return mock

def test_database_query(database):
    """データベースクエリのモックをテスト"""
    result = database.query("SELECT * FROM users")
    assert len(result) == 1
    assert result[0]["name"] == "Test User"