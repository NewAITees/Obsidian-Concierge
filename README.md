# Obsidian Concierge

Obsidian Conciergeは、Obsidianナレッジベースを効率的に管理・活用するためのAIパワードアシスタントです。LLMを活用して、ナレッジベースの整理、検索、分析をサポートします。

## 特徴

- 🤖 高度なLLM統合による知識ベースの理解と活用
- 📚 効率的なナレッジベース管理と整理
- 🔍 コンテキストを考慮した高度な検索機能
- 📊 知識の関連性分析とビジュアライゼーション
- 🛠️ カスタマイズ可能なワークフロー

## 必要条件

- Python 3.10以上
- Poetry（依存関係管理）
- Ollama（LLMサービス）

## セットアップ

1. リポジトリのクローン:
```bash
git clone https://github.com/yourusername/obsidian-concierge.git
cd obsidian-concierge
```

2. 依存関係のインストール:
```bash
poetry install
```

3. 環境変数の設定:
```bash
cp .env.example .env
# .envファイルを編集して必要な設定を行う
```

4. Ollamaのセットアップ:
- [Ollama](https://ollama.ai/)をインストール
- 必要なモデルをダウンロード:
```bash
ollama pull mistral
```

## 使用方法

1. アプリケーションの起動:
```bash
poetry run python -m obsidian_concierge
```

2. APIエンドポイントの確認:
```bash
curl http://localhost:8000/docs
```

## 開発

### テストの実行

```bash
poetry run pytest
```

### リンター・フォーマッターの実行

```bash
poetry run black .
poetry run flake8
poetry run mypy .
```

## プロジェクト構造

詳細なプロジェクト構造については[ARCHITECTURE.md](docs/ARCHITECTURE.md)を参照してください。

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルを参照してください。

## コントリビューション

プロジェクトへの貢献を歓迎します。Issue報告や機能提案、プルリクエストなど、どのような形での貢献も大歓迎です。

## サポート

問題や質問がある場合は、GitHubのIssueを作成してください。