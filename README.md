# Obsidian Concierge

Obsidian Conciergeは、Obsidianノートの管理と分析を支援するPythonベースのツールです。AIを活用して、ノートの整理、検索、分析を効率化します。

## 機能

- ノートの自動分類と整理
- AIを活用したコンテンツ分析
- 高度な検索機能
- メタデータの自動生成と管理

## 必要条件

- Python 3.8以上
- Obsidianがインストールされていること
- OpenAI APIキー（オプション）

## インストール

```bash
pip install obsidian-concierge
```

または、ソースからインストール：

```bash
git clone https://github.com/yourusername/obsidian-concierge.git
cd obsidian-concierge
pip install -e .
```

## 設定

1. `.env.example`を`.env`にコピーして必要な設定を行います：

```bash
cp .env.example .env
```

2. `.env`ファイルを編集して、必要な環境変数を設定します：
   - `VAULT_PATH`: Obsidianボールトのパス
   - `OPENAI_API_KEY`: OpenAI APIキー（オプション）
   - その他の設定項目

## 使用方法

基本的な使用方法：

```bash
obsidian-concierge --help
```

## 開発

開発用の依存関係をインストール：

```bash
pip install -e ".[dev]"
```

テストの実行：

```bash
pytest
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