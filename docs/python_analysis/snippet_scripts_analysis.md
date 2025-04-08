# snippet/scripts フォルダのPython解析レポート

生成日時: 2025-04-08 20:40:21.785236

==================================================

# __init__.py の解析結果


--------------------------------------------------

# analyze_python_files.py の解析結果

## インポート一覧
- `ast` (✅ 使用あり)
- `datetime` (✅ 使用あり)
- `pathlib.Path` (✅ 使用あり)
- `save_file_structure.get_ignored_patterns` (✅ 使用あり)
- `save_file_structure.should_include` (✅ 使用あり)
- `subprocess` (✅ 使用あり)
- `typing.Any` (❌ 未使用)
- `typing.Dict` (❌ 未使用)
- `typing.List` (❌ 未使用)
- `typing.Set` (✅ 使用あり)
- `typing.Tuple` (✅ 使用あり)

## 関数: `find_usages(node: ast.AST [✅], target_names: Set[str] [✅]) -> Set[str]` [✅ 使用あり]
**Docstring**: ASTノード内で使用されている名前を検索

**内部で定義される名前:**
- `find_usages`
- `used_names`


## 関数: `collect_function_calls(tree: ast.AST [✅]) -> Set[str]` [✅ 使用あり]
**Docstring**: ASTから関数呼び出しを収集

**内部で定義される名前:**
- `collect_function_calls`
- `func_name`
- `used_funcs`


## 関数: `analyze_function_body(node: ast.FunctionDef [✅]) -> Tuple[Set[str], Set[str]]` [✅ 使用あり]
**Docstring**: 関数本体内での変数の使用状況を分析

**内部で定義される名前:**
- `analyze_function_body`
- `arg_names`
- `defined_names`
- `used_args`


## 関数: `extract_docstrings(node: Any [✅]) -> None` [✅ 使用あり]
**Docstring**: ノードからdocstringを抽出

**内部で定義される名前:**
- `docstring`
- `extract_docstrings`


## 関数: `analyze_python_file(file_path: str [✅]) -> str` [✅ 使用あり]
**Docstring**: Pythonファイルを解析してMarkdown形式で出力

**内部で定義される名前:**
- `analysis`
- `analyze_python_file`
- `arg_type`
- `args`
- `base_str`
- `bases`
- `class_methods`
- `code`
- `dec_str`
- `decorators`
- `full_import`
- `func_signature`
- `imported_names`
- `imports`
- `method_signature`
- `name`
- `returns`
- `status`
- `tree`
- `usage`
- `usage_flag`
- `usage_status`
- `used_funcs`


## 関数: `save_python_analysis() -> None` [✅ 使用あり]
**Docstring**: Pythonファイルの解析結果を保存

**内部で定義される名前:**
- `analysis`
- `base_dir`
- `files_by_folder`
- `folder`
- `folder_name`
- `git_files`
- `ignored_patterns`
- `output_file`
- `python_files`
- `save_python_analysis`



--------------------------------------------------

# check_code_quality.py の解析結果

## インポート一覧
- `pathlib.Path` (❌ 未使用)
- `subprocess` (✅ 使用あり)
- `sys` (✅ 使用あり)

## 関数: `run_check(command: list[str] [✅], description: str [✅]) -> tuple[bool, str]` [✅ 使用あり]
**Docstring**: コマンドを実行してチェックを行う

Args:
    command (List[str]): 実行するコマンド
    description (str): チェックの説明

Returns:
    Tuple[bool, str]: チェックの結果（成功したかどうか）とエラーメッセージ

**内部で定義される名前:**
- `result`
- `run_check`


## 関数: `main() -> int` [✅ 使用あり]
**Docstring**: メイン関数

**内部で定義される名前:**
- `checks`
- `failed`
- `main`



--------------------------------------------------

# code_complexity_checker.py の解析結果

## インポート一覧
- `ast` (✅ 使用あり)
- `collections.defaultdict` (❌ 未使用)
- `os` (❌ 未使用)
- `sys` (✅ 使用あり)

## クラス: `CodeComplexityChecker`
**Docstring**: 関数の行数とネストレベルを数える簡易的なコード複雑度チェッカー

### メソッド: `__init__(self: Any [✅], max_lines: Any [✅], max_nest_level: Any [✅]) -> None` [❌ 未使用]
**Docstring**: Args:
    max_lines: 関数の最大行数の閾値
    max_nest_level: 最大ネストレベルの閾値

**内部で定義される名前:**
- `__init__`


### メソッド: `_count_lines(self: Any [❌], node: Any [✅]) -> None` [✅ 使用あり]
**Docstring**: ASTノードの行数をカウント

**内部で定義される名前:**
- `_count_lines`


### メソッド: `_get_max_nest_level(self: Any [✅], node: Any [✅], current_level: Any [✅]) -> None` [✅ 使用あり]
**Docstring**: 最大ネストレベルを計算

**内部で定義される名前:**
- `_get_max_nest_level`
- `child_level`
- `max_level`


### メソッド: `check_file(self: Any [✅], file_path: Any [✅]) -> None` [✅ 使用あり]
**Docstring**: ファイルをチェック

**内部で定義される名前:**
- `check_file`
- `code`


### メソッド: `check_code(self: Any [✅], code: Any [✅], file_name: Any [✅]) -> None` [✅ 使用あり]
**Docstring**: コード文字列をチェック

**内部で定義される名前:**
- `check_code`
- `lines`
- `max_nest`
- `name`
- `tree`


### メソッド: `print_report(self: Any [✅]) -> None` [✅ 使用あり]
**Docstring**: 結果レポートを表示

**内部で定義される名前:**
- `print_report`



--------------------------------------------------

# save_file_structure.py の解析結果

## インポート一覧
- `analyze_python_files.save_python_analysis` (✅ 使用あり)
- `datetime` (✅ 使用あり)
- `os` (✅ 使用あり)
- `pathlib.Path` (✅ 使用あり)
- `subprocess` (✅ 使用あり)

## 関数: `get_ignored_patterns() -> None` [✅ 使用あり]

**内部で定義される名前:**
- `get_ignored_patterns`
- `ignored_patterns`


## 関数: `should_include(path: Any [✅], ignored_patterns: Any [✅]) -> None` [✅ 使用あり]

**内部で定義される名前:**
- `path_str`
- `should_include`


## 関数: `format_file_structure(files: Any [✅]) -> None` [✅ 使用あり]

**内部で定義される名前:**
- `connector`
- `current`
- `dirs`
- `emoji`
- `file_tree`
- `files`
- `format_file_structure`
- `format_tree`
- `is_last_dir`
- `is_last_file`
- `new_prefix`
- `output`
- `parts`


## 関数: `save_file_structure() -> None` [✅ 使用あり]

**内部で定義される名前:**
- `all_files`
- `git_files`
- `ignored_patterns`
- `output_dir`
- `output_file`
- `save_file_structure`


## 関数: `format_tree(tree: Any [✅], prefix: Any [✅]) -> None` [✅ 使用あり]

**内部で定義される名前:**
- `connector`
- `dirs`
- `emoji`
- `files`
- `format_tree`
- `is_last_dir`
- `is_last_file`
- `new_prefix`
- `output`



--------------------------------------------------

