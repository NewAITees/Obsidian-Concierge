import ast
import datetime
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

from save_file_structure import get_ignored_patterns, should_include


def find_usages(node: ast.AST, target_names: Set[str]) -> Set[str]:
    """ASTノード内で使用されている名前を検索"""
    used_names = set()
    for child in ast.walk(node):
        if isinstance(child, ast.Name) and child.id in target_names:
            used_names.add(child.id)
    return used_names

def collect_function_calls(tree: ast.AST) -> Set[str]:
    """ASTから関数呼び出しを収集"""
    used_funcs = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            try:
                func_name = ast.unparse(node.func)
                # メソッド呼び出しの場合はメソッド名のみを抽出
                if '.' in func_name:
                    func_name = func_name.split('.')[-1]
                if '(' not in func_name:  # 単純な関数呼び出しのみ対象
                    used_funcs.add(func_name)
            except Exception:
                continue
    return used_funcs

def analyze_function_body(node: ast.FunctionDef) -> Tuple[Set[str], Set[str]]:
    """関数本体内での変数の使用状況を分析"""
    arg_names = {arg.arg for arg in node.args.args}
    used_args = find_usages(node, arg_names)
    
    # 関数内で定義された関数/変数を収集
    defined_names = set()
    for child in ast.walk(node):
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
            defined_names.add(child.name)
        elif isinstance(child, ast.Assign):
            for target in child.targets:
                if isinstance(target, ast.Name):
                    defined_names.add(target.id)
    
    return used_args, defined_names

def extract_docstrings(node):
    """ノードからdocstringを抽出"""
    docstring = ast.get_docstring(node)
    return f"\n**Docstring**: {docstring}" if docstring else ""

def analyze_python_file(file_path: str) -> str:
    """Pythonファイルを解析してMarkdown形式で出力"""
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    tree = ast.parse(code)
    analysis = f"# {Path(file_path).name} の解析結果\n\n"

    # 関数呼び出しの収集
    used_funcs = collect_function_calls(tree)

    # インポート解析
    imports = []
    imported_names = set()  # 追跡用
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
                imported_names.add(alias.name.split('.')[-1])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                for name in node.names:
                    full_import = f"{node.module}.{name.name}"
                    imports.append(full_import)
                    imported_names.add(name.name)

    if imports:
        analysis += "## インポート一覧\n"
        for imp in sorted(set(imports)):
            # インポートの使用状況を確認
            name = imp.split('.')[-1]
            usage = find_usages(tree, {name})
            status = "✅ 使用あり" if name in usage else "❌ 未使用"
            analysis += f"- `{imp}` ({status})\n"
        analysis += "\n"

    # クラス解析
    class_methods = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            bases = [ast.unparse(base) for base in node.bases]
            base_str = f" ({', '.join(bases)})" if bases else ""
            
            analysis += f"## クラス: `{node.name}`{base_str}"
            analysis += extract_docstrings(node) + "\n\n"
            
            for sub_node in node.body:
                if isinstance(sub_node, ast.FunctionDef):
                    decorators = [ast.unparse(d) for d in sub_node.decorator_list]
                    dec_str = f"@{', @'.join(decorators)} " if decorators else ""
                    
                    # 関数の引数使用状況を分析
                    used_args, defined_names = analyze_function_body(sub_node)
                    
                    args = []
                    for arg in sub_node.args.args:
                        arg_type = ast.unparse(arg.annotation) if arg.annotation else "Any"
                        usage_status = "✅" if arg.arg in used_args else "❌"
                        args.append(f"{arg.arg}: {arg_type} [{usage_status}]")
                    
                    returns = ast.unparse(sub_node.returns) if sub_node.returns else "None"
                    
                    method_signature = f"{dec_str}{sub_node.name}({', '.join(args)}) -> {returns}"
                    # メソッドの使用状況を確認
                    usage_flag = "✅ 使用あり" if sub_node.name in used_funcs else "❌ 未使用"
                    analysis += f"### メソッド: `{method_signature}` [{usage_flag}]"
                    analysis += extract_docstrings(sub_node)
                    
                    # 関数内で定義される名前の分析
                    if defined_names:
                        analysis += "\n\n**内部で定義される名前:**\n"
                        for name in sorted(defined_names):
                            analysis += f"- `{name}`\n"
                    
                    analysis += "\n\n"
                    class_methods.add(sub_node.name)

    # 関数解析（クラスメソッド以外）
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name not in class_methods:
            decorators = [ast.unparse(d) for d in node.decorator_list]
            dec_str = f"@{', @'.join(decorators)} " if decorators else ""
            
            # 関数の引数使用状況を分析
            used_args, defined_names = analyze_function_body(node)
            
            args = []
            for arg in node.args.args:
                arg_type = ast.unparse(arg.annotation) if arg.annotation else "Any"
                usage_status = "✅" if arg.arg in used_args else "❌"
                args.append(f"{arg.arg}: {arg_type} [{usage_status}]")
            
            returns = ast.unparse(node.returns) if node.returns else "None"
            
            func_signature = f"{dec_str}{node.name}({', '.join(args)}) -> {returns}"
            # 関数の使用状況を確認
            usage_flag = "✅ 使用あり" if node.name in used_funcs else "❌ 未使用"
            analysis += f"## 関数: `{func_signature}` [{usage_flag}]"
            analysis += extract_docstrings(node)
            
            # 関数内で定義される名前の分析
            if defined_names:
                analysis += "\n\n**内部で定義される名前:**\n"
                for name in sorted(defined_names):
                    analysis += f"- `{name}`\n"
            
            analysis += "\n\n"

    return analysis

def save_python_analysis():
    """Pythonファイルの解析結果を保存"""
    base_dir = Path('docs/python_analysis')
    base_dir.mkdir(parents=True, exist_ok=True)
    
    # gitignoreとcursorignoreのパターンを取得
    ignored_patterns = get_ignored_patterns()
    
    # git ls-files を使用してバージョン管理されているファイルを取得
    try:
        git_files = set(subprocess.check_output(['git', 'ls-files'], text=True).splitlines())
    except subprocess.CalledProcessError:
        git_files = set()
    
    # 解析対象のPythonファイルを収集
    python_files = set()
    for path in Path('.').rglob('*.py'):
        if path.is_file() and should_include(path, ignored_patterns):
            python_files.add(str(path))
    
    # git ls-filesの結果も追加（Pythonファイルのみ）
    python_files.update(f for f in git_files if f.endswith('.py'))
    
    # ファイルをフォルダごとにグループ化
    files_by_folder = {}
    for py_file in sorted(python_files):
        folder = Path(py_file).parent.relative_to('.')
        if folder not in files_by_folder:
            files_by_folder[folder] = []
        files_by_folder[folder].append(py_file)
    
    # フォルダごとに解析結果を保存
    for folder, files in files_by_folder.items():
        folder_name = str(folder).replace('/', '_').replace('\\', '_') or 'root'
        output_file = base_dir / f'{folder_name}_analysis.md'
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f'# {folder} フォルダのPython解析レポート\n\n')
            f.write(f'生成日時: {datetime.datetime.now()}\n\n')
            f.write('=' * 50 + '\n\n')
            
            for py_file in sorted(files):
                try:
                    analysis = analyze_python_file(str(py_file))
                    f.write(analysis)
                    f.write('\n' + '-' * 50 + '\n\n')
                except Exception as e:
                    f.write(f'### ⚠️ {py_file} の解析中にエラーが発生しました\n')
                    f.write(f'エラー: {str(e)}\n\n')

if __name__ == '__main__':
    save_python_analysis() 