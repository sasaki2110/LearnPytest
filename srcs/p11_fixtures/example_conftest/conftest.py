"""
conftest.py の例(共有フィクスチャの定義)
"""

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