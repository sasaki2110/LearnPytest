# How to use fixtures

pytestのフィクスチャ（fixture）は、テストの前後に共通のセットアップやクリーンアップ処理を行うための強力な機能です。これにより、コードの重複を排除し、テストの可読性と保守性を向上させることができます。

**公式ドキュメント**: https://docs.pytest.org/en/stable/how-to/fixtures.html

## 目次

1. [フィクスチャとは](#フィクスチャとは)
2. [基本的な使い方](#基本的な使い方)
3. [フィクスチャのスコープ](#フィクスチャのスコープ)
4. [フィクスチャの依存関係](#フィクスチャの依存関係)
5. [フィクスチャの自動使用（autouse）](#フィクスチャの自動使用autouse)
6. [フィクスチャの共有（conftest.py）](#フィクスチャの共有conftestpy)
7. [フィクスチャのクリーンアップ（yield）](#フィクスチャのクリーンアップyield)
8. [パラメータ化されたフィクスチャ](#パラメータ化されたフィクスチャ)
9. [組み込みフィクスチャ](#組み込みフィクスチャ)
10. [実践的な例](#実践的な例)

---

## フィクスチャとは

フィクスチャは、テスト関数に依存性を注入するためのメカニズムです。テストで必要なデータ、オブジェクト、リソースなどを提供し、テストの前後で必要な処理を実行できます。

### フィクスチャの主な利点

- **コードの重複排除**: 共通のセットアップ処理を1箇所に集約
- **テストの独立性**: 各テストが独立した環境で実行される
- **保守性の向上**: セットアップロジックの変更が容易
- **可読性の向上**: テストコードがシンプルで理解しやすくなる

---

## 基本的な使い方

フィクスチャは `@pytest.fixture` デコレーターを使用して定義します。

### シンプルな例

```python
import pytest

@pytest.fixture
def sample_data():
    """テスト用のサンプルデータを返すフィクスチャ"""
    return [1, 2, 3, 4, 5]

def test_sum(sample_data):
    """sample_dataフィクスチャを使用してテストを実行"""
    assert sum(sample_data) == 15

def test_length(sample_data):
    """同じフィクスチャを別のテストで使用"""
    assert len(sample_data) == 5
```

### 動作の仕組み

1. `@pytest.fixture` デコレーターが関数をフィクスチャとして登録
2. テスト関数の引数にフィクスチャ名を指定すると、pytestが自動的にフィクスチャを実行
3. フィクスチャの戻り値がテスト関数の引数として渡される

---

## フィクスチャのスコープ

フィクスチャのスコープを指定することで、どの範囲でフィクスチャが有効かを制御できます。スコープには以下の種類があります。

| スコープ | 説明 | 使用例 |
|---------|------|--------|
| `function` | 各テスト関数ごとに新しいフィクスチャが作成される（デフォルト） | テストごとに独立したデータが必要な場合 |
| `class` | クラス内のすべてのテストメソッドで同じフィクスチャが使用される | クラス内のテストで共有リソースが必要な場合 |
| `module` | モジュール内のすべてのテストで同じフィクスチャが使用される | モジュール全体で共有する設定やリソース |
| `package` | パッケージ内のすべてのテストで同じフィクスチャが使用される | パッケージ全体で共有する設定 |
| `session` | テストセッション全体で同じフィクスチャが使用される | データベース接続など、セッション全体で共有するリソース |

### スコープの例

```python
import pytest

@pytest.fixture(scope="function")
def function_scope_data():
    """各テストごとに新しいデータが作成される"""
    return {"counter": 0}

@pytest.fixture(scope="module")
def module_scope_data():
    """モジュール内のすべてのテストで同じデータが使用される"""
    return {"shared_counter": 0}

def test_function_scope_1(function_scope_data):
    function_scope_data["counter"] += 1
    assert function_scope_data["counter"] == 1

def test_function_scope_2(function_scope_data):
    # 新しいインスタンスなので、counterは0から始まる
    function_scope_data["counter"] += 1
    assert function_scope_data["counter"] == 1

def test_module_scope_1(module_scope_data):
    module_scope_data["shared_counter"] += 1
    assert module_scope_data["shared_counter"] == 1

def test_module_scope_2(module_scope_data):
    # 同じインスタンスなので、前のテストの値が残っている
    module_scope_data["shared_counter"] += 1
    assert module_scope_data["shared_counter"] == 2
```

---

## フィクスチャの依存関係

フィクスチャは他のフィクスチャを依存関係として持つことができます。これにより、複雑なセットアップを分割して管理できます。

### 基本的な依存関係

```python
import pytest

@pytest.fixture
def user_data():
    """ユーザーデータを返すフィクスチャ"""
    return {"name": "Alice", "age": 30, "email": "alice@example.com"}

@pytest.fixture
def user(user_data):
    """user_dataフィクスチャに依存してUserオブジェクトを作成"""
    from dataclasses import dataclass
    
    @dataclass
    class User:
        name: str
        age: int
        email: str
    
    return User(**user_data)

def test_user_creation(user):
    """userフィクスチャを使用（内部的にuser_dataも使用される）"""
    assert user.name == "Alice"
    assert user.age == 30
```

### 複数の依存関係

```python
import pytest

@pytest.fixture
def database():
    """データベース接続を返すフィクスチャ"""
    return {"connected": True}

@pytest.fixture
def user_data():
    """ユーザーデータを返すフィクスチャ"""
    return {"name": "Bob", "age": 25}

@pytest.fixture
def user_with_db(database, user_data):
    """複数のフィクスチャに依存"""
    # databaseとuser_dataの両方を使用
    return {
        "database": database,
        "user": user_data
    }

def test_user_with_db(user_with_db):
    assert user_with_db["database"]["connected"] is True
    assert user_with_db["user"]["name"] == "Bob"
```

---

## フィクスチャの自動使用（autouse）

`autouse=True` を指定することで、テスト関数で明示的に指定しなくても自動的にフィクスチャが適用されます。

### autouseの例

```python
import pytest

@pytest.fixture(autouse=True)
def setup_logging():
    """すべてのテストで自動的にログ設定を実行"""
    import logging
    logging.basicConfig(level=logging.INFO)
    print("ログ設定が完了しました")

@pytest.fixture(autouse=True)
def reset_counter():
    """テストごとにカウンターをリセット"""
    print("カウンターをリセット")
    yield
    print("テスト終了後のクリーンアップ")

def test_example_1():
    """autouseフィクスチャが自動的に適用される"""
    assert True

def test_example_2():
    """こちらも自動的に適用される"""
    assert True
```

### autouseの注意点

- すべてのテストに適用されるため、パフォーマンスに影響する可能性がある
- 明示的に指定しないため、テストコードから依存関係が見えにくくなる
- 必要な場合のみ使用することを推奨

---

## フィクスチャの共有（conftest.py）

複数のテストファイルでフィクスチャを共有する場合、`conftest.py` ファイルにフィクスチャを定義します。

### conftest.pyの構造

```
project/
├── conftest.py          # プロジェクト全体で共有
├── tests/
│   ├── conftest.py      # testsディレクトリ内で共有
│   ├── test_module1.py
│   └── test_module2.py
└── tests/integration/
    ├── conftest.py      # integrationディレクトリ内で共有
    └── test_integration.py
```

### conftest.pyの例

```python
# conftest.py
import pytest

@pytest.fixture
def shared_resource():
    """プロジェクト全体で共有されるリソース"""
    return {"resource_id": 12345}

@pytest.fixture(scope="session")
def database_connection():
    """セッション全体で共有されるデータベース接続"""
    # データベース接続のセットアップ
    conn = {"connected": True, "host": "localhost"}
    yield conn
    # クリーンアップ
    conn["connected"] = False
```

### テストファイルでの使用

```python
# test_module1.py
def test_with_shared_resource(shared_resource):
    """conftest.pyで定義されたフィクスチャを使用"""
    assert shared_resource["resource_id"] == 12345

# test_module2.py
def test_with_database(database_connection):
    """同じくconftest.pyのフィクスチャを使用"""
    assert database_connection["connected"] is True
```

---

## フィクスチャのクリーンアップ（yield）

フィクスチャで `yield` を使用することで、テスト実行後のクリーンアップ処理を記述できます。

### yieldの基本的な使い方

```python
import pytest

@pytest.fixture
def temporary_file():
    """一時ファイルを作成し、テスト後に削除"""
    import tempfile
    import os
    
    # セットアップ: 一時ファイルを作成
    temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w')
    temp_file.write("test data")
    temp_file.close()
    
    yield temp_file.name  # テストにファイル名を提供
    
    # クリーンアップ: ファイルを削除
    if os.path.exists(temp_file.name):
        os.remove(temp_file.name)
        print(f"一時ファイル {temp_file.name} を削除しました")

def test_file_operations(temporary_file):
    """一時ファイルを使用してテスト"""
    with open(temporary_file, 'r') as f:
        content = f.read()
    assert content == "test data"
```

### 複数のクリーンアップ処理

```python
import pytest

@pytest.fixture
def complex_setup():
    """複数のリソースをセットアップし、順番にクリーンアップ"""
    resources = []
    
    # リソース1のセットアップ
    resource1 = {"type": "database", "id": 1}
    resources.append(resource1)
    
    # リソース2のセットアップ
    resource2 = {"type": "cache", "id": 2}
    resources.append(resource2)
    
    yield resources
    
    # クリーンアップ（逆順）
    for resource in reversed(resources):
        print(f"リソース {resource['id']} をクリーンアップ")
        resource["active"] = False
```

### try-finallyとの比較

`yield` の代わりに `try-finally` を使用することもできますが、`yield` の方が推奨されます。

```python
import pytest

@pytest.fixture
def setup_with_try_finally():
    """try-finallyを使用した例（yieldの方が推奨）"""
    resource = {"active": True}
    try:
        yield resource
    finally:
        resource["active"] = False
        print("クリーンアップ完了")
```

---

## パラメータ化されたフィクスチャ

フィクスチャをパラメータ化することで、同じフィクスチャを異なる値で複数回実行できます。

### 基本的なパラメータ化

```python
import pytest

@pytest.fixture(params=["chrome", "firefox", "safari"])
def browser(request):
    """異なるブラウザでテストを実行"""
    browser_name = request.param
    print(f"ブラウザ {browser_name} でテストを実行")
    return browser_name

def test_browser_compatibility(browser):
    """パラメータ化されたフィクスチャを使用"""
    assert browser in ["chrome", "firefox", "safari"]
```

### 複数のパラメータの組み合わせ

```python
import pytest

@pytest.fixture(params=[("admin", "admin123"), ("user", "user123")])
def credentials(request):
    """異なる認証情報でテストを実行"""
    username, password = request.param
    return {"username": username, "password": password}

def test_login(credentials):
    """認証情報を使用してテスト"""
    assert credentials["username"] in ["admin", "user"]
    assert "123" in credentials["password"]
```

### パラメータ化フィクスチャの依存関係

```python
import pytest

@pytest.fixture(params=["sqlite", "postgresql"])
def database_type(request):
    return request.param

@pytest.fixture
def database_connection(database_type):
    """パラメータ化されたフィクスチャに依存"""
    if database_type == "sqlite":
        return {"type": "sqlite", "connection": "sqlite:///test.db"}
    elif database_type == "postgresql":
        return {"type": "postgresql", "connection": "postgresql://localhost/test"}

def test_database_operations(database_connection):
    """異なるデータベースタイプでテスト"""
    assert database_connection["type"] in ["sqlite", "postgresql"]
```

---

## 組み込みフィクスチャ

pytestには、よく使用される機能を提供する組み込みフィクスチャが用意されています。

### 主な組み込みフィクスチャ

| フィクスチャ | 説明 | 使用例 |
|------------|------|--------|
| `tmp_path` | 一時ディレクトリのパス（Pathオブジェクト） | テスト用の一時ファイルを作成 |
| `tmp_path_factory` | セッションスコープの一時ディレクトリファクトリ | セッション全体で共有する一時ディレクトリ |
| `tmpdir` | 一時ディレクトリのパス（str、レガシー） | 後方互換性のため（tmp_pathを推奨） |
| `monkeypatch` | テスト中に環境変数や属性を変更 | モックやスタブの設定 |
| `capsys` | 標準出力・標準エラー出力をキャプチャ | 出力の検証 |
| `capfd` | ファイルディスクリプタ経由で出力をキャプチャ | 低レベルな出力の検証 |
| `request` | テストの実行コンテキスト情報 | フィクスチャ内でテスト情報を取得 |

### tmp_pathの例

```python
def test_file_creation(tmp_path):
    """一時ディレクトリにファイルを作成"""
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello, pytest!")
    
    assert test_file.exists()
    assert test_file.read_text() == "Hello, pytest!"
```

### monkeypatchの例

```python
def test_environment_variable(monkeypatch):
    """環境変数を一時的に変更"""
    monkeypatch.setenv("API_KEY", "test_key")
    
    import os
    assert os.getenv("API_KEY") == "test_key"

def test_function_mock(monkeypatch):
    """関数をモック"""
    def mock_function():
        return "mocked"
    
    monkeypatch.setattr("module.function", mock_function)
    # テストを実行
```

### capsysの例

```python
def test_print_output(capsys):
    """標準出力をキャプチャ"""
    print("Hello, pytest!")
    captured = capsys.readouterr()
    
    assert captured.out == "Hello, pytest!\n"
```

---

## 実践的な例

### 例1: データベース接続のフィクスチャ

```python
import pytest

@pytest.fixture(scope="module")
def db_connection():
    """モジュール全体で共有されるデータベース接続"""
    # データベース接続のセットアップ
    connection = {
        "host": "localhost",
        "port": 5432,
        "database": "test_db",
        "connected": True
    }
    
    print("データベースに接続しました")
    
    yield connection
    
    # クリーンアップ
    connection["connected"] = False
    print("データベース接続を閉じました")

@pytest.fixture
def test_user(db_connection):
    """データベースにテストユーザーを作成"""
    user = {
        "id": 1,
        "name": "Test User",
        "email": "test@example.com"
    }
    # データベースにユーザーを挿入（実際の実装ではDB操作）
    print(f"テストユーザー {user['name']} を作成しました")
    
    yield user
    
    # クリーンアップ: テストユーザーを削除
    print(f"テストユーザー {user['name']} を削除しました")

def test_user_operations(test_user, db_connection):
    """データベース接続とテストユーザーを使用"""
    assert db_connection["connected"] is True
    assert test_user["name"] == "Test User"
```

### 例2: APIクライアントのフィクスチャ

```python
import pytest
import requests
from unittest.mock import Mock

@pytest.fixture
def api_client():
    """APIクライアントのモック"""
    client = Mock()
    client.get.return_value.json.return_value = {"status": "ok"}
    client.post.return_value.json.return_value = {"id": 123}
    return client

@pytest.fixture
def authenticated_api_client(api_client):
    """認証済みAPIクライアント"""
    api_client.headers = {"Authorization": "Bearer token123"}
    return api_client

def test_get_data(authenticated_api_client):
    """認証済みクライアントでデータを取得"""
    response = authenticated_api_client.get("/api/data")
    assert response.json()["status"] == "ok"
```

### 例3: 設定ファイルのフィクスチャ

```python
import pytest
import json
from pathlib import Path

@pytest.fixture
def config_file(tmp_path):
    """一時的な設定ファイルを作成"""
    config = {
        "app_name": "Test App",
        "debug": True,
        "database": {
            "host": "localhost",
            "port": 5432
        }
    }
    
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps(config))
    
    return config_path

@pytest.fixture
def app_config(config_file):
    """設定ファイルを読み込む"""
    with open(config_file, 'r') as f:
        return json.load(f)

def test_app_config(app_config):
    """設定を検証"""
    assert app_config["app_name"] == "Test App"
    assert app_config["debug"] is True
    assert app_config["database"]["host"] == "localhost"
```

---

## ベストプラクティス

1. **適切なスコープを選択**: 必要最小限のスコープを使用してパフォーマンスを最適化
2. **conftest.pyで共有**: 複数のテストで使用するフィクスチャは `conftest.py` に配置
3. **明確な名前付け**: フィクスチャの目的が明確になるような名前を付ける
4. **クリーンアップの確実な実行**: `yield` を使用してリソースのクリーンアップを保証
5. **依存関係の最小化**: フィクスチャの依存関係を最小限に保つ
6. **autouseの慎重な使用**: 必要な場合のみ `autouse=True` を使用

---

## まとめ

pytestのフィクスチャは、テストコードの品質を大幅に向上させる強力な機能です。基本的な使い方から、スコープ、依存関係、パラメータ化、クリーンアップまで、様々な機能を適切に組み合わせることで、保守性の高いテストコードを書くことができます。

### 次のステップ

- [About fixtures](https://docs.pytest.org/en/stable/explanation/fixtures.html#about-fixtures) - フィクスチャの概念と設計思想
- [How to parametrize fixtures and test functions](https://docs.pytest.org/en/stable/how-to/parametrize.html) - フィクスチャのパラメータ化の詳細
- [Fixtures reference](https://docs.pytest.org/en/stable/reference/fixtures.html#reference-fixtures) - フィクスチャのAPIリファレンス

