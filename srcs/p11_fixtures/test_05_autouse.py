"""
フィクスチャの自動使用（autouse）
"""

import pytest

@pytest.fixture(autouse=True)
def setup_logging():
    """すべてのテストで自動的にログ設定を実行"""
    import logging
    logging.basicConfig(level=logging.INFO)
    print("ログ設定が完了しました")

@pytest.fixture(autouse=True)
def reset_counter():
    """テストごとにカウンターをリセット"""
    print("カウンターをリセット")
    yield
    print("テスト終了後のクリーンアップ")
    print("")

def test_example_1():
    print("=" * 50)
    print("test_example_1")
    """autouseフィクスチャが自動的に適用される"""
    assert True

def test_example_2():
    print("=" * 50)
    print("test_example_2")
    """こちらも自動的に適用される"""
    assert True