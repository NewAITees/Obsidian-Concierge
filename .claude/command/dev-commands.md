# Obsidian Concierge 開発コマンド

## 基本開発フロー

```bash
# 環境セットアップ
uv sync --all-extras

# 開発サーバー起動
uv run python -m obsidian_concierge

# テスト実行
uv run pytest

# コード品質チェック
uv run ruff format .
uv run ruff check .
uv run mypy obsidian_concierge/

# pre-commitフック実行
uv run pre-commit run --all-files
```

## CLI コマンド

```bash
# Vault インデックス作成
uv run python -m obsidian_concierge.cli index

# 検索実行
uv run python -m obsidian_concierge.cli search "検索クエリ"

# 質問回答
uv run python -m obsidian_concierge.cli ask "質問内容"
```

## Docker環境

```bash
# Docker Compose での起動
docker compose up --build

# 個別コンテナ起動
docker compose up obsidian-concierge
docker compose up ollama
```