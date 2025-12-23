# conftestのサンプル

conftest で共有するには、テストルート（pytest実行フォルダ）にconftest.pyを記載し、
そのフォルダ、またはそのサブフォルダにテストを配置する。

ちなみに、pytest はサブフォルダも再帰的に走査してくれる。

```
example_conftest/        # ここでpytestを実行する
├── conftest.py          # ここにフィクスチャが定義されている
├── test_3.py            # shared_resource を使用
├── hoge1/
│   └── test_1.py        # shared_resource を使用
└── fuga2/
    └── test_2.py        # database_connection を使用
```

**pytest.ini や pyproject.toml で rootdir を指定**: プロジェクトルートを明示的に指定する方法もある見たい。