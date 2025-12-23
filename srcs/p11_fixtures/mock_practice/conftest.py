"""
pytest設定ファイル
テスト実行時にパスを追加し、共通のフィクスチャを定義します。
"""

import sys
from pathlib import Path
import pytest
from unittest.mock import Mock

# このディレクトリをパスに追加
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))


# ============================================
# 共通フィクスチャ
# ============================================

@pytest.fixture
def mock_api_response_success():
    """
    成功したAPIレスポンスのモックを作成するヘルパー関数
    
    Usage:
        mock_response = mock_api_response_success({"key": "value"})
    """
    def _create_response(data: dict, status_code: int = 200):
        """成功したAPIレスポンスのモックを作成"""
        mock_response = Mock()
        mock_response.json.return_value = data
        mock_response.status_code = status_code
        mock_response.raise_for_status = Mock()  # エラーを発生させない
        return mock_response
    return _create_response


@pytest.fixture
def mock_api_response_error():
    """
    エラーが発生したAPIレスポンスのモックを作成するヘルパー関数
    
    Usage:
        mock_response = mock_api_response_error(Exception("API Error"))
    """
    def _create_response(error: Exception, status_code: int = 500):
        """エラーが発生したAPIレスポンスのモックを作成"""
        mock_response = Mock()
        mock_response.status_code = status_code
        mock_response.raise_for_status.side_effect = error
        return mock_response
    return _create_response


@pytest.fixture
def mock_successful_payment():
    """
    成功した決済のモック設定を返すフィクスチャ
    
    Returns:
        成功した決済結果の辞書
    """
    return {
        "success": True,
        "transaction_id": "txn_12345"
    }


@pytest.fixture
def mock_failed_payment():
    """
    失敗した決済のモック設定を返すフィクスチャ
    
    Returns:
        失敗した決済結果の辞書
    """
    return {
        "success": False,
        "transaction_id": None,
        "error": "Payment failed"
    }


@pytest.fixture
def sample_user_data():
    """
    サンプルユーザーデータを返すフィクスチャ
    
    Returns:
        サンプルユーザーデータの辞書
    """
    return {
        "id": 123,
        "name": "Alice",
        "email": "alice@example.com"
    }

