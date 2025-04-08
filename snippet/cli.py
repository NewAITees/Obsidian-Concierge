#!/usr/bin/env python3
"""
拡張コード分析ツールのコマンドラインインターフェース

関数検証機能を追加した統合コード分析ツールをコマンドラインから使用できるようにします。
"""
import os
import sys
import argparse
import importlib.util
import json
from pathlib import Path
from typing import List, Optional, Dict, Any

# 元のモジュールをインポート
from analytics.code_analyzer import CodeAnalyzer, analyze_file, analyze_directory
from analytics.report_generator import generate_report, save_report

# 関数検証機能をインポート
from analytics.validator_integration import validate_functions


def generate_enhanced_report(
    code_analysis_results: Dict[str, Any],
    validator_results: Optional[Dict[str, Any]] = None,
    output_file: str = None,
    format: str = 'markdown'
) -> str:
    """
    コード分析と関数検証の結果を統合したレポートを生成

    Args:
        code_analysis_results: コード分析の結果
        validator_results: 関数検証の結果（オプション）
        output_file: 出力ファイルパス（省略時は返すだけ）
        format: 出力フォーマット

    Returns:
        生成されたレポート、または保存したファイルパス
    """
    # 統合結果を作成
    combined_results = {
        "timestamp": code_analysis_results.get("timestamp", ""),
        "code_analysis": code_analysis_results,
    }

    if validator_results:
        combined_results["validator_results"] = validator_results

    if format == 'json':
        # JSON形式の場合は単純に結合
        report = json.dumps(combined_results, indent=2, ensure_ascii=False)
    else:
        # 基本的なコード分析レポートを生成
        report = generate_report(code_analysis_results, format)

        # 関数検証結果がある場合は追加
        if validator_results:
            validator_report = _generate_validator_report(validator_results, format)
            if format == 'markdown':
                report += f"\n\n{validator_report}"

    # ファイルに保存（指定がある場合）
    if output_file:
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
    
    return report


def _generate_validator_report(results: Dict[str, Any], format: str = 'markdown') -> str:
    """
    関数検証結果のレポートを生成

    Args:
        results: 関数検証の結果
        format: 出力フォーマット

    Returns:
        フォーマット済みレポート
    """
    if format == 'json':
        return json.dumps(results, indent=2, ensure_ascii=False)
    
    elif format == 'markdown':
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
    
    else:
        # 他のフォーマットはサポート外
        return f"サポートされていないフォーマット: {format}"


