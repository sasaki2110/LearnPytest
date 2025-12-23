# test_module1.py
def test_with_shared_resource(shared_resource):
    """conftest.pyで定義されたフィクスチャを使用"""
    assert shared_resource["resource_id"] == 12345
