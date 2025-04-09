"""
統合コード分析ツール

既存の分析ツール群を統合し、一貫したインターフェースを提供します。
"""
import os
import sys
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple, Optional, Union
import datetime
import json
import concurrent.futures
from tqdm import tqdm

# 既存のツールをインポート
from ..scripts.analyze_python_files import analyze_python_file, find_usages, collect_function_calls
from ..scripts.code_complexity_checker import CodeComplexityChecker
try:
    from ..scripts.check_code_quality import run_check
except ImportError:
    # check_code_quality.py が存在しない場合のフォールバック
    def run_check(command, description):
        """コマンドを実行してチェックを行う"""
        print(f"\nチェック: {description}...")
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,
                shell=False,  # シェルインジェクションを防ぐ
            )
            if result.returncode != 0:
                return False, result.stderr or result.stdout
            return True, ""
        except subprocess.SubprocessError as e:
            return False, str(e)

# ファイル操作ユーティリティをインポート
try:
    from ..scripts.save_file_structure import get_ignored_patterns, should_include
except ImportError:
    # フォールバック実装
    def get_ignored_patterns():
        """無視するパターンを取得"""
        ignored_patterns = set()
        
        # .gitignore の読み込み
        if os.path.exists('.gitignore'):
            with open('.gitignore', 'r') as f:
                ignored_patterns.update(line.strip() for line in f if line.strip() and not line.startswith('#'))
        
        # .cursorignore の読み込み
        if os.path.exists('.cursorignore'):
            with open('.cursorignore', 'r') as f:
                ignored_patterns.update(line.strip() for line in f if line.strip() and not line.startswith('#'))
        
        return ignored_patterns

    def should_include(path, ignored_patterns):
        """ファイルを含めるかどうかを判定"""
        path_str = str(path)
        for pattern in ignored_patterns:
            if pattern in path_str or path_str.endswith(pattern):
                return False
        return True


