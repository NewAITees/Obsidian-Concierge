# 統合活用例

このドキュメントでは、プロジェクト内の様々なツールを組み合わせて利用する方法について説明します。個々のツールを組み合わせることで、より強力な開発支援環境が構築できます。

## コード品質と関数検証の統合

コード複雑度分析と関数の型検証を組み合わせたワークフローの例です。

```python
import json
import os
from analytics import analyze_file, validate_functions, save_enhanced_report

def analyze_with_validation(file_path):
    """コード分析と関数検証を統合して実行"""
    
    # ステップ1: コード分析
    print(f"ファイル分析中: {file_path}")
    analysis_results = analyze_file(file_path)
    
    # ステップ2: 関数検証
    print(f"関数検証中: {file_path}")
    validator_results = validate_functions(file_path)
    
    # ステップ3: 結果を統合して保存
    report_path = f"reports/{os.path.basename(file_path)}_report.md"
    os.makedirs("reports", exist_ok=True)
    
    save_enhanced_report(
        analysis_results,
        validator_results,
        report_path,
        format='markdown'
    )
    
    print(f"統合レポートを保存しました: {report_path}")
    
    # 問題があるかどうかを返す
    has_issues = (
        analysis_results.get("complexity", {}).get("issue_count", 0) > 0 or
        validator_results.get("stats", {}).get("function_with_issues", 0) > 0
    )
    
    return not has_issues

# 例: プロジェクト内の重要なファイルをチェック
key_files = ["main.py", "api/endpoints.py", "models/user.py"]
all_passed = all(analyze_with_validation(file) for file in key_files)

if all_passed:
    print("すべてのファイルが検証に合格しました！")
else:
    print("一部のファイルに問題があります。レポートを確認してください。")
```

## テストデータ生成と自動検証

テストデータの自動生成と検証機能を組み合わせた例です。

```python
from testing import TestDataGenerator
from utils import Validator, InputSanitizer

def generate_and_validate_test_data(count=10):
    """テストデータを生成し、検証する"""
    
    generator = TestDataGenerator()
    valid_data = []
    invalid_data = []
    
    for _ in range(count):
        # テストデータ生成
        test_data = {
            "name": generator.random_string(8),
            "email": generator.random_email(),
            "age": random.randint(10, 100),
            "created_at": generator.random_date()
        }
        
        # サニタイズ
        sanitized_data = {
            "name": InputSanitizer.sanitize_html(test_data["name"]),
            "email": InputSanitizer.sanitize_email(test_data["email"]),
            "age": test_data["age"],
            "created_at": test_data["created_at"]
        }
        
        # 検証
        try:
            Validator.validate_length(sanitized_data["name"], min_length=3, max_length=50)
            Validator.validate_email(sanitized_data["email"])
            Validator.validate_range(sanitized_data["age"], min_value=18, max_value=80)
            valid_data.append(sanitized_data)
        except ValidationError as e:
            invalid_data.append((sanitized_data, str(e)))
    
    return {
        "valid_data": valid_data,
        "invalid_data": invalid_data,
        "valid_count": len(valid_data),
        "invalid_count": len(invalid_data)
    }

# テスト実行
results = generate_and_validate_test_data(100)
print(f"生成されたデータ: {results['valid_count'] + results['invalid_count']}")
print(f"有効なデータ: {results['valid_count']}")
print(f"無効なデータ: {results['invalid_count']}")
```

## LLMツールとコード分析の連携

Geminiを使ったドキュメント生成とコード分析を組み合わせた例です。

```python
import os
from analytics import analyze_directory, generate_report
from scripts.llm.createdocumentation import create_documentation

def generate_project_documentation(project_dir, output_dir="docs"):
    """
    プロジェクトを分析し、コード品質レポートと
    自動生成されたドキュメントを作成
    """
    # ディレクトリが存在することを確認
    os.makedirs(output_dir, exist_ok=True)
    
    # ステップ1: コード分析
    print(f"プロジェクト分析中: {project_dir}")
    analysis_results = analyze_directory(project_dir, recursive=True)
    
    # ステップ2: 分析レポート生成
    analysis_report_path = os.path.join(output_dir, "code_quality_report.md")
    with open(analysis_report_path, 'w', encoding='utf-8') as f:
        f.write(generate_report(analysis_results))
    
    print(f"コード品質レポートを保存しました: {analysis_report_path}")
    
    # ステップ3: プロジェクト概要ドキュメントの生成
    # 分析から主要なクラスや機能を抽出
    main_classes = []
    main_functions = []
    
    for file_path, file_data in analysis_results.get("files", {}).items():
        if "structure" in file_data:
            # 注: 実際の構造解析結果に応じて調整が必要
            # このサンプルはある仮定した構造に基づいています
            structure = file_data["structure"]
            if "classes" in structure:
                main_classes.extend([cls["name"] for cls in structure.get("classes", [])])
            if "functions" in structure:
                main_functions.extend([func["name"] for func in structure.get("functions", [])])
    
    # プロジェクト概要を生成
    topic = f"{os.path.basename(project_dir)} プロジェクト"
    objective = f"主要クラス ({', '.join(main_classes[:5])}) と機能の説明"
    
    doc_result = create_documentation(
        topic=topic,
        objective=objective,
        output_path=os.path.join(output_dir, "project_overview.md")
    )
    
    return {
        "analysis_report": analysis_report_path,
        "project_overview": doc_result["output_path"],
        "stats": {
            "analyzed_files": len(analysis_results.get("files", {})),
            "main_classes": len(main_classes),
            "main_functions": len(main_functions)
        }
    }

# 例: プロジェクトのドキュメント生成
results = generate_project_documentation("./src")
print(f"ドキュメント生成完了!")
print(f"分析されたファイル数: {results['stats']['analyzed_files']}")
print(f"主要クラス数: {results['stats']['main_classes']}")
print(f"主要関数数: {results['stats']['main_functions']}")
```

