# コード分析・開発支援ツール ガイド

このプロジェクトには、コード品質の向上、開発効率化、ドキュメント生成などのための様々なツールが含まれています。このガイドでは、それらのツールの概要と使い方を説明します。

## 1. コード分析ツール

### 統合コード分析 (`analytics` パッケージ)

Pythonコードの品質、複雑度、構造を包括的に分析するための統合ツールです。

#### 主な機能

- **コード構造解析**: クラス、関数、インポートなどの構造を分析
- **複雑度チェック**: 関数の行数やネストレベルを評価
- **型ヒント検証**: 関数の型ヒントが正しく設定されているか検証
- **品質チェック**: コーディング規約、セキュリティ、パフォーマンスなどをチェック

#### 使用例

```python
from analytics import analyze_directory, generate_report

# ディレクトリを分析
results = analyze_directory('src', recursive=True)

# マークダウンレポートを生成
report = generate_report(results, format='markdown')
```

#### コマンドライン実行

```bash
# 基本的な分析
python -m analytics.cli analyze src/ --recursive --report analysis.md

# 関数検証を含む拡張分析
python -m analytics.enhanced_cli analyze src/ --validate-functions --report enhanced_analysis.md
```

### コード品質チェック (`scripts/check_code_quality.py`)

コード品質チェックを一括実行するスクリプトです。Ruff、Mypy、Pytestなどの外部ツールを実行します。

```bash
python scripts/check_code_quality.py
```

### コード複雑度チェッカー (`scripts/code_complexity_checker.py`)

関数やクラスの複雑度を個別に分析するツールです。

```bash
python scripts/code_complexity_checker.py path/to/file.py
```

## 2. ファイル操作ユーティリティ

### SafeFileOps と FileStructureAnalyzer (`utils/file_utils.py`)

ファイル操作を安全に行うためのユーティリティと、プロジェクト構造を分析するためのツールです。

```python
from utils import SafeFileOps, FileUtils

# 安全なファイル書き込み
SafeFileOps.safe_write("config.json", json_content)

# プロジェクト構造のレポート生成
FileUtils.save_file_structure('docs')
```

## 3. テスト支援ツール

### テストデータ生成 (`testing` パッケージ)

テストデータを自動生成するためのユーティリティです。

```python
from testing import TestDataGenerator

# テストデータの生成
generator = TestDataGenerator()
test_email = generator.random_email()
test_date = generator.random_date()
```

### テストランナー (`scripts/test_all.py`)

テストを一括実行するためのスクリプトです。

```bash
python snippet/test_all.py
```

## 4. 入力検証ユーティリティ

### 入力サニタイザー (`utils/input_sanitizer.py`)

ユーザー入力を安全に処理するためのユーティリティです。

```python
from utils import InputSanitizer

# HTMLの安全化
safe_html = InputSanitizer.sanitize_html(user_input)

# ファイル名の安全化
safe_filename = InputSanitizer.sanitize_filename(user_input)
```

### バリデーター (`utils/validator.py`)

入力データの検証を行うためのユーティリティです。

```python
from utils import Validator

# データの検証
Validator.validate_email(email)
Validator.validate_length(text, min_length=5, max_length=100)
```

## 5. LLMツール

### ドキュメント生成 (`scripts/llm/createdocumentation.py`)

Geminiを使用して高品質なドキュメントを生成するツールです。

```bash
python scripts/llm/createdocumentation.py --topic "FastAPI" --objective "RESTful API開発ガイド" --output docs/fastapi_guide.md
```

### チャット要約 (`scripts/llm/chat_summary_tool.py`)

チャット履歴を要約するツールです。

```bash
# 最新のチャットを要約
python scripts/llm/chat_summary_tool.py --latest

# 最近の3つのチャットを要約
python scripts/llm/chat_summary_tool.py --recent 3
```

### 研究ヘルパー (`scripts/llm/research_helper.py`)

トピックについて素早く調査するツールです。

```bash
python scripts/llm/research_helper.py "量子コンピューティングの基礎"
```

## 6. 環境設定ツール

### 環境変数ローダー (`utils/env_loader.py`)

.envファイルから環境変数を読み込むユーティリティです。

```python
from utils import EnvLoader

# 環境変数の読み込み
env_loader = EnvLoader()
env_vars = env_loader.load()
db_host = env_loader.get('DB_HOST', default='localhost')
```

### 開発環境セットアップ (`scripts/setup_dev.bat`)

開発環境をセットアップするためのスクリプトです。

```bash
scripts/setup_dev.bat
```

## 7. 例外処理ユーティリティ

### 例外ハンドラー (`utils/exception_handler.py`)

例外処理を簡素化するデコレータを提供します。

```python
from utils import exception_handler

@exception_handler(reraise=False, default_return=None)
def risky_operation():
    # 例外が発生する可能性のある処理
    pass
```

## 8. ロギングユーティリティ

### コンテキスト付きロガー (`snippet/utils/logger/contextual_logger.py`)

コンテキスト情報を含むログを出力するためのユーティリティです。

```python
from snippet.utils.logger.contextual_logger import get_logger

logger = get_logger("my_module")
logger.info("処理開始", user_id=123, operation="data_sync")
```

## 統合的な使用例

### 開発ワークフローの例

1. **開発環境のセットアップ**:
   ```bash
   scripts/setup_dev.bat
   ```

2. **コード変更**:
   - 機能実装
   - テスト作成

3. **コード品質チェック**:
   ```bash
   python scripts/check_code_quality.py
   ```

4. **詳細な分析とレポート生成**:
   ```bash
   python -m analytics.enhanced_cli analyze . --validate-functions --report code_analysis.md
   ```

5. **ドキュメント生成**:
   ```bash
   python scripts/llm/createdocumentation.py --topic "実装した機能" --output docs/feature_docs.md
   ```

### プロジェクト構造の分析

```bash
# ファイル構造の保存
python scripts/save_file_structure.py

# Python解析レポートの生成
python scripts/analyze_python_files.py
```

## ツールの選び方

- **迅速な品質チェック**: `scripts/check_code_quality.py`
- **詳細なコード分析**: `analytics` パッケージ
- **ファイル操作の安全性向上**: `utils.SafeFileOps`
- **テストデータの自動生成**: `testing.TestDataGenerator`
- **ドキュメント生成の自動化**: `scripts/llm` 内のツール

各ツールは単独でも使えますが、組み合わせることでより強力な開発支援環境を構築できます。