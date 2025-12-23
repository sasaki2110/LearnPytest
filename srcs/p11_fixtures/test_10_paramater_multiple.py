"""
フィクスチャのパラメータ化（複数のパラメータ）
"""
import pytest

@pytest.fixture(params=[("admin", "admin123"), ("user", "user123")])
def credentials(request):
    """異なる認証情報でテストを実行"""
    username, password = request.param
    return {"username": username, "password": password}

def test_login(credentials):
    """認証情報を使用してテスト"""
    assert credentials["username"] in ["admin", "user"]
    assert "123" in credentials["password"]