"""
フィクスチャのパラメータ化
"""

import pytest

@pytest.fixture(params=["chrome", "firefox", "safari", "edge"])
def browser(request):
    """異なるブラウザでテストを実行"""
    browser_name = request.param
    print("")
    print(f"ブラウザ {browser_name} でテストを実行")
    return browser_name

def test_browser_compatibility(browser):
    """パラメータ化されたフィクスチャを使用"""
    print("")
    print("テストの実行時に渡されたbrows渡された:", browser)
    assert browser in ["chrome", "firefox", "safari", "edge"]