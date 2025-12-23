"""
フィクスチャのパラメータ化（依存関係）
"""

import pytest

@pytest.fixture(params=["sqlite", "postgresql"])
def database_type(request):
    return request.param

@pytest.fixture
def database_connection(database_type):
    print("")
    print("テストの実行時にフィクスチャ関数に渡されたdatabase_type:", database_type)
    """パラメータ化されたフィクスチャに依存"""
    if database_type == "sqlite":
        return {"type": "sqlite", "connection": "sqlite:///test.db"}
    elif database_type == "postgresql":
        return {"type": "postgresql", "connection": "postgresql://localhost/test"}

def test_database_operations(database_connection):
    """異なるデータベースタイプでテスト"""
    print("")
    print("テストの実行時に渡されたdatabase_connection:", database_connection)
    assert database_connection["type"] in ["sqlite", "postgresql"]