def main(args: Optional[List[str]] = None) -> int:
    """
    コマンドライン実行のメインエントリーポイント
    
    Args:
        args: コマンドライン引数（テスト用、通常はNone）
        
    Returns:
        終了コード
    """
    # パーサー作成
    parser = argparse.ArgumentParser(
        description="拡張コード品質と構造の分析ツール",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # サブコマンド
    subparsers = parser.add_subparsers(dest="command", help="使用するコマンド")
    
    # analyze コマンド
    analyze_parser = subparsers.add_parser("analyze", help="コードを分析")
    analyze_parser.add_argument("path", help="分析するファイルまたはディレクトリ")
    analyze_parser.add_argument("--recursive", "-r", action="store_true", help="サブディレクトリも再帰的に分析")
    analyze_parser.add_argument("--patterns", "-p", nargs="+", default=["*.py"], help="分析するファイルパターン")
    analyze_parser.add_argument("--max-lines", type=int, default=100, help="関数の最大行数閾値")
    analyze_parser.add_argument("--max-nest", type=int, default=4, help="最大ネストレベル閾値")
    analyze_parser.add_argument("--output", "-o", help="結果を保存するJSONファイル")
    analyze_parser.add_argument("--report", help="分析レポートを保存するファイル")
    analyze_parser.add_argument("--format", "-f", choices=['markdown', 'html', 'json'], 
                              default='markdown', help="レポート形式")
    analyze_parser.add_argument("--validate-functions", action="store_true", 
                              help="関数の入出力検証も実行する")
    
    # validate コマンド
    validate_parser = subparsers.add_parser("validate", help="モジュールの関数を検証")
    validate_parser.add_argument("path", help="検証するPythonファイル")
    validate_parser.add_argument("--test-count", "-t", type=int, default=3, help="生成するテストケース数")
    validate_parser.add_argument("--output", "-o", help="結果を保存するJSONファイル")
    validate_parser.add_argument("--report", help="検証レポートを保存するファイル")
    validate_parser.add_argument("--format", "-f", choices=['markdown', 'html', 'json'], 
                               default='markdown', help="レポート形式")
    
    # enhanced-report コマンド
    enhanced_parser = subparsers.add_parser("enhanced-report", help="コード分析と関数検証の統合レポートを生成")
    enhanced_parser.add_argument("code_analysis", help="コード分析結果のJSONファイル")
    enhanced_parser.add_argument("--validator-results", help="関数検証結果のJSONファイル")
    enhanced_parser.add_argument("--output", "-o", required=True, help="出力ファイル")
    enhanced_parser.add_argument("--format", "-f", choices=['markdown', 'html', 'json'], 
                               default='markdown', help="レポート形式")
    
    # 既存のコマンドを継承
    report_parser = subparsers.add_parser("report", help="既存の分析結果からレポートを生成")
    report_parser.add_argument("results", help="分析結果のJSONファイル")
    report_parser.add_argument("--output", "-o", required=True, help="レポートを保存するファイル")
    report_parser.add_argument("--format", "-f", choices=['markdown', 'html', 'json'], 
                             default='markdown', help="レポート形式")
    
    check_parser = subparsers.add_parser("check", help="シンプルな品質チェックを実行")
    check_parser.add_argument("path", help="チェックするファイルまたはディレクトリ")
    check_parser.add_argument("--recursive", "-r", action="store_true", help="サブディレクトリも再帰的にチェック")
    check_parser.add_argument("--patterns", "-p", nargs="+", default=["*.py"], help="チェックするファイルパターン")
    
    # 引数解析
    args = parser.parse_args(args)
    
    # コマンドの処理
    if args.command == "analyze":
        path = args.path
        
        # 分析の実行
        if os.path.isfile(path):
            results = analyze_file(
                path,
                max_lines=args.max_lines,
                max_nest_level=args.max_nest
            )
            print(f"ファイル分析完了: {path}")
            
        else:
            results = analyze_directory(
                path,
                patterns=args.patterns,
                recursive=args.recursive,
                max_lines=args.max_lines,
                max_nest_level=args.max_nest
            )
            print(f"ディレクトリ分析完了: {path}")
            print(f"分析ファイル数: {results.get('file_count', 0)}")
        
        # 関数検証（オプション）
        validator_results = None
        if args.validate_functions:
            try:
                if os.path.isfile(path):
                    print(f"関数検証実行中: {path}")
                    validator_results = validate_functions(path)
                    print(f"関数検証完了")
                else:
                    print("関数検証はディレクトリ全体ではなく、単一ファイルでのみサポートされています")
            except Exception as e:
                print(f"関数検証エラー: {str(e)}")
        
        # JSON結果の保存（オプション）
        if args.output:
            import json
            # 関数検証結果を含むかどうか
            save_data = results
            if validator_results:
                save_data = {
                    "code_analysis": results,
                    "validator_results": validator_results
                }
            
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)
            print(f"分析結果を保存しました: {args.output}")
        
        # レポートの生成（オプション）
        if args.report:
            if validator_results:
                # 統合レポートを生成
                output_file = generate_enhanced_report(
                    results, 
                    validator_results, 
                    args.report, 
                    args.format
                )
            else:
                # 通常のレポートを生成
                output_file = save_report(results, args.report, args.format)
            
            print(f"レポートを生成しました: {output_file}")
            
        # サマリーを表示
        if "summary" in results:
            summary = results["summary"]
            print("\n=== 分析サマリー ===")
            print(f"複雑度の問題数: {summary.get('complexity_issues', 0)}")
            print(f"問題のあるファイル数: {summary.get('files_with_issues', 0)}")
            print(f"品質チェック: {'成功' if summary.get('quality_checks_passed', True) else '失敗'}")
        
        if validator_results:
            stats = validator_results.get('stats', {})
            print("\n=== 関数検証サマリー ===")
            print(f"検証した関数数: {stats.get('function_count', 0)}")
            print(f"問題のある関数数: {stats.get('function_with_issues', 0)}")
            print(f"型ヒント不足: {stats.get('missing_type_hints', 0)}")
            print(f"実行時エラー: {stats.get('runtime_errors', 0)}")
        
        return 0
    
    elif args.command == "validate":
        path = args.path
        
        # 関数検証の実行
        try:
            print(f"関数検証実行中: {path}")
            results = validate_functions(path, test_data_count=args.test_count)
            print(f"関数検証完了")
            
            # JSON結果の保存（オプション）
            if args.output:
                import json
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(results, f, indent=2, ensure_ascii=False)
                print(f"検証結果を保存しました: {args.output}")
            
            # レポートの生成（オプション）
            if args.report:
                validator_report = _generate_validator_report(results, args.format)
                
                with open(args.report, 'w', encoding='utf-8') as f:
                    f.write(validator_report)
                print(f"レポートを生成しました: {args.report}")
            
            # サマリーを表示
            stats = results.get('stats', {})
            print("\n=== 関数検証サマリー ===")
            print(f"検証した関数数: {stats.get('function_count', 0)}")
            print(f"問題のある関数数: {stats.get('function_with_issues', 0)}")
            print(f"検証したメソッド数: {stats.get('method_count', 0)}")
            print(f"問題のあるメソッド数: {stats.get('method_with_issues', 0)}")
            print(f"型ヒント不足: {stats.get('missing_type_hints', 0)}")
            print(f"実行時エラー: {stats.get('runtime_errors', 0)}")
            
            # 終了コード設定（問題があれば1、なければ0）
            return 1 if (stats.get('function_with_issues', 0) > 0 or 
                          stats.get('method_with_issues', 0) > 0) else 0
        
        except Exception as e:
            print(f"関数検証エラー: {str(e)}")
            return 1
    
    elif args.command == "enhanced-report":
        import json
        
        # コード分析結果の読み込み
        with open(args.code_analysis, 'r', encoding='utf-8') as f:
            code_analysis_results = json.load(f)
        
        # 関数検証結果の読み込み（オプション）
        validator_results = None
        if args.validator_results:
            with open(args.validator_results, 'r', encoding='utf-8') as f:
                validator_results = json.load(f)
        
        # 統合レポートの生成
        output_file = generate_enhanced_report(
            code_analysis_results,
            validator_results,
            args.output,
            args.format
        )
        print(f"拡張レポートを生成しました: {output_file}")
        
        return 0
    
    elif args.command in ["report", "check"]:
        # 既存のコマンドを実行するためのインポート
        from .cli import main as original_main
        
        # 元のCLI処理に委譲
        return original_main(sys.argv[1:])
    
    else:
        # コマンドが指定されていない場合
        parser.print_help()
        return 1


# スクリプトとして実行された場合
if __name__ == "__main__":
    sys.exit(main())