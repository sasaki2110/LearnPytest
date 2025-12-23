# About fixtures

pytestのフィクスチャ（fixture）の概念と設計思想について深く理解することで、より効果的なテストコードを書くことができます。

**公式ドキュメント**: https://docs.pytest.org/en/stable/explanation/fixtures.html#about-fixtures

## 目次

1. [フィクスチャとは何か](#フィクスチャとは何か)
2. [pytestにおけるフィクスチャの設計思想](#pytestにおけるフィクスチャの設計思想)
3. [フィクスチャの本質的な特徴](#フィクスチャの本質的な特徴)
4. [従来のテストフレームワークとの比較](#従来のテストフレームワークとの比較)
5. [フィクスチャの設計原則](#フィクスチャの設計原則)
6. [フィクスチャの階層構造と依存関係](#フィクスチャの階層構造と依存関係)
7. [フィクスチャのスコープの設計思想](#フィクスチャのスコープの設計思想)
8. [フィクスチャによるテストの分離](#フィクスチャによるテストの分離)
9. [実践的な設計パターン](#実践的な設計パターン)
10. [まとめ](#まとめ)

---

## フィクスチャとは何か

### テストにおけるフィクスチャの役割

フィクスチャ（fixture）という言葉は、元々「固定装置」や「備品」を意味します。テストの文脈では、**テストが実行されるために必要な環境、データ、リソースを提供するもの**を指します。

### フィクスチャの本質

フィクスチャは、テストの**前提条件（preconditions）**を確立するためのメカニズムです。具体的には：

- **環境のセットアップ**: データベース接続、ファイルシステム、ネットワーク設定など
- **データの準備**: テストに必要なサンプルデータ、モックデータなど
- **リソースの管理**: 一時ファイル、メモリ、外部サービスへの接続など
- **クリーンアップ**: テスト後のリソース解放、状態のリセットなど

### なぜフィクスチャが必要なのか

テストは、**一貫性のある環境**で実行される必要があります。同じテストを何度実行しても、同じ結果が得られるべきです。フィクスチャは、この一貫性を保証するための仕組みです。

```python
# フィクスチャなしの場合（問題のある例）
def test_user_creation():
    # テストごとに異なる状態になる可能性がある
    user = create_user()  # 前のテストの影響を受ける可能性
    assert user.name == "Alice"

# フィクスチャありの場合（推奨）
@pytest.fixture
def clean_user():
    """毎回新しい、クリーンな状態のユーザーを提供"""
    return create_user()

def test_user_creation(clean_user):
    """一貫性のある環境でテストを実行"""
    assert clean_user.name == "Alice"
```

---

## pytestにおけるフィクスチャの設計思想

### 明示的な依存関係の注入

pytestのフィクスチャは、**依存性注入（Dependency Injection）**のパターンを採用しています。テスト関数の引数としてフィクスチャを指定することで、依存関係が明示的になります。

```python
# 明示的な依存関係
def test_example(database, user_data, api_client):
    # このテストが何に依存しているかが一目でわかる
    result = api_client.get_user(user_data["id"])
    assert result is not None
```

### 関数型アプローチ

pytestのフィクスチャは、**関数型プログラミング**の思想に基づいています：

- フィクスチャは関数として定義される
- 副作用を最小限に抑える
- 再利用性と組み合わせやすさを重視

```python
# 関数型のアプローチ
@pytest.fixture
def base_data():
    """基本データを返す純粋関数に近いフィクスチャ"""
    return {"value": 42}

@pytest.fixture
def processed_data(base_data):
    """base_dataを変換して新しいデータを作成"""
    return {**base_data, "processed": True}
```

### モジュール化と再利用性

フィクスチャは、**モジュール化されたコンポーネント**として設計されています。小さなフィクスチャを組み合わせて、より複雑なセットアップを構築できます。

```python
# 小さな、再利用可能なフィクスチャ
@pytest.fixture
def database_connection():
    return connect_to_db()

@pytest.fixture
def user_table(database_connection):
    return create_user_table(database_connection)

@pytest.fixture
def test_user(user_table):
    return insert_test_user(user_table)

# 組み合わせて使用
def test_user_operations(test_user, database_connection):
    # 複数のフィクスチャを組み合わせて使用
    pass
```

---

## フィクスチャの本質的な特徴

### 1. 宣言的（Declarative）

フィクスチャは、**何が必要か**を宣言するだけで、**どのように取得するか**はpytestが自動的に処理します。

```python
# 宣言的: 「user_dataが必要」と宣言するだけ
def test_example(user_data):
    # pytestが自動的にuser_dataを提供
    assert user_data is not None
```

### 2. 遅延評価（Lazy Evaluation）

フィクスチャは、実際に必要になったときにのみ実行されます。これにより、不要なセットアップを避けることができます。

```python
@pytest.fixture
def expensive_setup():
    """高コストなセットアップ"""
    print("高コストなセットアップを実行")
    return expensive_resource()

# このフィクスチャを使用しないテストでは、セットアップは実行されない
def test_simple():
    assert True  # expensive_setupは実行されない

def test_with_setup(expensive_setup):
    assert expensive_setup is not None  # ここで初めて実行される
```

### 3. スコープによる制御

フィクスチャのスコープにより、**リソースのライフサイクル**を制御できます。

```python
# セッションスコープ: テスト全体で1回だけ実行
@pytest.fixture(scope="session")
def database():
    db = setup_database()
    yield db
    teardown_database(db)

# 関数スコープ: 各テストごとに実行
@pytest.fixture(scope="function")
def clean_state():
    reset_state()
    yield
    cleanup_state()
```

### 4. 依存関係の自動解決

pytestは、フィクスチャの依存関係を**自動的に解決**し、適切な順序で実行します。

```python
@pytest.fixture
def a():
    return "A"

@pytest.fixture
def b(a):  # aに依存
    return f"B({a})"

@pytest.fixture
def c(b):  # bに依存（間接的にaにも依存）
    return f"C({b})"

def test_example(c):
    # pytestが自動的に a -> b -> c の順序で実行
    assert c == "C(B(A))"
```

---

## 従来のテストフレームワークとの比較

### setUp/tearDown パターンとの比較

従来のテストフレームワーク（unittestなど）では、`setUp` と `tearDown` メソッドを使用していました。

#### unittestのアプローチ

```python
import unittest

class TestExample(unittest.TestCase):
    def setUp(self):
        """各テストメソッドの前に実行"""
        self.data = [1, 2, 3]
        self.setup_database()
    
    def tearDown(self):
        """各テストメソッドの後に実行"""
        self.cleanup_database()
    
    def test_example(self):
        # setUpで準備されたself.dataを使用
        assert len(self.data) == 3
```

#### pytestのアプローチ

```python
import pytest

@pytest.fixture
def data():
    return [1, 2, 3]

@pytest.fixture
def database():
    db = setup_database()
    yield db
    cleanup_database(db)

def test_example(data, database):
    # 明示的な依存関係
    assert len(data) == 3
```

### pytestのアプローチの利点

1. **明示的な依存関係**: テスト関数の引数を見れば、何が必要かがわかる
2. **柔軟な組み合わせ**: 必要なフィクスチャだけを選択できる
3. **スコープの制御**: テスト、クラス、モジュール、セッションなど、柔軟にスコープを設定できる
4. **再利用性**: フィクスチャを複数のテストで簡単に共有できる
5. **関数型アプローチ**: クラスに依存しない、より柔軟な設計

---

## フィクスチャの設計原則

### 1. 単一責任の原則（Single Responsibility Principle）

各フィクスチャは、**1つの責任**だけを持つべきです。

```python
# ❌ 悪い例: 複数の責任を持つフィクスチャ
@pytest.fixture
def everything():
    db = setup_database()
    user = create_user()
    api = setup_api()
    return {"db": db, "user": user, "api": api}

# ✅ 良い例: 各フィクスチャが1つの責任を持つ
@pytest.fixture
def database():
    return setup_database()

@pytest.fixture
def user():
    return create_user()

@pytest.fixture
def api():
    return setup_api()

# 必要なものだけを組み合わせて使用
def test_example(database, user):
    # apiは不要なので指定しない
    pass
```

### 2. 再利用性の原則

フィクスチャは、**複数のテストで再利用**できるように設計すべきです。

```python
# ✅ 再利用可能なフィクスチャ
@pytest.fixture
def sample_user():
    """様々なテストで使用できる汎用的なユーザー"""
    return {
        "id": 1,
        "name": "Test User",
        "email": "test@example.com"
    }

def test_user_name(sample_user):
    assert sample_user["name"] == "Test User"

def test_user_email(sample_user):
    assert sample_user["email"] == "test@example.com"
```

### 3. 最小限のスコープの原則

フィクスチャのスコープは、**必要最小限**に設定すべきです。これにより、テストの独立性が保たれ、パフォーマンスも向上します。

```python
# ❌ 悪い例: 不要に広いスコープ
@pytest.fixture(scope="session")
def user_data():
    # セッション全体で共有されるが、各テストで変更される可能性がある
    return {"counter": 0}

# ✅ 良い例: 適切なスコープ
@pytest.fixture(scope="function")  # 各テストで独立
def user_data():
    return {"counter": 0}

# または、本当に共有する必要がある場合のみセッションスコープ
@pytest.fixture(scope="session")
def database_connection():
    # セッション全体で共有される、読み取り専用のリソース
    return connect_to_database()
```

### 4. 明示性の原則

フィクスチャの依存関係は、**明示的**であるべきです。

```python
# ❌ 悪い例: 暗黙的な依存関係（autouseの乱用）
@pytest.fixture(autouse=True)
def global_state():
    # すべてのテストに自動的に適用されるが、依存関係が見えない
    setup_global_state()

# ✅ 良い例: 明示的な依存関係
@pytest.fixture
def global_state():
    return setup_global_state()

def test_example(global_state):
    # 依存関係が明示的
    assert global_state is not None
```

---

## フィクスチャの階層構造と依存関係

### 依存関係のグラフ構造

フィクスチャの依存関係は、**有向非巡回グラフ（DAG: Directed Acyclic Graph）**として表現されます。pytestは、この依存関係グラフを解析して、適切な順序でフィクスチャを実行します。

```python
# 依存関係の例
@pytest.fixture
def level1():
    return "Level 1"

@pytest.fixture
def level2(level1):
    return f"Level 2 -> {level1}"

@pytest.fixture
def level3(level2):
    return f"Level 3 -> {level2}"

# 依存関係グラフ:
# level1 -> level2 -> level3
```

### 複数の依存関係

1つのフィクスチャが複数のフィクスチャに依存することもできます。

```python
@pytest.fixture
def database():
    return setup_database()

@pytest.fixture
def cache():
    return setup_cache()

@pytest.fixture
def api_client(database, cache):
    # databaseとcacheの両方に依存
    return create_api_client(database, cache)

# 依存関係グラフ:
# database ──┐
#            ├─> api_client
# cache ─────┘
```

### 依存関係の解決順序

pytestは、依存関係を**トポロジカルソート**して実行順序を決定します。

```python
@pytest.fixture
def a():
    print("A")
    return "A"

@pytest.fixture
def b(a):
    print("B")
    return "B"

@pytest.fixture
def c(a, b):
    print("C")
    return "C"

# 実行順序: A -> B -> C
# （aが先に実行され、次にbが実行され、最後にcが実行される）
```

---

## フィクスチャのスコープの設計思想

### スコープの階層構造

フィクスチャのスコープは、**階層構造**を持っています：

```
session (最広)
  └── package
       └── module
            └── class
                 └── function (最狭)
```

### スコープの選択指針

| スコープ | 使用例 | 注意点 |
|---------|--------|--------|
| `function` | テストごとに独立したデータが必要 | デフォルト。最も安全 |
| `class` | クラス内のテストで共有リソース | テスト間で状態が共有される |
| `module` | モジュール全体で共有する設定 | テスト間で状態が共有される |
| `package` | パッケージ全体で共有する設定 | テスト間で状態が共有される |
| `session` | データベース接続など、セッション全体で共有 | テスト間で状態が共有される |

### スコープとクリーンアップ

スコープが広いフィクスチャほど、クリーンアップが重要になります。

```python
# セッションスコープ: テスト全体で1回だけセットアップ/クリーンアップ
@pytest.fixture(scope="session")
def database():
    db = setup_database()
    yield db
    # すべてのテストが終わった後にクリーンアップ
    teardown_database(db)

# 関数スコープ: 各テストごとにセットアップ/クリーンアップ
@pytest.fixture(scope="function")
def temporary_file():
    file = create_temp_file()
    yield file
    # 各テストの後にクリーンアップ
    delete_temp_file(file)
```

---

## フィクスチャによるテストの分離

### テストの独立性

フィクスチャは、テストの**独立性**を保証するための重要なメカニズムです。

```python
# 各テストが独立した環境で実行される
@pytest.fixture(scope="function")
def isolated_data():
    """各テストごとに新しいデータが作成される"""
    return {"value": 0}

def test_1(isolated_data):
    isolated_data["value"] = 1
    assert isolated_data["value"] == 1

def test_2(isolated_data):
    # test_1の影響を受けない
    assert isolated_data["value"] == 0
```

### 状態の分離

フィクスチャにより、テスト間で**状態が分離**されます。

```python
@pytest.fixture
def clean_state():
    """クリーンな状態を提供"""
    state = {"counter": 0, "items": []}
    yield state
    # テスト後のクリーンアップ
    state.clear()

def test_add_item(clean_state):
    clean_state["items"].append("item1")
    assert len(clean_state["items"]) == 1

def test_counter(clean_state):
    # 前のテストの影響を受けない
    assert len(clean_state["items"]) == 0
```

### リソースの分離

フィクスチャにより、テスト間で**リソースが分離**されます。

```python
@pytest.fixture
def temporary_directory(tmp_path):
    """各テストごとに独立した一時ディレクトリ"""
    test_dir = tmp_path / "test"
    test_dir.mkdir()
    return test_dir

def test_file_1(temporary_directory):
    file1 = temporary_directory / "file1.txt"
    file1.write_text("content1")
    assert file1.exists()

def test_file_2(temporary_directory):
    # 前のテストのファイルは存在しない（新しいディレクトリ）
    file2 = temporary_directory / "file2.txt"
    file2.write_text("content2")
    assert file2.exists()
```

---

## 実践的な設計パターン

### パターン1: ファクトリーパターン

フィクスチャをファクトリーとして使用し、動的にオブジェクトを作成します。

```python
@pytest.fixture
def user_factory():
    """ユーザーを作成するファクトリー"""
    def _create_user(name="Default", age=30):
        return {
            "name": name,
            "age": age,
            "email": f"{name.lower()}@example.com"
        }
    return _create_user

def test_user_1(user_factory):
    user = user_factory(name="Alice", age=25)
    assert user["name"] == "Alice"

def test_user_2(user_factory):
    user = user_factory()  # デフォルト値を使用
    assert user["name"] == "Default"
```

### パターン2: ビルダーパターン

複雑なオブジェクトを段階的に構築します。

```python
@pytest.fixture
def user_builder():
    """ユーザーを段階的に構築するビルダー"""
    class UserBuilder:
        def __init__(self):
            self.user = {}
        
        def with_name(self, name):
            self.user["name"] = name
            return self
        
        def with_age(self, age):
            self.user["age"] = age
            return self
        
        def build(self):
            return self.user
    
    return UserBuilder()

def test_user_builder(user_builder):
    user = (user_builder
            .with_name("Bob")
            .with_age(35)
            .build())
    assert user["name"] == "Bob"
    assert user["age"] == 35
```

### パターン3: コンテキストマネージャーパターン

リソースの管理にコンテキストマネージャーを使用します。

```python
@pytest.fixture
def managed_resource():
    """コンテキストマネージャーでリソースを管理"""
    class Resource:
        def __enter__(self):
            print("リソースを取得")
            return self
        
        def __exit__(self, *args):
            print("リソースを解放")
    
    with Resource() as resource:
        yield resource

def test_with_resource(managed_resource):
    # リソースが自動的に管理される
    assert managed_resource is not None
```

### パターン4: パラメータ化と組み合わせ

パラメータ化されたフィクスチャを組み合わせて、様々なシナリオをテストします。

```python
@pytest.fixture(params=["admin", "user", "guest"])
def user_role(request):
    return request.param

@pytest.fixture(params=["read", "write", "delete"])
def permission(request):
    return request.param

def test_permissions(user_role, permission):
    # すべての組み合わせでテストが実行される
    # 3 roles × 3 permissions = 9回のテスト
    print(f"Testing {user_role} with {permission} permission")
```

---

## まとめ

### フィクスチャの本質

pytestのフィクスチャは、単なるセットアップ/クリーンアップの仕組みではなく、**テストの設計思想そのもの**を表現するメカニズムです。

### 重要な概念

1. **明示的な依存関係**: テストが何に依存しているかが明確
2. **モジュール化**: 小さなコンポーネントを組み合わせて複雑なセットアップを構築
3. **再利用性**: 一度定義したフィクスチャを様々なテストで使用
4. **スコープによる制御**: リソースのライフサイクルを適切に管理
5. **テストの分離**: 各テストが独立した環境で実行されることを保証

### 設計原則

- **単一責任の原則**: 各フィクスチャは1つの責任を持つ
- **最小限のスコープ**: 必要最小限のスコープを使用
- **明示性**: 依存関係を明示的に表現
- **再利用性**: 複数のテストで使用できるように設計

### 次のステップ

- [How to use fixtures](../p11_fixtures/README.md) - フィクスチャの使い方の詳細
- [How to parametrize fixtures and test functions](https://docs.pytest.org/en/stable/how-to/parametrize.html) - パラメータ化の詳細
- [Fixtures reference](https://docs.pytest.org/en/stable/reference/fixtures.html#reference-fixtures) - APIリファレンス

フィクスチャの概念と設計思想を理解することで、より保守性が高く、理解しやすいテストコードを書くことができるようになります。

