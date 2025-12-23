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
    print("")
    print(f"一時ファイル {temp_file.name} を作成しました")
    
    yield temp_file.name  # テストにファイル名を提供
    
    # クリーンアップ: ファイルを削除
    if os.path.exists(temp_file.name):
        os.remove(temp_file.name)
        print("")
        print(f"一時ファイル {temp_file.name} を削除しました")

def test_file_operations(temporary_file):
    print("テスト関数の実行")
    """一時ファイルを使用してテスト"""
    with open(temporary_file, 'r') as f:
        content = f.read()
    assert content == "test data"