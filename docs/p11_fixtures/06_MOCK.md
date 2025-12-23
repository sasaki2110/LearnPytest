# Mock クラスの学習プラン

Pythonの標準ライブラリ `unittest.mock` の `Mock` クラスは、テストでオブジェクトや関数をモック（模倣）するための強力なツールです。フィクスチャと組み合わせることで、テストのセットアップを簡潔にし、再利用性を高めることができます。

**公式ドキュメント**: https://docs.python.org/ja/3/library/unittest.mock.html

## 目次

1. [基本的なモック作成](#基本的なモック作成)
2. [戻り値の設定](#戻り値の設定)
3. [side_effect を使った動的な動作](#side_effect-を使った動的な動作)
4. [呼び出しの検証](#呼び出しの検証)
5. [メソッドのモック](#メソッドのモック)
6. [実際のコードでの使用例（conftest.pyのパターン）](#実際のコードでの使用例conftestpyのパターン)

---

## 基本的なモック作成

`Mock` クラスは、存在しない属性やメソッドにアクセスしてもエラーを発生させません。これにより、テスト対象のオブジェクトの依存関係を簡単に置き換えることができます。

### 基本的な使い方

```python
from unittest.mock import Mock

mock = Mock()
mock.some_method()  # エラーにならない
```

### フィクスチャとしての実装

```python
import pytest
from unittest.mock import Mock

@pytest.fixture
def basic_mock():
    """基本的なモックオブジェクトを返すフィクスチャ"""
    return Mock()

def test_basic_mock(basic_mock):
    """基本的なモックの動作を確認"""
    # 存在しないメソッドを呼び出してもエラーにならない
    result = basic_mock.some_method()
    assert result is not None
    assert isinstance(result, Mock)
```

### 動作の仕組み

- `Mock()` を呼び出すと、任意の属性やメソッドにアクセスできるオブジェクトが作成される
- 存在しないメソッドを呼び出しても、新しい `Mock` オブジェクトが自動的に作成されて返される
- これにより、テスト対象のオブジェクトが依存する外部オブジェクトを簡単に置き換えられる

---

## 戻り値の設定

モックメソッドの戻り値を `return_value` 属性で設定できます。これにより、テストで期待する値を返すようにモックを設定できます。

### 基本的な使い方

```python
mock = Mock()
mock.method.return_value = "Hello"
print(mock.method())  # "Hello" を返す
```

### フィクスチャとしての実装

```python
import pytest
from unittest.mock import Mock

@pytest.fixture
def api_mock():
    """APIクライアントのモック"""
    mock = Mock()
    mock.get.return_value = {"status": "ok", "data": [1, 2, 3]}
    mock.post.return_value = {"id": 123, "created": True}
    return mock

def test_get_data(api_mock):
    """GETリクエストのモックをテスト"""
    result = api_mock.get()
    assert result["status"] == "ok"
    assert len(result["data"]) == 3

def test_post_data(api_mock):
    """POSTリクエストのモックをテスト"""
    result = api_mock.post()
    assert result["id"] == 123
    assert result["created"] is True
```

### ネストした属性の設定

```python
import pytest
from unittest.mock import Mock

@pytest.fixture
def response_mock():
    """HTTPレスポンスのモック"""
    mock = Mock()
    # ネストした属性も設定可能
    mock.json.return_value = {"status": "ok"}
    mock.status_code = 200
    return mock

def test_response(response_mock):
    """ネストした属性のモックをテスト"""
    assert response_mock.json()["status"] == "ok"
    assert response_mock.status_code == 200
```

---

## side_effect を使った動的な動作

`side_effect` を使用すると、メソッドが呼び出されるたびに異なる動作をさせることができます。関数、例外、イテレータなどを設定できます。

### 基本的な使い方

```python
mock = Mock()
mock.method.side_effect = lambda x: x * 2
print(mock.method(5))  # 10 を返す

# 例外を発生させる場合
mock.method.side_effect = ValueError("Error!")
```

### フィクスチャとしての実装

#### 関数を使った動的な動作

```python
import pytest
from unittest.mock import Mock

@pytest.fixture
def calculator_mock():
    """計算機のモック"""
    mock = Mock()
    mock.add.side_effect = lambda x, y: x + y
    mock.multiply.side_effect = lambda x, y: x * y
    return mock

def test_calculator_add(calculator_mock):
    """加算のモックをテスト"""
    result = calculator_mock.add(3, 5)
    assert result == 8

def test_calculator_multiply(calculator_mock):
    """乗算のモックをテスト"""
    result = calculator_mock.multiply(4, 6)
    assert result == 24
```

#### 例外を発生させる場合

```python
import pytest
from unittest.mock import Mock

@pytest.fixture
def error_mock():
    """エラーを発生させるモック"""
    mock = Mock()
    mock.method.side_effect = ValueError("Something went wrong!")
    return mock

def test_error_handling(error_mock):
    """例外が発生することを確認"""
    with pytest.raises(ValueError, match="Something went wrong!"):
        error_mock.method()
```

#### イテレータを使った複数の戻り値

```python
import pytest
from unittest.mock import Mock

@pytest.fixture
def sequence_mock():
    """連続した値を返すモック"""
    mock = Mock()
    mock.get_next.side_effect = [1, 2, 3, StopIteration]
    return mock

def test_sequence(sequence_mock):
    """連続した値を取得"""
    assert sequence_mock.get_next() == 1
    assert sequence_mock.get_next() == 2
    assert sequence_mock.get_next() == 3
```

---

## 呼び出しの検証

モックがどのように呼び出されたかを検証することで、テスト対象のコードが正しく動作していることを確認できます。

### 基本的な使い方

```python
mock = Mock()
mock.method("arg1", "arg2")
mock.method.assert_called_once()  # 1回呼ばれたか確認
mock.method.assert_called_with("arg1", "arg2")  # 引数を確認
```

### フィクスチャとしての実装

```python
import pytest
from unittest.mock import Mock

@pytest.fixture
def logger_mock():
    """ロガーのモック"""
    return Mock()

def test_logging(logger_mock):
    """ログが正しく呼び出されることを確認"""
    logger_mock.info("Test message")
    
    # 1回呼ばれたことを確認
    logger_mock.info.assert_called_once()
    
    # 引数を確認
    logger_mock.info.assert_called_with("Test message")

def test_multiple_calls(logger_mock):
    """複数回の呼び出しを確認"""
    logger_mock.debug("First")
    logger_mock.debug("Second")
    
    # 2回呼ばれたことを確認
    assert logger_mock.debug.call_count == 2
    
    # すべての呼び出しを確認
    logger_mock.debug.assert_any_call("First")
    logger_mock.debug.assert_any_call("Second")
```

### より詳細な検証

```python
import pytest
from unittest.mock import Mock, call

@pytest.fixture
def api_client_mock():
    """APIクライアントのモック"""
    return Mock()

def test_api_calls(api_client_mock):
    """複数のAPI呼び出しを検証"""
    api_client_mock.get("/users")
    api_client_mock.post("/users", json={"name": "Alice"})
    api_client_mock.get("/users/1")
    
    # 呼び出しの順序と引数を確認
    expected_calls = [
        call.get("/users"),
        call.post("/users", json={"name": "Alice"}),
        call.get("/users/1")
    ]
    api_client_mock.assert_has_calls(expected_calls)
```

---

## メソッドのモック

既存のメソッドをカスタム関数で置き換えることができます。これにより、複雑なロジックを持つメソッドを簡単にモックできます。

### 基本的な使い方

```python
mock = Mock()
def custom_method(x):
    return x + 1

mock.add = custom_method
print(mock.add(5))  # 6 を返す
```

### フィクスチャとしての実装

```python
import pytest
from unittest.mock import Mock

def custom_validation(value):
    """カスタムバリデーション関数"""
    if value < 0:
        raise ValueError("Value must be positive")
    return value * 2

@pytest.fixture
def validator_mock():
    """バリデーターのモック"""
    mock = Mock()
    mock.validate = custom_validation
    return mock

def test_validation_success(validator_mock):
    """正常な値のバリデーション"""
    result = validator_mock.validate(5)
    assert result == 10

def test_validation_error(validator_mock):
    """エラーケースのバリデーション"""
    with pytest.raises(ValueError, match="Value must be positive"):
        validator_mock.validate(-1)
```

### クラスのメソッドをモック

```python
import pytest
from unittest.mock import Mock

class Database:
    def connect(self):
        return "Connected"
    
    def query(self, sql):
        return [{"id": 1, "name": "Alice"}]

@pytest.fixture
def database_mock():
    """データベースのモック"""
    mock = Mock(spec=Database)
    
    # メソッドをカスタム関数で置き換え
    def mock_query(sql):
        if "SELECT" in sql:
            return [{"id": 1, "name": "Test User"}]
        return []
    
    mock.query = mock_query
    mock.connect.return_value = "Mock Connected"
    return mock

def test_database_query(database_mock):
    """データベースクエリのモックをテスト"""
    result = database_mock.query("SELECT * FROM users")
    assert len(result) == 1
    assert result[0]["name"] == "Test User"
```

---

## 実際のコードでの使用例（conftest.pyのパターン）

実際のプロジェクトでは、`conftest.py` にフィクスチャを定義して、複数のテストファイルで共有することが一般的です。

### conftest.py での定義

```python
# conftest.py
import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_client():
    """クライアントのモック"""
    mock = Mock()
    
    def bind_tools(tools):
        """ツールをバインドする関数"""
        bound_mock = Mock()
        bound_mock.invoke.side_effect = lambda messages: {
            "content": "Mock response",
            "tool_calls": []
        }
        return bound_mock
    
    mock.bind_tools = bind_tools
    return mock
```

### テストファイルでの使用

```python
# test_example.py
def test_with_mock_client(mock_client):
    """モッククライアントを使用したテスト"""
    bound_client = mock_client.bind_tools(["tool1", "tool2"])
    result = bound_client.invoke([{"role": "user", "content": "Hello"}])
    
    assert result["content"] == "Mock response"
    assert "tool_calls" in result
```

### より実践的な例：APIクライアントのモック

```python
# conftest.py
import pytest
from unittest.mock import Mock

@pytest.fixture
def api_client_mock():
    """APIクライアントのモックフィクスチャ"""
    mock = Mock()
    
    # GETリクエストのモック
    def mock_get(url, params=None):
        response_mock = Mock()
        if url == "/api/users":
            response_mock.json.return_value = {
                "users": [
                    {"id": 1, "name": "Alice"},
                    {"id": 2, "name": "Bob"}
                ]
            }
            response_mock.status_code = 200
        else:
            response_mock.json.return_value = {"error": "Not found"}
            response_mock.status_code = 404
        return response_mock
    
    # POSTリクエストのモック
    def mock_post(url, json_data=None):
        response_mock = Mock()
        response_mock.json.return_value = {
            "id": 123,
            "created": True,
            **json_data
        }
        response_mock.status_code = 201
        return response_mock
    
    mock.get = mock_get
    mock.post = mock_post
    return mock
```

```python
# test_api.py
def test_get_users(api_client_mock):
    """ユーザー一覧の取得をテスト"""
    response = api_client_mock.get("/api/users")
    users = response.json()["users"]
    
    assert response.status_code == 200
    assert len(users) == 2
    assert users[0]["name"] == "Alice"

def test_create_user(api_client_mock):
    """ユーザーの作成をテスト"""
    user_data = {"name": "Charlie", "email": "charlie@example.com"}
    response = api_client_mock.post("/api/users", json_data=user_data)
    
    assert response.status_code == 201
    assert response.json()["id"] == 123
    assert response.json()["created"] is True
    assert response.json()["name"] == "Charlie"
```

### パラメータ化されたモックフィクスチャ

```python
# conftest.py
import pytest
from unittest.mock import Mock

@pytest.fixture
def configurable_mock(request):
    """設定可能なモックフィクスチャ"""
    mock = Mock()
    
    # パラメータから設定を取得
    return_value = getattr(request, "param", "default")
    mock.method.return_value = return_value
    
    return mock

# パラメータ化されたテスト
@pytest.mark.parametrize("configurable_mock", ["value1", "value2", "value3"], indirect=True)
def test_configurable_mock(configurable_mock):
    """設定可能なモックをテスト"""
    result = configurable_mock.method()
    assert result in ["value1", "value2", "value3"]
```

---

## まとめ

`unittest.mock` の `Mock` クラスをフィクスチャと組み合わせることで、以下のメリットが得られます：

1. **再利用性**: 同じモック設定を複数のテストで使用できる
2. **保守性**: モックの設定を1箇所に集約できる
3. **可読性**: テストコードがシンプルで理解しやすくなる
4. **柔軟性**: `side_effect` や `return_value` で様々な動作をシミュレートできる

フィクスチャとモックを組み合わせることで、より堅牢で保守しやすいテストコードを書くことができます。

