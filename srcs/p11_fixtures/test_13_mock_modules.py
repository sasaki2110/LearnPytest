"""
モジュールのモック例
monkeypatchを使用してモジュール内の関数やクラスをモックする方法を示します。

参考: https://docs.pytest.org/en/stable/how-to/monkeypatch.html
"""

import pytest

# テスト対象となるモジュールのシミュレーション
# 実際のプロジェクトでは、別ファイルのモジュールをモックします

"""
例1: モジュール内の関数をモック
"""
def test_mock_module_function(monkeypatch):
    """モジュール内の関数をモック"""
    import os
    
    # os.path.expanduser をモック
    def mock_expanduser(path):
        return "/mock/home/directory"
    
    monkeypatch.setattr(os.path, "expanduser", mock_expanduser)
    
    # モックされた関数をテスト
    result = os.path.expanduser("~")
    print("")
    print(f"os.path.expanduser('~') の結果: {result}")
    assert result == "/mock/home/directory"
    print("")
    print(f"モックされた expanduser の結果: {result}")

"""
例2: モジュール内のクラスメソッドをモック
注意: datetime.datetime は不変型のため直接モックできません。
代わりに、time.time() などのモック可能な関数を使用します。
"""
def test_mock_module_class_method(monkeypatch):
    """モジュール内のクラスメソッドをモック（time.time()の例）"""
    import time
    
    # time.time() をモック
    fixed_time = 1704110400.0  # 2024-01-01 12:00:00 のタイムスタンプ
    
    def mock_time():
        return fixed_time
    
    monkeypatch.setattr(time, "time", mock_time)
    
    # モックされた関数をテスト
    result = time.time()
    assert result == fixed_time
    print("")
    print(f"モックされた time.time() の結果: {result}")

"""
例3: モジュールの属性をモック
"""
def test_mock_module_attribute(monkeypatch):
    """モジュールの属性をモック"""
    import sys
    
    # sys.platform をモック
    monkeypatch.setattr(sys, "platform", "mock_platform")
    
    # モックされた属性をテスト
    assert sys.platform == "mock_platform"
    print("")
    print(f"モックされた sys.platform: {sys.platform}")

"""
例4: 文字列パスでモジュールを指定してモック
"""
def test_mock_module_with_string_path(monkeypatch):
    """文字列パスでモジュールを指定してモック"""
    # モジュールがまだインポートされていない場合でも、
    # 文字列パスで指定することでモックできます
    
    def mock_function():
        return "mocked_result"
    
    # 文字列パスでモジュールと関数を指定
    # 注意: 実際に存在するモジュールと関数を指定する必要があります
    monkeypatch.setattr("os.getcwd", mock_function)
    
    # モックされた関数をテスト
    import os
    result = os.getcwd()
    assert result == "mocked_result"
    print("")
    print(f"モックされた os.getcwd() の結果: {result}")

"""
例5: 複数のモジュール属性をモック
"""
def test_mock_multiple_attributes(monkeypatch):
    """複数のモジュール属性をモック"""
    import os
    
    # 複数の属性をモック
    monkeypatch.setenv("TEST_VAR", "test_value")
    monkeypatch.setattr(os, "name", "mock_os")
    
    # モックされた属性をテスト
    assert os.getenv("TEST_VAR") == "test_value"
    assert os.name == "mock_os"
    print("")
    print(f"環境変数 TEST_VAR: {os.getenv('TEST_VAR')}")
    print(f"os.name: {os.name}")

"""
例6: モジュール内の関数をモックして、元の値を保持
"""
def test_mock_with_original_value(monkeypatch):
    """モジュール内の関数をモックし、元の値を保持"""
    import os
    
    # 元の関数を保存
    original_getenv = os.getenv
    
    # モック関数を作成（元の関数も呼び出せる）
    def mock_getenv(key, default=None):
        if key == "MOCKED_VAR":
            return "mocked_value"
        # それ以外は元の関数を呼び出す
        return original_getenv(key, default)
    
    monkeypatch.setattr(os, "getenv", mock_getenv)
    
    # モックされた関数をテスト
    assert os.getenv("MOCKED_VAR") == "mocked_value"
    # 元の関数の動作も確認
    assert os.getenv("PATH") is not None  # 実際の環境変数
    print("")
    print(f"モックされた環境変数: {os.getenv('MOCKED_VAR')}")
    print(f"元の環境変数 PATH: {os.getenv('PATH') is not None}")

