import ast
import os
import sys
from collections import defaultdict


class CodeComplexityChecker:
    """
    関数の行数とネストレベルを数える簡易的なコード複雑度チェッカー
    """
    
    def __init__(self, max_lines=100, max_nest_level=4):
        """
        Args:
            max_lines: 関数の最大行数の閾値
            max_nest_level: 最大ネストレベルの閾値
        """
        self.max_lines = max_lines
        self.max_nest_level = max_nest_level
        self.issues = []
    
    def _count_lines(self, node):
        """ASTノードの行数をカウント"""
        if hasattr(node, 'lineno') and hasattr(node, 'end_lineno'):
            return node.end_lineno - node.lineno + 1
        return 0
    
    def _get_max_nest_level(self, node, current_level=0):
        """最大ネストレベルを計算"""
        max_level = current_level
        
        # 制御構造のネストをチェック
        if isinstance(node, (ast.For, ast.While, ast.If, ast.With, ast.Try)):
            current_level += 1
            max_level = max(max_level, current_level)
        
        # 再帰的に子ノードをチェック
        for child in ast.iter_child_nodes(node):
            child_level = self._get_max_nest_level(child, current_level)
            max_level = max(max_level, child_level)
        
        return max_level
    
    def check_file(self, file_path):
        """ファイルをチェック"""
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        return self.check_code(code, file_path)
    
    def check_code(self, code, file_name="<string>"):
        """コード文字列をチェック"""
        self.issues = []
        
        try:
            tree = ast.parse(code)
            
            # モジュール内のすべての関数定義と関数とメソッドを検出
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    name = node.name
                    lines = self._count_lines(node)
                    max_nest = self._get_max_nest_level(node)
                    
                    # 行数チェック
                    if lines > self.max_lines:
                        self.issues.append({
                            'file': file_name,
                            'name': name,
                            'type': 'function' if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) else 'class',
                            'issue': 'too_long',
                            'lines': lines,
                            'limit': self.max_lines,
                            'lineno': node.lineno
                        })
                    
                    # ネストレベルチェック
                    if max_nest > self.max_nest_level:
                        self.issues.append({
                            'file': file_name,
                            'name': name,
                            'type': 'function' if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) else 'class',
                            'issue': 'too_nested',
                            'nest_level': max_nest,
                            'limit': self.max_nest_level,
                            'lineno': node.lineno
                        })
            
            return len(self.issues) == 0
            
        except SyntaxError as e:
            self.issues.append({
                'file': file_name,
                'name': '<module>',
                'type': 'syntax',
                'issue': 'syntax_error',
                'message': str(e),
                'lineno': e.lineno
            })
            return False
    
    def print_report(self):
        """結果レポートを表示"""
        if not self.issues:
            print("✅ 問題は見つかりませんでした。")
            return
        
        print(f"❌ {len(self.issues)}件の問題が見つかりました:")
        
        for i, issue in enumerate(self.issues, 1):
            print(f"\n問題 #{i}:")
            print(f"  ファイル: {issue['file']}")
            print(f"  行番号: {issue['lineno']}")
            print(f"  名前: {issue['name']} ({issue['type']})")
            
            if issue['issue'] == 'too_long':
                print(f"  問題: 行数が多すぎます ({issue['lines']}行、上限{issue['limit']}行)")
            elif issue['issue'] == 'too_nested':
                print(f"  問題: ネストが深すぎます (レベル{issue['nest_level']}、上限{issue['limit']})")
            elif issue['issue'] == 'syntax_error':
                print(f"  問題: 構文エラー - {issue['message']}")


# 使用例
if __name__ == "__main__":
    # 引数からファイルを取得するか、サンプルコードを使用
    if len(sys.argv) > 1:
        file_to_check = sys.argv[1]
        checker = CodeComplexityChecker()
        checker.check_file(file_to_check)
        checker.print_report()
    else:
        # サンプルコード
        sample_code = """
def complex_function(a, b, c):
    result = 0
    if a > 0:
        if b > 0:
            if c > 0:
                if a + b > c:
                    if b + c > a:
                        result = a + b + c
                        for i in range(10):
                            for j in range(10):
                                result += i * j
    return result

def long_function():
    lines = []
    for i in range(200):
        lines.append(f"Line {i}")
    return "\\n".join(lines)
"""
        checker = CodeComplexityChecker(max_lines=20, max_nest_level=3)
        checker.check_code(sample_code, "<sample>")
        checker.print_report()