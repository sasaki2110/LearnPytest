"""
ファイルサービスのテスト
ファイル操作をモック化してテストします。

全般的に、pathを丸々モック化して、必要なメソッドの戻り値を設定する。
"""

import pytest
from unittest.mock import Mock, patch, mock_open
from services.file_service import FileService


@pytest.fixture
def file_service():
    """ファイルサービスのフィクスチャ"""
    return FileService()


def test_read_file_success(file_service):
    """ファイル読み込みが成功する場合のテスト"""
    with patch("services.file_service.Path") as mock_path:
        mock_path_instance = Mock()
        mock_path_instance.exists.return_value = True
        mock_path_instance.read_text.return_value = "Hello, World!"
        mock_path.return_value = mock_path_instance
        
        # テスト実行
        result = file_service.read_file("test.txt")
        
        # 結果を検証
        assert result == "Hello, World!"
        
        # ファイルが正しく読み込まれたことを確認
        mock_path_instance.read_text.assert_called_once_with(encoding="utf-8")


def test_read_file_not_found(file_service):
    """ファイルが見つからない場合のテスト"""
    # Path.exists が False を返す
    with patch("services.file_service.Path") as mock_path:
        mock_path_instance = Mock()
        mock_path_instance.exists.return_value = False
        mock_path.return_value = mock_path_instance
        
        # エラーが発生することを確認
        with pytest.raises(FileNotFoundError, match="File not found"):
            file_service.read_file("nonexistent.txt")


def test_write_file(file_service):
    """ファイル書き込みのテスト"""
    # Path をモック化
    with patch("services.file_service.Path") as mock_path:
        mock_path_instance = Mock()
        mock_path_instance.parent.mkdir = Mock()
        mock_path_instance.write_text = Mock()
        mock_path.return_value = mock_path_instance
        
        # テスト実行
        file_service.write_file("test.txt", "Hello, World!")
        
        # ファイルが正しく書き込まれたことを確認
        mock_path_instance.parent.mkdir.assert_called_once_with(
            parents=True, exist_ok=True
        )
        mock_path_instance.write_text.assert_called_once_with(
            "Hello, World!", encoding="utf-8"
        )


def test_append_file(file_service):
    """ファイル追記のテスト"""
    # Path をモック化
    with patch("services.file_service.Path") as mock_path:
        mock_path_instance = Mock()
        mock_path_instance.exists.return_value = True
        mock_path_instance.read_text.return_value = "Existing content"
        mock_path_instance.write_text = Mock()
        mock_path.return_value = mock_path_instance
        
        # テスト実行
        file_service.append_file("test.txt", "\nNew content")
        
        # ファイルが正しく追記されたことを確認
        mock_path_instance.read_text.assert_called_once_with(encoding="utf-8")
        mock_path_instance.write_text.assert_called_once_with(
            "Existing content\nNew content", encoding="utf-8"
        )


def test_append_file_not_found(file_service):
    """追記対象のファイルが見つからない場合のテスト"""
    # Path.exists が False を返す
    with patch("services.file_service.Path") as mock_path:
        mock_path_instance = Mock()
        mock_path_instance.exists.return_value = False
        mock_path.return_value = mock_path_instance
        
        # エラーが発生することを確認
        with pytest.raises(FileNotFoundError, match="File not found"):
            file_service.append_file("nonexistent.txt", "content")


def test_file_exists(file_service):
    """ファイル存在確認のテスト"""
    # Path.exists をモック化
    with patch("services.file_service.Path") as mock_path:
        mock_path_instance = Mock()
        mock_path_instance.exists.return_value = True
        mock_path.return_value = mock_path_instance
        
        # テスト実行
        result = file_service.file_exists("test.txt")
        
        # 結果を検証
        assert result is True
        mock_path_instance.exists.assert_called_once()

