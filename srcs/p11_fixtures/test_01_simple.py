"""
フィクスチャの簡単な例
"""

import pytest

# デコレータでフィクスチャを定義
@pytest.fixture 
def sample_data():
    return [1, 2, 3, 4, 5]

# テスト関数の引数にフィクスチャ名を指定すると、pytestが自動的にフィクスチャを実行
# フィクスチャの戻り値がテスト関数の引数として渡される
def test_sample_data(sample_data): 
    assert len(sample_data) == 5
    assert sum(sample_data) == 15