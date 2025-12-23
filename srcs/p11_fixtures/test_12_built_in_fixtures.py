"""
組み込みフィクスチャ
"""

import pytest

"""
tmp_pathの例 (テンポラリーパスを使用してファイルを作成)
"""

@pytest.fixture
def maked_tmp_file(tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello, pytest!")
    print("")
    print(f"一時ファイル {test_file} を作成しました")

    yield test_file

    test_file.unlink()
    print("")
    print(f"一時ファイル {test_file} を削除しました")

def test_file_creation(maked_tmp_file):
    assert maked_tmp_file.exists()
    assert maked_tmp_file.read_text() == "Hello, pytest!"

"""
monkeypatchの例 (環境変数を一時的に変更)
"""
def test_environment_variable(monkeypatch):
    """環境変数を一時的に変更"""
    import os
    print("")
    print(f"環境変数 API_KEY の値は {os.getenv('API_KEY')} です")

    monkeypatch.setenv("API_KEY", "test_key")

    assert os.getenv("API_KEY") == "test_key"
    print("")
    print(f"環境変数 API_KEY を {os.getenv('API_KEY')} に変更しました")

"""
capsysの例 (標準出力をキャプチャ)
capsysは、標準出力と標準エラー出力をキャプチャするためのフィクスチャです。
capsysをパラメータに記載したテスト関数内の、テスト中は出力がコンソールに出ず、captured.outで検証できます。

標準出力や標準エラー出力の検証に使用します。
"""
def test_print_output(capsys):
    """標準出力をキャプチャ"""
    print("Hello, pytest!")
    captured = capsys.readouterr()
    
    assert captured.out == "Hello, pytest!\n"