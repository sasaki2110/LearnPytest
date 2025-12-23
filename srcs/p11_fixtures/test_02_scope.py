"""
フィクスチャのスコープ
"""

import pytest

# 関数スコープのフィクスチャ
@pytest.fixture(scope="function")
def function_fixture():
    return {"counter": 0}

# モジュールスコープのフィクスチャ
@pytest.fixture(scope="module")
def module_fixture():
    return {"shared_counter": 0}

# 関数スコープのフィクスチャを使用したテスト。１回目は当然０から始まる。
def test_function_fixture1(function_fixture):
    print(f"function_fixture1: {function_fixture}")
    print(f"function_fixture1_type: {type(function_fixture)}") # dict 今回の例では辞書型
    function_fixture["counter"] += 1
    assert function_fixture["counter"] == 1

# 関数スコープのフィクスチャを使用したテスト。２回目も、新しいインスタンスなので、０から始まる。
def test_function_fixture2(function_fixture):
    function_fixture["counter"] += 1
    assert function_fixture["counter"] == 1

# モジュールスコープのフィクスチャを使用したテスト。１回目は当然０から始まる。
def test_module_fixture1(module_fixture):
    module_fixture["shared_counter"] += 1
    assert module_fixture["shared_counter"] == 1

# モジュールスコープのフィクスチャを使用したテスト。２回目も、同じインスタンスなので、前のテストの値が残っている。
def test_module_fixture2(module_fixture):
    module_fixture["shared_counter"] += 1
    assert module_fixture["shared_counter"] == 2