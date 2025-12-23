# How to parametrize fixtures and test functions

pytestのパラメータ化機能を使用することで、同じテストロジックを異なる入力値で複数回実行できます。これにより、テストコードの重複を排除し、網羅的なテストを効率的に記述できます。

**公式ドキュメント**: https://docs.pytest.org/en/stable/how-to/parametrize.html

## 目次

1. [パラメータ化とは](#パラメータ化とは)
2. [テスト関数のパラメータ化](#テスト関数のパラメータ化)
3. [フィクスチャのパラメータ化](#フィクスチャのパラメータ化)
4. [パラメータ化の組み合わせ](#パラメータ化の組み合わせ)
5. [パラメータ化の高度な使い方](#パラメータ化の高度な使い方)
6. [パラメータ化のベストプラクティス](#パラメータ化のベストプラクティス)
7. [実践的な例](#実践的な例)
8. [まとめ](#まとめ)

---

## パラメータ化とは

### パラメータ化の目的

パラメータ化は、**同じテストロジックを異なる入力値で実行**するためのメカニズムです。これにより：

- **コードの重複を排除**: 同じロジックを複数のテスト関数に書く必要がない
- **網羅的なテスト**: 様々な入力値でテストを実行できる
- **保守性の向上**: テストロジックの変更が1箇所で済む
- **テストの可読性**: テストケースが明確に列挙される

### パラメータ化の種類

pytestでは、以下の2つの方法でパラメータ化できます：

1. **テスト関数のパラメータ化**: `@pytest.mark.parametrize` を使用
2. **フィクスチャのパラメータ化**: `@pytest.fixture(params=...)` を使用

---

## テスト関数のパラメータ化

### 基本的な使い方

`@pytest.mark.parametrize` デコレーターを使用して、テスト関数をパラメータ化します。

```python
import pytest

@pytest.mark.parametrize("input_value,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_multiply_by_two(input_value, expected):
    """入力値を2倍する関数のテスト"""
    result = input_value * 2
    assert result == expected
```

このテストは、3つの異なる入力値で実行されます：
- `input_value=1, expected=2`
- `input_value=2, expected=4`
- `input_value=3, expected=6`

### パラメータ名の指定

パラメータ名は、カンマ区切りの文字列で指定します。

```python
@pytest.mark.parametrize("x,y,expected", [
    (1, 2, 3),
    (2, 3, 5),
    (5, 7, 12),
])
def test_add(x, y, expected):
    """加算のテスト"""
    assert x + y == expected
```

### 単一パラメータのパラメータ化

パラメータが1つだけの場合も、同様に記述できます。

```python
@pytest.mark.parametrize("number", [1, 2, 3, 4, 5])
def test_is_positive(number):
    """正の数かどうかをテスト"""
    assert number > 0
```

### パラメータ化の実行結果

パラメータ化されたテストは、各パラメータの組み合わせごとに**別々のテストケース**として実行されます。

```bash
# 実行結果の例
test_example.py::test_multiply_by_two[1-2] PASSED
test_example.py::test_multiply_by_two[2-4] PASSED
test_example.py::test_multiply_by_two[3-6] PASSED
```

---

## フィクスチャのパラメータ化

### 基本的な使い方

フィクスチャをパラメータ化するには、`@pytest.fixture` デコレーターの `params` 引数を使用します。

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

このテストは、3つの異なるブラウザで実行されます。

### request.param の使用

パラメータ化されたフィクスチャ内では、`request.param` で現在のパラメータ値にアクセスできます。

```python
@pytest.fixture(params=[("admin", "admin123"), ("user", "user123")])
def credentials(request):
    """異なる認証情報でテストを実行"""
    username, password = request.param
    return {
        "username": username,
        "password": password
    }

def test_login(credentials):
    """認証情報を使用してテスト"""
    assert credentials["username"] in ["admin", "user"]
    assert "123" in credentials["password"]
```

### パラメータ化フィクスチャのスコープ

パラメータ化されたフィクスチャにもスコープを設定できます。

```python
@pytest.fixture(scope="module", params=["sqlite", "postgresql"])
def database_type(request):
    """モジュールスコープでパラメータ化"""
    db_type = request.param
    print(f"データベースタイプ: {db_type}")
    return db_type

def test_database_1(database_type):
    assert database_type in ["sqlite", "postgresql"]

def test_database_2(database_type):
    # 同じモジュール内では同じデータベースタイプが使用される
    assert database_type in ["sqlite", "postgresql"]
```

### パラメータ化フィクスチャの依存関係

パラメータ化されたフィクスチャは、他のフィクスチャに依存できます。

```python
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

## パラメータ化の組み合わせ

### 複数のパラメータ化デコレーター

1つのテスト関数に複数の `@pytest.mark.parametrize` を適用すると、**すべての組み合わせ**でテストが実行されます。

```python
@pytest.mark.parametrize("x", [1, 2])
@pytest.mark.parametrize("y", [3, 4])
def test_multiple_params(x, y):
    """2つのパラメータのすべての組み合わせで実行"""
    # 実行される組み合わせ:
    # (x=1, y=3), (x=1, y=4), (x=2, y=3), (x=2, y=4)
    assert x + y > 0
```

### パラメータ化されたフィクスチャとテスト関数の組み合わせ

パラメータ化されたフィクスチャとパラメータ化されたテスト関数を組み合わせると、**すべての組み合わせ**でテストが実行されます。

```python
@pytest.fixture(params=["admin", "user"])
def user_role(request):
    return request.param

@pytest.mark.parametrize("action", ["read", "write", "delete"])
def test_permissions(user_role, action):
    """ユーザーロールとアクションのすべての組み合わせでテスト"""
    # 実行される組み合わせ:
    # (admin, read), (admin, write), (admin, delete)
    # (user, read), (user, write), (user, delete)
    print(f"Testing {user_role} with {action} permission")
    assert user_role in ["admin", "user"]
    assert action in ["read", "write", "delete"]
```

### パラメータ化の順序

パラメータ化の順序は重要です。外側のパラメータ化が先に評価されます。

```python
@pytest.mark.parametrize("x", [1, 2])
@pytest.mark.parametrize("y", [3, 4])
def test_order(x, y):
    """パラメータ化の順序"""
    # 実行順序:
    # x=1, y=3
    # x=1, y=4
    # x=2, y=3
    # x=2, y=4
    pass
```

---

## パラメータ化の高度な使い方

### パラメータのID指定

パラメータにIDを指定することで、テスト結果をより読みやすくできます。

```python
@pytest.mark.parametrize("input_value,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
], ids=["one", "two", "three"])
def test_with_ids(input_value, expected):
    """IDを指定したパラメータ化"""
    assert input_value * 2 == expected
```

実行結果:
```
test_example.py::test_with_ids[one] PASSED
test_example.py::test_with_ids[two] PASSED
test_example.py::test_with_ids[three] PASSED
```

### 動的なID生成

関数を使用してIDを動的に生成できます。

```python
def id_func(val):
    """パラメータ値からIDを生成"""
    return f"value_{val}"

@pytest.mark.parametrize("value", [1, 2, 3], ids=id_func)
def test_dynamic_ids(value):
    """動的にIDを生成"""
    assert value > 0
```

### 条件付きパラメータ化

条件に応じてパラメータを選択できます。

```python
import sys

# 条件に応じてパラメータを選択
params = ["chrome", "firefox"]
if sys.platform == "darwin":  # macOSの場合
    params.append("safari")

@pytest.mark.parametrize("browser", params)
def test_browser(browser):
    """プラットフォームに応じたブラウザでテスト"""
    assert browser in params
```

### パラメータの間接指定（indirect）

`indirect=True` を使用すると、パラメータをフィクスチャに渡すことができます。

```python
@pytest.fixture
def browser(request):
    """パラメータを受け取るフィクスチャ"""
    browser_name = request.param
    print(f"ブラウザ {browser_name} をセットアップ")
    return browser_name

@pytest.mark.parametrize("browser", ["chrome", "firefox"], indirect=True)
def test_browser_indirect(browser):
    """間接的にパラメータをフィクスチャに渡す"""
    assert browser in ["chrome", "firefox"]
```

### パラメータのスキップ

特定のパラメータの組み合わせをスキップできます。

```python
import pytest

@pytest.mark.parametrize("x,y", [
    (1, 2),
    pytest.param(2, 3, marks=pytest.mark.skip(reason="スキップするテスト")),
    (3, 4),
])
def test_with_skip(x, y):
    """特定のパラメータをスキップ"""
    assert x + y > 0
```

### パラメータのマーキング

特定のパラメータにマーカーを適用できます。

```python
@pytest.mark.parametrize("browser", [
    "chrome",
    pytest.param("firefox", marks=pytest.mark.slow),
    "safari",
])
def test_browser_marked(browser):
    """特定のパラメータにマーカーを適用"""
    assert browser in ["chrome", "firefox", "safari"]
```

---

## パラメータ化のベストプラクティス

### 1. 適切なパラメータの選択

パラメータは、**テストの本質的な違い**を表すものにすべきです。

```python
# ✅ 良い例: 本質的な違いを表すパラメータ
@pytest.mark.parametrize("user_type", ["admin", "user", "guest"])
def test_permissions(user_type):
    # ユーザータイプによる権限の違いをテスト
    pass

# ❌ 悪い例: 本質的でないパラメータ
@pytest.mark.parametrize("color", ["red", "blue", "green"])
def test_user_creation(color):
    # 色はユーザー作成とは関係ない
    pass
```

### 2. パラメータの数を適切に制御

パラメータの組み合わせが多すぎると、テストの実行時間が長くなります。

```python
# ⚠️ 注意: 組み合わせが多すぎる例
@pytest.mark.parametrize("x", range(100))
@pytest.mark.parametrize("y", range(100))
def test_combination(x, y):
    # 10,000回のテストが実行される！
    pass

# ✅ 良い例: 代表的な値のみをテスト
@pytest.mark.parametrize("x,y", [
    (0, 0),
    (1, 1),
    (-1, -1),
    (100, 100),
])
def test_representative(x, y):
    # 代表的な値のみをテスト
    pass
```

### 3. パラメータの可読性

パラメータの値は、**意味が明確**であるべきです。

```python
# ✅ 良い例: 意味が明確
@pytest.mark.parametrize("status_code,expected", [
    (200, "success"),
    (404, "not_found"),
    (500, "server_error"),
])
def test_status_codes(status_code, expected):
    pass

# ❌ 悪い例: 意味が不明確
@pytest.mark.parametrize("code,result", [
    (200, "ok"),
    (404, "err"),
    (500, "err"),
])
def test_codes(code, result):
    pass
```

### 4. パラメータ化とフィクスチャの使い分け

- **パラメータ化**: テストロジックが同じで、入力値だけが異なる場合
- **フィクスチャ**: セットアップ/クリーンアップが必要な場合

```python
# パラメータ化が適切な例
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
])
def test_multiply(input, expected):
    assert input * 2 == expected

# フィクスチャが適切な例
@pytest.fixture
def database():
    db = setup_database()
    yield db
    cleanup_database(db)

def test_database_operations(database):
    # セットアップ/クリーンアップが必要
    pass
```

### 5. パラメータ化のテスト名

パラメータ化されたテストには、**意味のあるID**を付けると良いでしょう。

```python
@pytest.mark.parametrize("user_type,has_permission", [
    ("admin", True),
    ("user", False),
    ("guest", False),
], ids=["admin_has_permission", "user_no_permission", "guest_no_permission"])
def test_permissions(user_type, has_permission):
    """意味のあるIDでテストを識別しやすくする"""
    pass
```

---

## 実践的な例

### 例1: APIエンドポイントのテスト

異なるHTTPメソッドとエンドポイントの組み合わせをテストします。

```python
import pytest

@pytest.mark.parametrize("method,endpoint,expected_status", [
    ("GET", "/api/users", 200),
    ("POST", "/api/users", 201),
    ("GET", "/api/users/1", 200),
    ("DELETE", "/api/users/1", 204),
    ("GET", "/api/users/999", 404),
])
def test_api_endpoints(method, endpoint, expected_status):
    """異なるHTTPメソッドとエンドポイントの組み合わせをテスト"""
    # 実際のAPIリクエストを送信
    response = make_request(method, endpoint)
    assert response.status_code == expected_status
```

### 例2: データベース接続のテスト

異なるデータベースタイプで同じテストを実行します。

```python
import pytest

@pytest.fixture(params=["sqlite", "postgresql", "mysql"])
def database(request):
    """異なるデータベースタイプでテスト"""
    db_type = request.param
    connection = connect_to_database(db_type)
    yield connection
    connection.close()

@pytest.mark.parametrize("table_name", ["users", "products", "orders"])
def test_table_exists(database, table_name):
    """異なるデータベースとテーブルの組み合わせでテスト"""
    assert table_exists(database, table_name)
```

### 例3: 認証と権限のテスト

異なるユーザーロールとアクションの組み合わせをテストします。

```python
import pytest

@pytest.fixture(params=["admin", "user", "guest"])
def user_role(request):
    """異なるユーザーロールでテスト"""
    return request.param

@pytest.mark.parametrize("action,resource", [
    ("read", "document"),
    ("write", "document"),
    ("delete", "document"),
    ("read", "settings"),
    ("write", "settings"),
])
def test_permissions(user_role, action, resource):
    """ユーザーロール、アクション、リソースの組み合わせでテスト"""
    has_permission = check_permission(user_role, action, resource)
    
    if user_role == "admin":
        assert has_permission is True
    elif user_role == "user" and action == "read":
        assert has_permission is True
    else:
        assert has_permission is False
```

### 例4: バリデーションのテスト

様々な入力値でバリデーション関数をテストします。

```python
import pytest

@pytest.mark.parametrize("email,is_valid", [
    ("user@example.com", True),
    ("test.email@domain.co.jp", True),
    ("invalid.email", False),
    ("@example.com", False),
    ("user@", False),
    ("", False),
    ("user@example", False),
])
def test_email_validation(email, is_valid):
    """様々なメールアドレスでバリデーションをテスト"""
    result = validate_email(email)
    assert result == is_valid, f"Email {email} should be {is_valid}"
```

### 例5: 数値計算のテスト

境界値と代表的な値で計算関数をテストします。

```python
import pytest

@pytest.mark.parametrize("a,b,expected", [
    # 正常なケース
    (1, 2, 3),
    (10, 20, 30),
    (-5, 5, 0),
    # 境界値
    (0, 0, 0),
    (100, -100, 0),
    # 大きな値
    (1000, 2000, 3000),
    # 負の値
    (-10, -20, -30),
])
def test_addition(a, b, expected):
    """様々な値で加算をテスト"""
    assert add(a, b) == expected
```

### 例6: ファイル形式のテスト

異なるファイル形式で同じ処理をテストします。

```python
import pytest

@pytest.fixture(params=["json", "yaml", "xml"])
def file_format(request):
    """異なるファイル形式でテスト"""
    return request.param

@pytest.mark.parametrize("data_type", ["users", "products", "orders"])
def test_file_parsing(file_format, data_type):
    """異なるファイル形式とデータタイプの組み合わせでテスト"""
    file_path = f"test_data/{data_type}.{file_format}"
    data = parse_file(file_path, file_format)
    assert data is not None
    assert len(data) > 0
```

---

## まとめ

### パラメータ化の利点

1. **コードの重複排除**: 同じロジックを複数のテスト関数に書く必要がない
2. **網羅的なテスト**: 様々な入力値でテストを実行できる
3. **保守性の向上**: テストロジックの変更が1箇所で済む
4. **テストの可読性**: テストケースが明確に列挙される

### 使い分けの指針

- **`@pytest.mark.parametrize`**: テスト関数のパラメータ化に使用
  - 同じロジックを異なる入力値で実行したい場合
  - セットアップ/クリーンアップが不要な場合

- **`@pytest.fixture(params=...)`**: フィクスチャのパラメータ化に使用
  - セットアップ/クリーンアップが必要な場合
  - 複数のテストで同じパラメータ化されたリソースを使用する場合

### 重要なポイント

1. **適切なパラメータの選択**: テストの本質的な違いを表すパラメータを選ぶ
2. **パラメータの数を制御**: 組み合わせが多すぎないように注意
3. **意味のあるID**: パラメータに意味のあるIDを付ける
4. **可読性**: パラメータの値が意味を明確に表すようにする

### 次のステップ

- [How to use fixtures](README.md) - フィクスチャの基本的な使い方
- [About fixtures](ABOUT_FIXTURES.md) - フィクスチャの概念と設計思想
- [Fixtures reference](https://docs.pytest.org/en/stable/reference/fixtures.html#reference-fixtures) - APIリファレンス

パラメータ化を適切に活用することで、より効率的で保守性の高いテストコードを書くことができるようになります。

