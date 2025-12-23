def test_with_database(database_connection):
    """同じくconftest.pyのフィクスチャを使用"""
    assert database_connection["connected"] is True