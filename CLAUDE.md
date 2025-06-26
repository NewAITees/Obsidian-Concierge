# Obsidian Concierge 開発ガイド

## プロジェクト概要

Obsidian ConciergeはObsidianユーザーのためのLLMベースの知識管理アシスタントです。FastAPIバックエンド、ChromaDBベクトルストレージ、OllamaローカルLLM推論を通じて、RAG検索、インテリジェントファイル管理、MOC生成、タグ付け機能を提供します。

## 開発ワークフロー

### 必須Git操作手順
1. 作業開始前に必ずfeatureブランチを作成
2. コミット前に必ずlint/test実行
3. PR作成時は明確な説明を記載
4. マージ前にレビュー必須

### ブランチ命名規則
- feature/issue-{番号}-{簡潔な説明}
- bugfix/issue-{番号}-{簡潔な説明}
- hotfix/{簡潔な説明}

### コミットメッセージ規則
- Conventional Commits形式を使用
- feat: 新機能
- fix: バグ修正
- docs: ドキュメント
- style: コードスタイル
- refactor: リファクタリング
- test: テスト追加・修正

### 仮想環境ルール
- Python: 必ずuvを使用（Poetryから移行済み）
- 仮想環境が有効でない場合は作業を開始しない

### 品質チェック必須項目
- Python: ruff (lint/format), mypy, pytest
- 全工程でpre-commit自動実行

## 技術スタック
- **フロントエンド**: React + TypeScript（計画中）
- **バックエンド**: Python 3.12+, FastAPI, uvicorn
- **ベクトルDB**: ChromaDB（セマンティック検索）
- **LLM**: Ollama with gemma3:27b
- **パッケージ管理**: uv（高速パッケージマネージャー）
- **コード品質**: ruff（高速統合ツール）
- **テスト**: pytest（非同期対応）
- **CLI**: httpx, rich（非同期HTTP + ターミナルUI）

## ドメイン知識

### ビジネスルール
- Obsidian Vaultの処理はすべてローカル環境で完結
- ChromaDBコレクションはVault単位で分離
- frontmatter、wikilinksなどObsidian特有の機能を適切に処理
- インクリメンタルなインデックス更新をサポート

### データモデル
```python
# APIリクエスト/レスポンスモデル
class SearchRequest(BaseModel):
    query: str
    limit: Optional[int] = 10
    filters: Optional[dict] = None

class SearchResponse(BaseModel):
    results: List[dict]
    total: int

class QuestionRequest(BaseModel):
    question: str
    context_size: Optional[int] = 3
    temperature: Optional[float] = 0.7

class QuestionResponse(BaseModel):
    answer: str
    context: List[dict]
    confidence: float
```

## 開発環境セットアップ

### uvベース環境構築
```bash
# 新規プロジェクト初期化（移行済み環境では省略）
uv init

# Pythonバージョン指定
uv python pin 3.12

# 依存関係インストール
uv sync

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

### 設定ファイル
- Main config: `config.example.yaml` → `config.yaml`
- 環境変数: `VAULT_PATH` (Obsidian vaultパス必須)
- Ollama: gemma3:27bモデルが利用可能である必要がある

## CLI ツール

包括的なCLIクライアント (`obsidian_concierge/cli.py`):

```bash
# Vault内容のインデックス作成
uv run python -m obsidian_concierge.cli index

# Vault検索
uv run python -m obsidian_concierge.cli search "検索クエリ"

# 質問回答
uv run python -m obsidian_concierge.cli ask "これは何について？"

# ノートとタグ管理
uv run python -m obsidian_concierge.cli note create "タイトル" "内容"
uv run python -m obsidian_concierge.cli tag list
```

## アーキテクチャ

レイヤードアーキテクチャを採用:

- **API Layer**: FastAPI非同期エンドポイント (`obsidian_concierge/api/`)
- **Core Layer**: 検索・Q&Aサービス (`obsidian_concierge/core/`)
- **Service Layer**: ビジネスロジック (`obsidian_concierge/services/`)
- **Repository Layer**: ChromaDB統合 (`obsidian_concierge/repository/`)
- **Infrastructure**: Vaultインデックス作成、LLMクライアント、ユーティリティ

## コーディング規約
- すべての関数に型ヒント必須
- 非同期I/O操作でasync/awaitパターン使用
- Pydanticモデルによるデータ検証
- CLIでRichコンソール出力
- HTTPExceptionによる適切なエラーハンドリング
- Googleスタイルのdocstring使用
- pathlib.Pathを使用（os.pathは使用しない）

## Git規約
- ブランチ: feature/issue-{番号}-{説明}
- コミット: Conventional Commits形式
- PR: テンプレート使用必須

## 品質基準
- テストカバレッジ: 85%以上
- ruff lint: エラー0件
- mypy type check: エラー0件
- セキュリティチェック: bandit合格

## 禁止事項
- 仮想環境無しでの開発
- テスト無しでのcommit
- レビュー無しでのマージ
- 直接mainブランチへのpush

## 主要コンポーネント

### API Routes (`obsidian_concierge/api/routes.py`)
- Health check: `/health`
- Search: `/search` (POST)
- Q&A: `/ask` (POST)
- Pydanticモデルによるリクエスト/レスポンス検証

### Services
- `SearchService`: ベクトルベース検索機能
- `QAService`: RAGベース質問回答
- ChromaRepository: データベース抽象化レイヤー

### Vault統合
- `VaultIndexer`: Obsidianマークダウンファイル処理
- frontmatter抽出とコンテンツインデックス作成
- インクリメンタル更新対応

## テスト

- テストファイル: `tests/` ディレクトリ
- pytest with async support使用
- 統合テスト含む
- 実行: `uv run pytest`

## 特別な考慮事項

- すべての処理はローカル環境で完結（外部API呼び出しなし）
- Obsidian特有のマークダウン機能（frontmatter、wikilinks）処理
- ChromaDBコレクションはVault単位で分離
- CLIはhttpxによる非同期HTTPクライアント使用
- YAML ファイルと環境変数の両方による設定対応

## 拡張ツール

`snippet/` ディレクトリには、コード品質チェックと検証のための独自CLI インターフェースを持つ追加のコード分析ツールが含まれています。