# LearnPytest

pytestの学習用プロジェクト

## セットアップ手順

### 1. Python仮想環境の作成

プロジェクトルートで以下のコマンドを実行して仮想環境を作成します：

```bash
python3 -m venv venv
```

### 2. 仮想環境の有効化

#### Linux/macOSの場合：
```bash
source venv/bin/activate
```

### 3. 依存関係のインストール

仮想環境を有効化した状態で、以下のコマンドを実行してpytestをインストールします：

```bash
pip install pytest
```

### 4. （オプション）requirements.txtの作成

インストールしたパッケージを記録するために、以下のコマンドを実行します：

```bash
pip freeze > requirements.txt
```

### 5. 動作確認

pytestが正しくインストールされたか確認します：

```bash
pytest --version
```

## プロジェクト構成

- `srcs/` - ソースコードを配置するディレクトリ
- `docs/` - ドキュメントを配置するディレクトリ
- `venv/` - Python仮想環境（.gitignoreに追加済み）

## 注意事項

- 仮想環境を有効化した状態で作業を行ってください
- 作業が終わったら、`deactivate`コマンドで仮想環境を無効化できます

