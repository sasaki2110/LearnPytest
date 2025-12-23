# モックの実践例

このディレクトリでは、実際の実装コードで外部依存（API、データベース、ファイル操作など）を使用し、
テストではモックで代用する実践例を示します。

## 構成

```
mock_practice/
├── services/          # 実装コード（外部依存を使用）
│   ├── __init__.py
│   ├── weather_service.py      # 外部API呼び出しの例
│   ├── user_service.py          # データベース操作の例
│   ├── file_service.py          # ファイル操作の例
│   └── order_service.py         # 複数の依存関係の例
├── tests/            # テストコード（モックを使用）
│   ├── __init__.py
│   ├── test_weather_service.py
│   ├── test_user_service.py
│   ├── test_file_service.py
│   └── test_order_service.py
├── conftest.py       # pytest設定ファイル（共通フィクスチャ）
└── README.md         # このファイル
```

## 学習のポイント

1. **実装コード**: 外部依存（API、DB、ファイル）を実際に使用
2. **テストコード**: モックで外部依存を置き換えて、テストを高速化・安定化
3. **フィクスチャ**: モックをフィクスチャとして定義し、再利用性を高める
4. **conftest.py**: 共通のフィクスチャやヘルパー関数を定義し、テスト間で共有

## 各例の説明

### 1. weather_service.py
外部の天気APIを呼び出すサービス。テストではAPI呼び出しをモック化。

### 2. user_service.py
データベースにユーザー情報を保存・取得するサービス。テストではDB操作をモック化。

### 3. file_service.py
ファイルの読み書きを行うサービス。テストではファイル操作をモック化。

### 4. order_service.py
複数の外部依存（決済API、在庫管理、メール送信）を使用するサービス。テストでは全てをモック化。

## conftest.py について

`conftest.py` は pytest の設定ファイルで、以下の役割を持ちます：

### 1. パスの設定
テスト実行時に `services/` ディレクトリを Python のパスに追加し、インポートを可能にします。

### 2. 共通フィクスチャの定義
複数のテストで使用される共通のフィクスチャやヘルパー関数を定義します。

#### 利用可能な共通フィクスチャ

- **`mock_api_response_success`**: 成功したAPIレスポンスのモックを作成するヘルパー
  ```python
  def test_example(mock_api_response_success):
      mock_response = mock_api_response_success({"key": "value"})
      # 使用例
  ```

- **`mock_api_response_error`**: エラーが発生したAPIレスポンスのモックを作成するヘルパー
  ```python
  def test_example(mock_api_response_error):
      mock_response = mock_api_response_error(Exception("API Error"))
      # 使用例
  ```

- **`mock_successful_payment`**: 成功した決済結果のモックデータ
  ```python
  def test_example(mock_successful_payment):
      payment_result = mock_successful_payment
      # {"success": True, "transaction_id": "txn_12345"}
  ```

- **`mock_failed_payment`**: 失敗した決済結果のモックデータ
  ```python
  def test_example(mock_failed_payment):
      payment_result = mock_failed_payment
      # {"success": False, "transaction_id": None, "error": "Payment failed"}
  ```

- **`sample_user_data`**: サンプルユーザーデータ
  ```python
  def test_example(sample_user_data):
      user = sample_user_data
      # {"id": 123, "name": "Alice", "email": "alice@example.com"}
  ```

#### 使用例

```python
# test_weather_service.py での使用例
def test_get_weather(weather_service, mock_requests_get, mock_api_response_success):
    # 成功したAPIレスポンスのモックを作成
    mock_response = mock_api_response_success({
        "city": "Tokyo",
        "temperature": 25,
        "condition": "Sunny"
    })
    mock_requests_get.return_value = mock_response
    
    result = weather_service.get_weather("Tokyo")
    assert result["city"] == "Tokyo"
```

```python
# test_order_service.py での使用例
def test_create_order(order_service, mock_payment_gateway, mock_successful_payment):
    # 成功した決済結果を使用
    mock_payment_gateway.process_payment.return_value = mock_successful_payment
    
    result = order_service.create_order(...)
    assert result["transaction_id"] == "txn_12345"
```

### conftest.py の利点

- **コードの重複排除**: 同じモック設定を複数のテストで再利用
- **保守性の向上**: 共通のモック設定を1箇所で管理
- **一貫性の確保**: すべてのテストで同じパターンのモックを使用

## セットアップ

まず、必要な依存関係をインストールします：

```bash
# プロジェクトルートに移動
cd /root/LearnPytest

# 依存関係をインストール
pip install -r requirements.txt
```

**注意**: `requests` ライブラリは、実装コード（`services/weather_service.py`）で使用されています。
テストでは `requests` をモック化しますが、モジュールのインポート時に `requests` が存在する必要があります。
プロジェクトルートの `requirements.txt` に `requests` が含まれています。

## 実行方法

```bash
# mock_practice ディレクトリに移動
cd srcs/p11_fixtures/mock_practice

# すべてのテストを実行
pytest tests/

# 特定のテストを実行
pytest tests/test_weather_service.py -v

# 詳細な出力とともに実行
pytest tests/ -v -s

# または、プロジェクトルートから実行
pytest srcs/p11_fixtures/mock_practice/tests/ -v
```

## 学習の流れ

1. **実装コードを確認**: `services/` ディレクトリの各サービスを見て、どのような外部依存を使用しているか理解する
2. **テストコードを確認**: `tests/` ディレクトリの各テストを見て、どのようにモックで外部依存を置き換えているか理解する
3. **テストを実行**: 実際にテストを実行して、モックが正しく動作することを確認する
4. **自分で試す**: 新しいサービスやテストケースを追加して、モックの使い方を練習する

