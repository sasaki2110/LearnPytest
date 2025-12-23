"""
ユーザーサービスのテスト
データベース操作をモック化してテストします。
"""

import pytest
from unittest.mock import Mock
from services.user_service import UserService, Database


@pytest.fixture
def mock_database():
    """データベースのモックフィクスチャ"""
    db = Mock(spec=Database)
    db.connect = Mock()
    return db


@pytest.fixture
def user_service(mock_database):
    """ユーザーサービスのフィクスチャ"""
    return UserService(mock_database)


def test_create_user(user_service, mock_database):
    """ユーザー作成のテスト"""
    # データベースの insert メソッドの戻り値を設定
    mock_database.insert.return_value = 123
    
    # テスト実行
    result = user_service.create_user("Alice", "alice@example.com")
    
    # 結果を検証
    assert result["id"] == 123
    assert result["name"] == "Alice"
    assert result["email"] == "alice@example.com"
    
    # データベースが正しく呼ばれたことを確認
    mock_database.connect.assert_called_once()
    mock_database.insert.assert_called_once_with(
        "users",
        {"name": "Alice", "email": "alice@example.com"}
    )


def test_get_user_success(user_service, mock_database):
    """ユーザー取得が成功する場合のテスト"""
    # データベースの select メソッドの戻り値を設定
    mock_database.select.return_value = [
        {"id": 123, "name": "Alice", "email": "alice@example.com"}
    ]
    
    # テスト実行
    result = user_service.get_user(123)
    
    # 結果を検証
    assert result["id"] == 123
    assert result["name"] == "Alice"
    assert result["email"] == "alice@example.com"
    
    # データベースが正しく呼ばれたことを確認
    mock_database.select.assert_called_once_with("users", {"id": 123})


def test_get_user_not_found(user_service, mock_database):
    """ユーザーが見つからない場合のテスト"""
    # データベースの select メソッドが空のリストを返す
    mock_database.select.return_value = []
    
    # エラーが発生することを確認
    with pytest.raises(ValueError, match="User with id 123 not found"):
        user_service.get_user(123)


def test_get_user_by_email_found(user_service, mock_database):
    """メールアドレスでユーザーが見つかる場合のテスト"""
    # データベースの select メソッドの戻り値を設定
    mock_database.select.return_value = [
        {"id": 123, "name": "Alice", "email": "alice@example.com"}
    ]
    
    # テスト実行
    result = user_service.get_user_by_email("alice@example.com")
    
    # 結果を検証
    assert result is not None
    assert result["email"] == "alice@example.com"
    
    # データベースが正しく呼ばれたことを確認
    mock_database.select.assert_called_once_with(
        "users",
        {"email": "alice@example.com"}
    )


def test_get_user_by_email_not_found(user_service, mock_database):
    """メールアドレスでユーザーが見つからない場合のテスト"""
    # データベースの select メソッドが空のリストを返す
    mock_database.select.return_value = []
    
    # テスト実行
    result = user_service.get_user_by_email("unknown@example.com")
    
    # 結果を検証
    assert result is None

