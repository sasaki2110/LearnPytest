# How to use temporary directories and files in tests

一時ディレクトリとファイルの使い方（備忘録）

**公式ドキュメント**: https://docs.pytest.org/en/stable/how-to/tmp_path.html

## 組み込みフィクスチャ

### `tmp_path`

一時ディレクトリのパス（`pathlib.Path` オブジェクト）

```python
def test_example(tmp_path):
    # 一時ディレクトリにファイルを作成
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello, pytest!")
    
    # ファイルの読み込み
    content = test_file.read_text()
    assert content == "Hello, pytest!"
```

**特徴:**
- 関数スコープ（各テストごとに新しいディレクトリ）
- `pathlib.Path` オブジェクトを返す
- テスト終了後に自動削除

### `tmp_path_factory`

セッションスコープの一時ディレクトリファクトリ

```python
@pytest.fixture(scope="session")
def shared_temp_dir(tmp_path_factory):
    # セッション全体で共有する一時ディレクトリ
    return tmp_path_factory.mktemp("shared")

def test_example(shared_temp_dir):
    # セッション全体で共有される一時ディレクトリを使用
    test_file = shared_temp_dir / "test.txt"
    test_file.write_text("data")
```

**使い方:**
- `tmp_path_factory.mktemp(basename)`: 一時ディレクトリを作成
- `tmp_path_factory.getbasetemp()`: ベース一時ディレクトリを取得

### `tmpdir`（レガシー）

一時ディレクトリのパス（文字列、レガシー）

```python
def test_example(tmpdir):
    # tmpdirは文字列を返す（後方互換性のため）
    test_file = tmpdir.join("test.txt")
    test_file.write("Hello")
    
    # tmp_pathの使用を推奨
```

**注意:** `tmp_path` の使用を推奨（`tmpdir` はレガシー）

## 使用例

### ファイルの作成と読み込み

```python
def test_file_operations(tmp_path):
    # ファイルを作成
    file_path = tmp_path / "data.txt"
    file_path.write_text("test data")
    
    # ファイルを読み込み
    content = file_path.read_text()
    assert content == "test data"
```

### ディレクトリ構造の作成

```python
def test_directory_structure(tmp_path):
    # サブディレクトリを作成
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    
    # ファイルを作成
    file_path = subdir / "file.txt"
    file_path.write_text("content")
    
    assert file_path.exists()
```

### 複数ファイルの作成

```python
def test_multiple_files(tmp_path):
    # 複数のファイルを作成
    for i in range(3):
        file_path = tmp_path / f"file_{i}.txt"
        file_path.write_text(f"content {i}")
    
    # ファイルのリストを取得
    files = list(tmp_path.glob("*.txt"))
    assert len(files) == 3
```

## ベストプラクティス

- `tmp_path` を優先的に使用（`tmpdir` は避ける）
- セッション全体で共有する場合は `tmp_path_factory` を使用
- テスト終了後のクリーンアップは自動的に行われる
- パスの操作には `pathlib.Path` のメソッドを使用

## 関連フィクスチャ

- `tmp_path`: 一時ディレクトリ（推奨）
- `tmp_path_factory`: セッションスコープの一時ディレクトリファクトリ
- `tmpdir`: 一時ディレクトリ（レガシー、非推奨）

