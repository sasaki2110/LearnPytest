import pytest

@pytest.fixture
def example_fixture():
    print("")
    print("1. セットアップ処理")  # yield前
    resource = {"value": 42}
    yield resource  # ここでテスト関数が実行される
    print("")
    print("3. クリーンアップ処理")  # yield後

def test_example(example_fixture):
    print("2. テスト関数の実行")
    assert example_fixture["value"] == 42