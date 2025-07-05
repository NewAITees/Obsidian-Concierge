# Obsidian Concierge

Obsidian ConciergeはObsidianユーザーのためのLLMベースの知識管理アシスタントです。FastAPIバックエンド、ChromaDBベクトルストレージ、OllamaローカルLLM推論を通じて、RAG検索、インテリジェントファイル管理、MOC生成、タグ付け機能を提供します。

## 機能

### 基本機能
- ベクトルベースセマンティック検索（ChromaDB）
- RAG（Retrieval-Augmented Generation）質問応答
- インテリジェントファイル移動・整理
- Map of Contents（MOC）自動生成
- Obsidianフォルダ内Pythonスクリプト実行

### 高度な機能
- TF-IDFベースの自動タグ生成
- ベクトル類似度による関連ノートリンク生成
- 日記テンプレート自動作成
- 階層構造を意識した高度なMOC生成
- インクリメンタルインデックス更新

## 技術スタック

- **バックエンド**: Python 3.12+, FastAPI, uvicorn
- **ベクトルDB**: ChromaDB（セマンティック検索）
- **LLM**: Ollama with gemma3:27b
- **パッケージ管理**: uv（高速パッケージマネージャー）
- **コード品質**: ruff（高速統合ツール）
- **テスト**: pytest（非同期対応）
- **CLI**: Click, httpx, rich（非同期HTTP + ターミナルUI）

## 必要条件

- Python 3.12以上
- Obsidianがインストールされていること
- Ollama with gemma3:27b model
- uv（推奨パッケージマネージャー）

## インストール

### 前提条件

1. **uv**のインストール（推奨）：
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. **Ollama**のインストール：
```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh

# gemma3:27bモデルのダウンロード
ollama pull gemma3:27b
```

### ソースからインストール

```bash
git clone https://github.com/yourusername/obsidian-concierge.git
cd obsidian-concierge

# uvを使用した環境構築
uv sync

# 開発用依存関係も含める場合
uv sync --dev
```

## 設定

1. 設定ファイルをコピー：

```bash
cp config.example.yaml config.yaml
```

2. `config.yaml`を編集して必要な設定を行います：

```yaml
vault:
  path: "/path/to/your/obsidian/vault"
  
ollama:
  base_url: "http://localhost:11434"
  model: "gemma3:27b"
  
chroma:
  persist_directory: "./chroma_db"
  collection_name: "obsidian_notes"
```

3. 環境変数での設定も可能：

```bash
export VAULT_PATH="/path/to/your/obsidian/vault"
export OLLAMA_BASE_URL="http://localhost:11434"
export OLLAMA_MODEL="gemma3:27b"
```

## 使用方法

### CLIコマンド

```bash
# ヘルプ表示
uv run python -m obsidian_concierge.cli --help

# Vaultのインデックス作成
uv run python -m obsidian_concierge.cli index

# セマンティック検索
uv run python -m obsidian_concierge.cli search "検索クエリ"

# 質問応答（RAG）
uv run python -m obsidian_concierge.cli ask "この文書は何について？"

# ファイル移動
uv run python -m obsidian_concierge.cli move "ファイル名" "移動先フォルダ"

# タグ自動生成
uv run python -m obsidian_concierge.cli tag generate "ファイル名"

# 関連ノートリンク生成
uv run python -m obsidian_concierge.cli link generate "ファイル名"

# MOC生成
uv run python -m obsidian_concierge.cli moc create "フォルダ名"

# 日記テンプレート作成
uv run python -m obsidian_concierge.cli journal create

# スクリプト実行
uv run python -m obsidian_concierge.cli script run "スクリプト名.py"
```

### FastAPI サーバー起動

```bash
# 開発サーバー起動
uv run python -m obsidian_concierge

# または
uv run uvicorn obsidian_concierge.main:app --reload
```

### 主要なCLIコマンド詳細

#### インデックス作成
```bash
# 全ファイルを再インデックス
uv run python -m obsidian_concierge.cli index --rebuild

# 増分インデックス更新
uv run python -m obsidian_concierge.cli index --incremental
```

#### 検索機能
```bash
# 基本検索
uv run python -m obsidian_concierge.cli search "機械学習"

# 検索結果数を指定
uv run python -m obsidian_concierge.cli search "機械学習" --limit 5

# 特定フォルダ内を検索
uv run python -m obsidian_concierge.cli search "機械学習" --folder "AI/Notes"
```

#### タグ生成
```bash
# 単一ファイルのタグ生成
uv run python -m obsidian_concierge.cli tag generate "example.md"

# フォルダ内全ファイルのタグ生成
uv run python -m obsidian_concierge.cli tag generate --folder "Notes"

# 信頼度閾値を指定
uv run python -m obsidian_concierge.cli tag generate "example.md" --threshold 0.3
```

## 開発

### 開発環境セットアップ

```bash
# 開発用依存関係をインストール
uv sync --dev

# pre-commitフックのセットアップ
uv run pre-commit install
```

### コード品質チェック

```bash
# 全品質チェック実行
uv run ruff format .          # フォーマット
uv run ruff check .           # リント
uv run mypy obsidian_concierge/  # 型チェック
uv run pytest                # テスト実行

# pre-commitフック実行
uv run pre-commit run --all-files
```

### テスト

```bash
# 全テスト実行
uv run pytest

# カバレッジ付きテスト
uv run pytest --cov=obsidian_concierge

# 特定のテストファイル実行
uv run pytest tests/test_search.py

# 詳細出力
uv run pytest -v
```

### 開発サーバー起動

```bash
# 開発用サーバー（自動リロード）
uv run uvicorn obsidian_concierge.main:app --reload --port 8000

# デバッグモード
uv run python -m obsidian_concierge --debug
```

## ライセンス

MITライセンス

## 貢献

プロジェクトへの貢献を歓迎します。以下の手順で貢献できます：

1. このリポジトリをフォーク
2. 新しいブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## サポート

問題や質問がある場合は、GitHubのIssueを作成してください。