## 自動コード改善ワークフロー

コード分析と自動修正を組み合わせたワークフローの例です。

```python
from analytics import analyze_file
from utils import SafeFileOps

def auto_improve_code(file_path, max_lines=80, max_nest_level=3):
    """
    コードの問題を自動的に検出し、改善する
    
    注: 完全自動化は難しいため、単純なケースのみ対応
    複雑なケースは手動での修正を推奨
    """
    # ステップ1: ファイル分析
    analysis = analyze_file(file_path, max_lines=max_lines, max_nest_level=max_nest_level)
    
    # 問題が見つからなければ終了
    if not analysis.get("complexity", {}).get("issues", []):
        print(f"問題は見つかりませんでした: {file_path}")
        return False
    
    # ステップ2: 元のコードを読み込む
    with open(file_path, 'r', encoding='utf-8') as f:
        original_code = f.read()
    
    # ステップ3: 改善されたコードを生成（簡易版）
    issues = analysis.get("complexity", {}).get("issues", [])
    improved_code = original_code
    
    for issue in issues:
        issue_type = issue.get("issue")
        
        if issue_type == "too_long":
            # 長すぎる関数には改善コメントを追加
            name = issue.get("name")
            lineno = issue.get("lineno", 1)
            lines = issue.get("lines", 0)
            
            # 改善提案をコメントとして挿入
            comment = f"# TODO: この関数は長すぎます ({lines}行)。複数の関数に分割することを検討してください。\n"
            # 注: 実際のコードでは、適切な行に挿入する処理が必要
            
        elif issue_type == "too_nested":
            # ネストが深すぎる箇所には改善コメントを追加
            name = issue.get("name")
            lineno = issue.get("lineno", 1)
            nest_level = issue.get("nest_level", 0)
            
            # 改善提案をコメントとして挿入
            comment = f"# TODO: このコードはネストが深すぎます (レベル{nest_level})。早期リターンや条件の分割を検討してください。\n"
            # 注: 実際のコードでは、適切な行に挿入する処理が必要
    
    # ステップ4: バックアップを作成して改善されたコードを保存
    if improved_code != original_code:
        backup_path = f"{file_path}.bak"
        SafeFileOps.safe_write(backup_path, original_code)
        SafeFileOps.safe_write(file_path, improved_code)
        
        print(f"コードを改善しました: {file_path}")
        print(f"バックアップを保存しました: {backup_path}")
        return True
    
    return False

# 例: 特定のファイルを自動改善
auto_improve_code("src/complex_module.py")
```

## 継続的な品質監視の設定

プロジェクトの品質を継続的に監視するセットアップの例です。

```python
import os
import schedule
import time
import datetime
from analytics import analyze_directory, save_report
from utils import EnvLoader, SafeFileOps

# 環境変数の読み込み
env_loader = EnvLoader()
env_vars = env_loader.load()

# 設定
PROJECT_DIR = env_loader.get('PROJECT_DIR', default='.')
REPORT_DIR = env_loader.get('REPORT_DIR', default='reports/quality')
CHECK_INTERVAL_HOURS = env_loader.get('CHECK_INTERVAL_HOURS', default='24', as_type=int)

def run_quality_check():
    """定期的な品質チェックを実行"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # ディレクトリを分析
    results = analyze_directory(PROJECT_DIR, recursive=True)
    
    # レポートディレクトリを作成
    os.makedirs(REPORT_DIR, exist_ok=True)
    
    # レポートを保存
    report_file = os.path.join(REPORT_DIR, f"quality_report_{timestamp}.md")
    save_report(results, report_file)
    
    # サマリーを生成
    summary = {
        "timestamp": timestamp,
        "file_count": results.get("file_count", 0),
        "issues": results.get("summary", {}).get("complexity_issues", 0),
        "report_file": report_file
    }
    
    # サマリーをJSONに保存
    summary_file = os.path.join(REPORT_DIR, "summary.json")
    existing_summaries = []
    
    if os.path.exists(summary_file):
        content = SafeFileOps.read_json(summary_file, default=[])
        if isinstance(content, list):
            existing_summaries = content
    
    existing_summaries.append(summary)
    SafeFileOps.write_json(summary_file, existing_summaries)
    
    print(f"品質チェック完了: {timestamp}")
    print(f"レポート: {report_file}")
    print(f"問題数: {summary['issues']}")

# スケジュール設定
schedule.every(CHECK_INTERVAL_HOURS).hours.do(run_quality_check)

# 起動時に1回実行
print(f"品質監視を開始します: {datetime.datetime.now()}")
run_quality_check()

# スケジュールのループ
while True:
    schedule.run_pending()
    time.sleep(60)
```

これらの例は、プロジェクト内の様々なツールを組み合わせて活用する方法を示しています。実際のプロジェクトの要件に合わせてカスタマイズしてください。