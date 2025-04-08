"""
レポート生成ユーティリティ

コード分析結果を様々なフォーマットのレポートに変換します。
関数検証結果も含めた拡張レポートの生成もサポートします。
"""
import os
import json
import datetime
import importlib
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


def generate_report(results: Dict[str, Any], format: str = 'markdown') -> str:
    """
    分析結果からレポートを生成
    
    Args:
        results: 分析結果の辞書
        format: 出力フォーマット ('markdown', 'html', 'json')
        
    Returns:
        フォーマット済みレポート
    """
    if format == 'json':
        return json.dumps(results, indent=2, ensure_ascii=False)
    
    elif format == 'markdown':
        # ディレクトリかファイルかで処理を分ける
        if "directory" in results:
            # ディレクトリレポート
            return _generate_directory_report_md(results)
        else:
            # 単一ファイルレポート
            return _generate_file_report_md(results)
    
    elif format == 'html':
        # HTMLレポート (簡易実装)
        if "directory" in results:
            md_content = _generate_directory_report_md(results)
        else:
            md_content = _generate_file_report_md(results)
        
        # マークダウンを簡易HTMLに変換
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>コード分析レポート</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 0 auto; max-width: 900px; padding: 20px; }}
                h1 {{ color: #333; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
                h2 {{ color: #444; margin-top: 25px; }}
                h3 {{ color: #555; }}
                .issue {{ margin: 10px 0; padding: 10px; border-left: 3px solid #ddd; }}
                .error {{ border-left-color: #f44336; }}
                .warning {{ border-left-color: #ff9800; }}
                pre {{ background: #f5f5f5; padding: 10px; overflow: auto; }}
                table {{ border-collapse: collapse; width: 100%; }}
                table, th, td {{ border: 1px solid #ddd; }}
                th, td {{ padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <div id="content">
                {md_content.replace('\n', '<br>').replace('# ', '<h1>').replace('## ', '<h2>').replace('### ', '<h3>').replace('- ', '• ')}
            </div>
        </body>
        </html>
        """
        return html
    
    else:
        raise ValueError(f"サポートされていないフォーマット: {format}")


def _generate_file_report_md(results: Dict[str, Any]) -> str:
    """単一ファイルの分析レポートをマークダウンで生成"""
    file_path = results["file_path"]
    report = [
        f"# ファイル分析レポート: {Path(file_path).name}",
        "",
        f"分析日時: {results.get('timestamp', datetime.datetime.now().isoformat())}",
        f"ファイルパス: {file_path}",
        "",
        "## 品質チェック結果",
    ]
    
    # 品質チェック結果
    quality = results.get("quality", {})
    if quality.get("passed", True):
        report.append("✅ すべての品質チェックに合格しました")
    else:
        report.append("❌ 品質チェックに失敗しました")
        
        for issue in quality.get("issues", []):
            report.append(f"- **{issue.get('check', '不明なチェック')}**: {issue.get('error', '不明なエラー')}")
    
    report.append("")
    
    # 複雑度の問題
    complexity = results.get("complexity", {})
    issues = complexity.get("issues", [])
    
    report.append("## 複雑度の問題")
    if not issues:
        report.append("✅ 複雑度に関する問題は見つかりませんでした")
    else:
        report.append(f"❌ {len(issues)}件の複雑度の問題が見つかりました")
        
        for issue in issues:
            issue_type = issue.get("issue", "unknown")
            name = issue.get("name", "不明な関数")
            lineno = issue.get("lineno", "?")
            
            if issue_type == "too_long":
                lines = issue.get("lines", "?")
                limit = issue.get("limit", "?")
                report.append(f"- 行 {lineno}: `{name}` は長すぎます ({lines}行、上限{limit}行)")
            
            elif issue_type == "too_nested":
                nest_level = issue.get("nest_level", "?")
                limit = issue.get("limit", "?")
                report.append(f"- 行 {lineno}: `{name}` はネストが深すぎます (レベル{nest_level}、上限{limit})")
            
            else:
                report.append(f"- 行 {lineno}: `{name}` に問題があります: {issue.get('message', '不明な問題')}")
    
    report.append("")
    
    # 構造情報
    structure = results.get("structure", "")
    if structure:
        report.append("## 構造情報")
        report.append(structure)
    
    return "\n".join(report)


def _generate_directory_report_md(results: Dict[str, Any]) -> str:
    """ディレクトリの分析レポートをマークダウンで生成"""
    directory = results["directory"]
    summary = results.get("summary", {})
    
    report = [
        f"# ディレクトリ分析レポート: {directory}",
        "",
        f"分析日時: {results.get('timestamp', datetime.datetime.now().isoformat())}",
        f"対象ディレクトリ: {directory}",
        "",
        "## サマリー",
        f"- 分析ファイル数: {summary.get('total_files', results.get('file_count', 0))}",
        f"- 問題のあるファイル数: {summary.get('files_with_issues', 0)}",
        f"- 複雑度の問題数: {summary.get('complexity_issues', 0)}",
        f"- 品質チェック: {'✅ 成功' if summary.get('quality_checks_passed', True) else '❌ 失敗'}",
        "",
    ]
    
    # 複雑度の高いファイル
    complex_files = summary.get("most_complex_files", [])
    if complex_files:
        report.append("## 複雑度の高いファイル")
        for item in complex_files:
            report.append(f"- {item['file']}: {item['issues']}件の問題")
        report.append("")
    
    # 品質チェックの問題
    quality_issues = results.get("quality_summary", {}).get("issues", [])
    if quality_issues:
        report.append("## 品質チェックの問題")
        for issue in quality_issues:
            report.append(f"- **{issue.get('check', '不明なチェック')}**: {issue.get('error', '不明なエラー')}")
        report.append("")
    
    # ファイル別の問題詳細
    file_details = []
    for file_path, file_result in results.get("files", {}).items():
        complexity = file_result.get("complexity", {})
        issues = complexity.get("issues", [])
        
        if issues:
            file_name = Path(file_path).name
            file_details.append(f"### {file_name}")
            
            for issue in issues:
                issue_type = issue.get("issue", "unknown")
                name = issue.get("name", "不明な関数")
                lineno = issue.get("lineno", "?")
                
                if issue_type == "too_long":
                    lines = issue.get("lines", "?")
                    limit = issue.get("limit", "?")
                    file_details.append(f"- 行 {lineno}: `{name}` は長すぎます ({lines}行、上限{limit}行)")
                
                elif issue_type == "too_nested":
                    nest_level = issue.get("nest_level", "?")
                    limit = issue.get("limit", "?")
                    file_details.append(f"- 行 {lineno}: `{name}` はネストが深すぎます (レベル{nest_level}、上限{limit})")
                
                else:
                    file_details.append(f"- 行 {lineno}: `{name}` に問題があります: {issue.get('message', '不明な問題')}")
            
            file_details.append("")
    
    if file_details:
        report.append("## ファイル別の問題詳細")
        report.extend(file_details)
    
    return "\n".join(report)


def _generate_validator_report_md(results: Dict[str, Any]) -> str:
    """
    関数検証結果のレポートをマークダウンで生成
    
    Args:
        results: 関数検証の結果
        
    Returns:
        マークダウン形式のレポート
    """
    if not results:
        return ""
        
    stats = results.get('stats', {})
    
    report = [
        "# 関数検証レポート",
        "",
        "## サマリー",
        f"- 検証した関数数: {stats.get('function_count', 0)}",
        f"- 問題のある関数数: {stats.get('function_with_issues', 0)}",
        f"- 検証したメソッド数: {stats.get('method_count', 0)}",
        f"- 問題のあるメソッド数: {stats.get('method_with_issues', 0)}",
        f"- 型ヒント不足の数: {stats.get('missing_type_hints', 0)}",
        f"- 実行時エラーの数: {stats.get('runtime_errors', 0)}",
        ""
    ]
    
    # グローバル関数の詳細
    functions = results.get('functions', [])
    if functions:
        report.append("## 関数の詳細")
        
        for func in functions:
            issues = func.get('issues', [])
            status = "❌ 問題あり" if issues else "✅ 問題なし"
            
            report.append(f"### {func['name']} ({status})")
            report.append(f"**シグネチャ**: `{func['signature']}`")
            
            if func.get('docstring'):
                report.append(f"\n**ドキュメント**:\n```\n{func['docstring']}\n```")
            
            if issues:
                report.append("\n**検出された問題**:")
                for issue in issues:
                    issue_type = issue.get('type', 'unknown')
                    message = issue.get('message', '不明な問題')
                    
                    if issue_type == 'missing_type_hint':
                        report.append(f"- 🔶 型ヒント不足: {message}")
                    elif issue_type == 'missing_return_type':
                        report.append(f"- 🔶 戻り値の型ヒント不足: {message}")
                    elif issue_type == 'return_type_mismatch':
                        report.append(f"- 🔴 戻り値型不一致: {message}")
                    elif issue_type == 'function_error':
                        report.append(f"- 🔴 実行時エラー: {message}")
                    else:
                        report.append(f"- ⚠️ その他の問題: {message}")
            
            report.append("")
    
    # クラスの詳細
    classes = results.get('classes', [])
    if classes:
        report.append("## クラスの詳細")
        
        for cls in classes:
            report.append(f"### クラス: {cls['name']}")
            
            if cls.get('docstring'):
                report.append(f"\n**ドキュメント**:\n```\n{cls['docstring']}\n```")
            
            # クラスの問題
            issues = cls.get('issues', [])
            if issues:
                report.append("\n**クラスの問題**:")
                for issue in issues:
                    report.append(f"- ⚠️ {issue.get('message', '不明な問題')}")
            
            # メソッドの詳細
            methods = cls.get('methods', [])
            if methods:
                report.append("\n**メソッド**:")
                
                for method in methods:
                    method_issues = method.get('issues', [])
                    status = "❌ 問題あり" if method_issues else "✅ 問題なし"
                    
                    report.append(f"#### {method['name']} ({status})")
                    report.append(f"**シグネチャ**: `{method['signature']}`")
                    
                    if method.get('docstring'):
                        report.append(f"\n**ドキュメント**:\n```\n{method['docstring']}\n```")
                    
                    if method_issues:
                        report.append("\n**検出された問題**:")
                        for issue in method_issues:
                            issue_type = issue.get('type', 'unknown')
                            message = issue.get('message', '不明な問題')
                            
                            if issue_type == 'missing_type_hint':
                                report.append(f"- 🔶 型ヒント不足: {message}")
                            elif issue_type == 'missing_return_type':
                                report.append(f"- 🔶 戻り値の型ヒント不足: {message}")
                            elif issue_type == 'return_type_mismatch':
                                report.append(f"- 🔴 戻り値型不一致: {message}")
                            elif issue_type == 'function_error':
                                report.append(f"- 🔴 実行時エラー: {message}")
                            else:
                                report.append(f"- ⚠️ その他の問題: {message}")
                    
                    report.append("")
            
            report.append("")
    
    return "\n".join(report)


def generate_enhanced_report(
    code_analysis_results: Dict[str, Any],
    validator_results: Optional[Dict[str, Any]] = None,
    format: str = 'markdown'
) -> str:
    """
    コード分析と関数検証の結果を統合したレポートを生成
    
    Args:
        code_analysis_results: コード分析の結果
        validator_results: 関数検証の結果（オプション）
        format: 出力フォーマット ('markdown', 'html', 'json')
        
    Returns:
        フォーマット済みレポート
    """
    if format == 'json':
        # JSON形式の場合は結果を統合
        combined_results = {
            'code_analysis': code_analysis_results,
            'validator_results': validator_results or {}
        }
        return json.dumps(combined_results, indent=2, ensure_ascii=False)
    
    elif format == 'markdown':
        # マークダウン形式の場合
        
        # コード分析レポートの基本部分を生成
        base_report = generate_report(code_analysis_results, format='markdown')
        
        # 関数検証結果がある場合のみ追加
        if validator_results:
            validator_report = _generate_validator_report_md(validator_results)
            return f"{base_report}\n\n{validator_report}"
        else:
            return base_report
    
    elif format == 'html':
        # HTMLレポートの場合、マークダウンを生成して簡易変換
        md_report = generate_enhanced_report(
            code_analysis_results, 
            validator_results, 
            format='markdown'
        )
        
        # 簡易的なHTML変換
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>拡張コード分析レポート</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 0 auto; max-width: 900px; padding: 20px; }}
                h1 {{ color: #333; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
                h2 {{ color: #444; margin-top: 25px; }}
                h3 {{ color: #555; }}
                h4 {{ color: #666; margin-top: 15px; }}
                .issue {{ margin: 10px 0; padding: 10px; border-left: 3px solid #ddd; }}
                .error {{ border-left-color: #f44336; }}
                .warning {{ border-left-color: #ff9800; }}
                pre {{ background: #f5f5f5; padding: 10px; overflow: auto; }}
                table {{ border-collapse: collapse; width: 100%; }}
                table, th, td {{ border: 1px solid #ddd; }}
                th, td {{ padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <div id="content">
                {md_report.replace('\n', '<br>').replace('# ', '<h1>').replace('## ', '<h2>').replace('### ', '<h3>').replace('#### ', '<h4>').replace('- ', '• ')}
            </div>
        </body>
        </html>
        """
        return html
    
    else:
        raise ValueError(f"サポートされていないフォーマット: {format}")


def save_report(results: Dict[str, Any], output_file: str, format: str = 'markdown') -> str:
    """
    レポートをファイルに保存
    
    Args:
        results: 分析結果
        output_file: 出力ファイルパス
        format: レポート形式
        
    Returns:
        保存したファイルパス
    """
    # レポートを生成
    report = generate_report(results, format)
    
    # 出力ディレクトリを作成
    os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
    
    # ファイル拡張子を確認/適用
    if format == 'markdown' and not output_file.endswith(('.md', '.markdown')):
        output_file += '.md'
    elif format == 'html' and not output_file.endswith(('.html', '.htm')):
        output_file += '.html'
    elif format == 'json' and not output_file.endswith('.json'):
        output_file += '.json'
    
    # ファイルに書き込み
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    return output_file


def save_enhanced_report(
    code_analysis_results: Dict[str, Any], 
    validator_results: Optional[Dict[str, Any]], 
    output_file: str, 
    format: str = 'markdown'
) -> str:
    """
    拡張レポートをファイルに保存
    
    Args:
        code_analysis_results: コード分析の結果
        validator_results: 関数検証の結果（オプション）
        output_file: 出力ファイルパス
        format: レポート形式
        
    Returns:
        保存したファイルパス
    """
    # 拡張レポートを生成
    report = generate_enhanced_report(code_analysis_results, validator_results, format)
    
    # 出力ディレクトリを作成
    os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
    
    # ファイル拡張子を確認/適用
    if format == 'markdown' and not output_file.endswith(('.md', '.markdown')):
        output_file += '.md'
    elif format == 'html' and not output_file.endswith(('.html', '.htm')):
        output_file += '.html'
    elif format == 'json' and not output_file.endswith('.json'):
        output_file += '.json'
    
    # ファイルに書き込み
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    return output_file


def create_summary_report(directory: str, 
                         output_dir: str = 'docs/code_analysis',
                         patterns: Optional[List[str]] = None,
                         recursive: bool = True,
                         max_lines: int = 100, 
                         max_nest_level: int = 4,
                         validate_functions: bool = False) -> str:
    """
    ディレクトリの分析を実行してレポートを作成する便利関数
    
    Args:
        directory: 分析するディレクトリ
        output_dir: レポートの出力ディレクトリ
        patterns: 分析対象ファイルパターン
        recursive: サブディレクトリも含めるか
        max_lines: 関数の最大行数閾値
        max_nest_level: 最大ネストレベル閾値
        validate_functions: 関数検証も行うかどうか
        
    Returns:
        生成されたレポートファイルのパス
    """
    # analytics.code_analyzer からインポート (循環インポート回避)
    from .code_analyzer import CodeAnalyzer
    
    # 関数検証をインポート (必要な場合のみ)
    validator_results = None
    if validate_functions:
        try:
            from .validator_integration import validate_functions as run_validation
        except ImportError:
            validate_functions = False
            print("関数検証モジュールをインポートできませんでした。関数検証はスキップされます。")
    
    # 分析実行
    analyzer = CodeAnalyzer(
        max_lines=max_lines, 
        max_nest_level=max_nest_level
    )
    
    results = analyzer.analyze_directory(
        directory,
        patterns=patterns,
        recursive=recursive
    )
    
    # 出力ディレクトリを作成
    os.makedirs(output_dir, exist_ok=True)
    
    # タイムスタンプを含むファイル名を生成
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    dir_name = Path(directory).name
    output_file = os.path.join(output_dir, f"{dir_name}_analysis_{timestamp}.md")
    
    # 関数検証を実行（オプション）
    if validate_functions:
        try:
            # 単一の Python ファイルを選択（例：最も問題の多いファイル）
            if "summary" in results and "most_complex_files" in results["summary"]:
                complex_files = results["summary"]["most_complex_files"]
                if complex_files:
                    target_file = complex_files[0]["file"]
                    print(f"関数検証の実行中: {target_file}")
                    validator_results = run_validation(target_file)
        except Exception as e:
            print(f"関数検証中にエラーが発生しました: {str(e)}")
    
    # レポートを保存
    if validator_results:
        return save_enhanced_report(results, validator_results, output_file, 'markdown')
    else:
        return save_report(results, output_file, 'markdown')


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="コード分析レポート生成")
    parser.add_argument("path", help="分析するファイルまたはディレクトリ")
    parser.add_argument("--output", "-o", required=True, help="出力ファイル")
    parser.add_argument("--format", "-f", choices=['markdown', 'html', 'json'], default='markdown', help="出力形式")
    parser.add_argument("--results", "-r", help="既存の分析結果JSONファイル (指定時は分析をスキップ)")
    parser.add_argument("--validator-results", "-v", help="関数検証結果のJSONファイル (オプション)")
    
    args = parser.parse_args()
    
    # 分析結果と関数検証結果を読み込む
    code_results = None
    validator_results = None
    
    if args.results:
        # 既存の分析結果を読み込み
        with open(args.results, 'r', encoding='utf-8') as f:
            code_results = json.load(f)
    else:
        # 分析を実行
        # (循環インポートを避けるため、分析が必要な場合のみインポート)
        from .code_analyzer import analyze_file, analyze_directory
        
        path = args.path
        if os.path.isfile(path):
            code_results = analyze_file(path)
        else:
            code_results = analyze_directory(path)
    
    # 関数検証結果の読み込み（オプション）
    if args.validator_results:
        with open(args.validator_results, 'r', encoding='utf-8') as f:
            validator_results = json.load(f)
    
    # レポートを保存
    if validator_results:
        output_file = save_enhanced_report(code_results, validator_results, args.output, args.format)
    else:
        output_file = save_report(code_results, args.output, args.format)
    
    print(f"レポートを作成しました: {output_file}")