class CodeAnalyzer:
    """
    コードの品質と構造を分析する統合ツール
    """
    
    def __init__(self, 
                 max_lines: int = 100, 
                 max_nest_level: int = 4,
                 quality_checks: Optional[List[Tuple[List[str], str]]] = None,
                 max_workers: Optional[int] = None):
        """
        統合コード分析ツールを初期化
        
        Args:
            max_lines: 関数の最大行数の閾値
            max_nest_level: 最大ネストレベルの閾値
            quality_checks: 追加の品質チェック (コマンドとその説明のタプルのリスト)
                           例: [(["ruff", "check", "."], "Ruffによるコードチェック")]
            max_workers: 並列処理の最大ワーカー数（Noneの場合はCPUコア数）
        """
        self.max_lines = max_lines
        self.max_nest_level = max_nest_level
        self.max_workers = max_workers
        
        # デフォルトの品質チェック
        self.quality_checks = quality_checks or [
            (["ruff", "check", "."], "Ruffによるコードチェック"),
            (["mypy", "."], "MypyによるPythonの型チェック"),
            (["pytest"], "Pytestによるテスト実行"),
            (["bandit", "-r", "."], "Banditによるセキュリティチェック"),
        ]
        
        # 複雑度チェッカーを初期化
        self.complexity_checker = CodeComplexityChecker(
            max_lines=max_lines, 
            max_nest_level=max_nest_level
        )
        
        # 解析結果を保存する辞書
        self.results = {}
    
    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """
        単一ファイルを分析
        
        Args:
            file_path: 分析するファイルのパス
            
        Returns:
            分析結果
        """
        file_result = {
            "file_path": file_path,
            "timestamp": datetime.datetime.now().isoformat(),
            "structure": {},
            "complexity": {},
            "quality": {"passed": True, "issues": []}
        }
        
        try:
            # 構造分析
            structure_analysis = analyze_python_file(file_path)
            file_result["structure"] = structure_analysis
            
            # 複雑度分析
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            self.complexity_checker.check_code(code, file_path)
            file_result["complexity"] = {
                "issues": self.complexity_checker.issues,
                "issue_count": len(self.complexity_checker.issues)
            }
            
            # ファイル固有の品質チェック
            for command, description in [
                (["ruff", "check", file_path], "Ruffによるコードチェック"),
                (["mypy", file_path], "Mypy型チェック"),
                (["bandit", file_path], "Banditセキュリティチェック")
            ]:
                success, error = run_check(command, description)
                if not success:
                    file_result["quality"]["passed"] = False
                    file_result["quality"]["issues"].append({
                        "check": description,
                        "error": error
                    })
            
            return file_result
            
        except Exception as e:
            # エラーが発生した場合は記録
            file_result["error"] = str(e)
            return file_result
    
    def analyze_directory(self, directory: str, 
                         patterns: Optional[List[str]] = None,
                         recursive: bool = True) -> Dict[str, Any]:
        """
        ディレクトリ内のファイルを分析
        
        Args:
            directory: 分析するディレクトリ
            patterns: 分析対象ファイルのパターン（例: ['*.py']）
            recursive: サブディレクトリも再帰的に分析するかどうか
            
        Returns:
            分析結果
        """
        # デフォルト値の設定
        if patterns is None:
            patterns = ['*.py']
        
        # 対象ファイルの収集
        py_files = []
        dir_path = Path(directory)
        ignored_patterns = get_ignored_patterns()
        
        # git ls-files を使用してバージョン管理下のファイルを取得
        try:
            git_files = set(subprocess.check_output(['git', 'ls-files'], text=True).splitlines())
        except subprocess.CalledProcessError:
            git_files = set()
        
        # パターンに一致するファイルを追加
        for pattern in patterns:
            if recursive:
                for path in dir_path.glob(f"**/{pattern}"):
                    if path.is_file() and should_include(path, ignored_patterns):
                        py_files.append(str(path))
            else:
                for path in dir_path.glob(pattern):
                    if path.is_file() and should_include(path, ignored_patterns):
                        py_files.append(str(path))
        
        # git ls-filesの結果も追加
        for git_file in git_files:
            if any(Path(git_file).match(pattern) for pattern in patterns):
                path = Path(git_file)
                if path.is_file() and should_include(path, ignored_patterns):
                    py_files.append(git_file)
        
        # 重複を排除
        py_files = sorted(set(py_files))
        
        # 分析結果の初期化
        directory_result = {
            "directory": directory,
            "timestamp": datetime.datetime.now().isoformat(),
            "file_count": len(py_files),
            "files": {},
            "quality_summary": {"passed": True, "issues": []}
        }
        
        # 並列処理で各ファイルを分析
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_file = {
                executor.submit(self.analyze_file, file_path): file_path 
                for file_path in py_files
            }
            
            with tqdm(total=len(py_files), desc="Analyzing files") as pbar:
                for future in concurrent.futures.as_completed(future_to_file):
                    file_path = future_to_file[future]
                    try:
                        file_result = future.result()
                        directory_result["files"][file_path] = file_result
                    except Exception as e:
                        print(f"Error analyzing {file_path}: {str(e)}")
                        directory_result["files"][file_path] = {
                            "error": str(e),
                            "file_path": file_path
                        }
                    finally:
                        pbar.update(1)
        
        # ディレクトリ全体の品質チェック
        for command, description in self.quality_checks:
            success, error = run_check(command, description)
            if not success:
                directory_result["quality_summary"]["passed"] = False
                directory_result["quality_summary"]["issues"].append({
                    "check": description,
                    "error": error
                })
        
        # 集計
        directory_result["summary"] = self._generate_summary(directory_result)
        
        # 結果を保存
        self.results = directory_result
        
        return directory_result
    
    def _generate_summary(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析結果のサマリーを生成
        
        Args:
            result: 分析結果
            
        Returns:
            サマリー情報
        """
        summary = {
            "total_files": result["file_count"],
            "complexity_issues": 0,
            "files_with_issues": 0,
            "quality_checks_passed": result["quality_summary"]["passed"],
            "most_complex_files": []
        }
        
        # 問題のあるファイルを集計
        complex_files = []
        for file_path, file_result in result["files"].items():
            issue_count = file_result.get("complexity", {}).get("issue_count", 0)
            if issue_count > 0:
                summary["complexity_issues"] += issue_count
                summary["files_with_issues"] += 1
                complex_files.append((file_path, issue_count))
        
        # 複雑度の高いファイルトップ5
        complex_files.sort(key=lambda x: x[1], reverse=True)
        summary["most_complex_files"] = [
            {"file": file_path, "issues": issue_count}
            for file_path, issue_count in complex_files[:5]
        ]
        
        return summary


def analyze_file(file_path: str, max_lines: int = 100, max_nest_level: int = 4) -> Dict[str, Any]:
    """
    単一ファイルを分析するヘルパー関数
    
    Args:
        file_path: 分析するファイルのパス
        max_lines: 関数の最大行数
        max_nest_level: 最大ネストレベル
        
    Returns:
        分析結果
    """
    analyzer = CodeAnalyzer(max_lines=max_lines, max_nest_level=max_nest_level)
    return analyzer.analyze_file(file_path)


def analyze_directory(directory: str, 
                     patterns: Optional[List[str]] = None,
                     recursive: bool = True,
                     max_lines: int = 100, 
                     max_nest_level: int = 4) -> Dict[str, Any]:
    """
    ディレクトリを分析するヘルパー関数
    
    Args:
        directory: 分析するディレクトリ
        patterns: 分析対象ファイルのパターン
        recursive: サブディレクトリも再帰的に分析するかどうか
        max_lines: 関数の最大行数
        max_nest_level: 最大ネストレベル
        
    Returns:
        分析結果
    """
    analyzer = CodeAnalyzer(max_lines=max_lines, max_nest_level=max_nest_level)
    return analyzer.analyze_directory(directory, patterns, recursive)


# メイン実行部分
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="コード品質と構造の分析")
    parser.add_argument("path", help="分析するファイルまたはディレクトリ")
    parser.add_argument("--recursive", "-r", action="store_true", help="サブディレクトリも再帰的に分析")
    parser.add_argument("--patterns", "-p", nargs="+", default=["*.py"], help="分析するファイルパターン")
    parser.add_argument("--max-lines", type=int, default=100, help="関数の最大行数閾値")
    parser.add_argument("--max-nest", type=int, default=4, help="最大ネストレベル閾値")
    parser.add_argument("--output", "-o", help="結果を保存するJSONファイル")
    
    args = parser.parse_args()
    
    # 分析実行
    analyzer = CodeAnalyzer(
        max_lines=args.max_lines,
        max_nest_level=args.max_nest
    )
    
    path = args.path
    if os.path.isfile(path):
        result = analyzer.analyze_file(path)
    else:
        result = analyzer.analyze_directory(
            path, 
            patterns=args.patterns, 
            recursive=args.recursive
        )
    
    # 結果を保存
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"分析結果を保存しました: {args.output}")
    else:
        # サマリーを表示
        if "summary" in result:
            print("\n=== 分析サマリー ===")
            summary = result["summary"]
            print(f"分析ファイル数: {summary['total_files']}")
            print(f"問題のあるファイル数: {summary['files_with_issues']}")
            print(f"複雑度の問題数: {summary['complexity_issues']}")
            print(f"品質チェック: {'成功' if summary['quality_checks_passed'] else '失敗'}")
            
            if summary["most_complex_files"]:
                print("\n複雑度の高いファイル:")
                for item in summary["most_complex_files"]:
                    print(f"  {item['file']}: {item['issues']}件の問題")
        else:
            print("\n=== ファイル分析 ===")
            if "complexity" in result:
                print(f"複雑度の問題数: {result['complexity'].get('issue_count', 0)}")
            
            if "quality" in result:
                print(f"品質チェック: {'成功' if result['quality']['passed'] else '失敗'}")