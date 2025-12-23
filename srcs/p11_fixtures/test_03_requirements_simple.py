"""
フィクスチャの依存関係の簡単な例
"""

import pytest

# ユーザーデータを返すフィクスチャ
@pytest.fixture
def user_data():
    return {"name": "John", "age": 30, "email": "john@example.com"}

# ユーザークラスを定義
# パラメータとしてuser_data（辞書型のユーザーデータの中身）を受け取る
@pytest.fixture
def user(user_data):
    # `@dataclass` デコレーターを使用して、ユーザークラスを簡単に定義
    from dataclasses import dataclass
    @dataclass
    class User:
        name: str
        age: int
        email: str
    # ユーザークラスをインスタンス化して返す　** 演算子（辞書のアンパック）を使用して、user_dataの中身をユーザークラスの引数に渡す  
    return User(**user_data)

def test_user(user):
    assert user.name == "John"
    assert user.age == 30
    assert user.email == "john@example.com"