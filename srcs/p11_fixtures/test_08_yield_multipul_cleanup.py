import pytest

@pytest.fixture
def complex_setup():
    """複数のリソースをセットアップし、順番にクリーンアップ"""
    resources = []
    
    # リソース1のセットアップ
    resource1 = {"type": "database", "id": 1}
    resources.append(resource1)
    
    # リソース2のセットアップ
    resource2 = {"type": "cache", "id": 2}
    resources.append(resource2)

    for resource in resources:
        print("")
        print(f"リソース {resource['id']} をセットアップ")
        resource["active"] = True
    
    yield resources
    
    # クリーンアップ（逆順）
    for resource in reversed(resources):
        print("")
        print(f"リソース {resource['id']} をクリーンアップ")
        resource["active"] = False

def test_complex_setup(complex_setup):
    print("")
    print("テスト関数の実行")

    assert complex_setup[0]["active"] is True
    assert complex_setup[0]["type"] == "database"
    assert complex_setup[0]["id"] == 1

    assert complex_setup[1]["active"] is True
    assert complex_setup[1]["type"] == "cache"
    assert complex_setup[1]["id"] == 2