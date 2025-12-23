# Fixtures reference

フィクスチャのAPIリファレンス（備忘録）

**公式ドキュメント**: https://docs.pytest.org/en/stable/reference/fixtures.html#reference-fixtures

## 主要なAPI

### `@pytest.fixture`

フィクスチャを定義するデコレーター

```python
@pytest.fixture(scope="function", autouse=False, params=None, ids=None, name=None)
def fixture_name():
    pass
```

**パラメータ:**
- `scope`: スコープ（`function`, `class`, `module`, `package`, `session`）
- `autouse`: 自動使用（`True`/`False`）
- `params`: パラメータ化の値リスト
- `ids`: パラメータのIDリスト
- `name`: フィクスチャの名前（デフォルトは関数名）

### `request` オブジェクト

フィクスチャ内で使用できるリクエストオブジェクト

```python
@pytest.fixture
def example(request):
    # 現在のスコープ
    scope = request.scope
    
    # パラメータ値（パラメータ化されたフィクスチャの場合）
    param = request.param
    
    # フィクスチャ名
    fixturename = request.fixturename
    
    # テスト関数
    test_function = request.function
    
    # ノード（テストアイテム）
    node = request.node
```

## よく使う属性

- `request.param`: パラメータ化されたフィクスチャの現在のパラメータ値
- `request.scope`: フィクスチャのスコープ
- `request.fixturename`: フィクスチャ名
- `request.node`: 現在のテストノード

## 注意点

- フィクスチャは関数として定義される
- `yield` を使用してクリーンアップを記述
- `conftest.py` に定義すると共有可能
- 依存関係は自動的に解決される

