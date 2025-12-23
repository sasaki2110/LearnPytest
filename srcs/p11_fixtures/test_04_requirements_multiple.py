"""
フィクスチャの依存関係の複数の例
"""

import pytest

@pytest.fixture
def database():
    return {"connected": True}

@pytest.fixture
def user_data():
    return {"name": "John", "age": 30, "email": "john@example.com"}

@pytest.fixture
def user_with_database(database, user_data):
    return {
        "database": database,
        "user": user_data
    }

def test_user_with_database(user_with_database):
    assert user_with_database["database"]["connected"] is True
    assert user_with_database["user"]["name"] == "John"
    assert user_with_database["user"]["age"] == 30
    assert user_with_database["user"]["email"] == "john@example.com"