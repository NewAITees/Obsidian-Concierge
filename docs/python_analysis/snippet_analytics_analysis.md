# snippet/analytics フォルダのPython解析レポート

生成日時: 2025-04-08 20:40:21.595627

==================================================

# __init__.py の解析結果

## インポート一覧
- `code_analyzer.CodeAnalyzer` (❌ 未使用)
- `code_analyzer.analyze_directory` (❌ 未使用)
- `code_analyzer.analyze_file` (❌ 未使用)
- `report_generator.create_summary_report` (❌ 未使用)
- `report_generator.generate_enhanced_report` (❌ 未使用)
- `report_generator.generate_report` (❌ 未使用)
- `report_generator.save_enhanced_report` (❌ 未使用)
- `report_generator.save_report` (❌ 未使用)
- `validator_integration.validate_functions` (❌ 未使用)


--------------------------------------------------

# code_analyzer.py の解析結果

## インポート一覧
- `argparse` (✅ 使用あり)
- `datetime` (✅ 使用あり)
- `json` (✅ 使用あり)
- `os` (✅ 使用あり)
- `pathlib.Path` (✅ 使用あり)
- `scripts.analyze_python_files.analyze_python_file` (✅ 使用あり)
- `scripts.analyze_python_files.collect_function_calls` (❌ 未使用)
- `scripts.analyze_python_files.find_usages` (❌ 未使用)
- `scripts.check_code_quality.run_check` (✅ 使用あり)
- `scripts.code_complexity_checker.CodeComplexityChecker` (✅ 使用あり)
- `scripts.save_file_structure.get_ignored_patterns` (✅ 使用あり)
- `scripts.save_file_structure.should_include` (✅ 使用あり)
- `subprocess` (✅ 使用あり)
- `sys` (✅ 使用あり)
- `typing.Any` (✅ 使用あり)
- `typing.Dict` (✅ 使用あり)
- `typing.List` (✅ 使用あり)
- `typing.Optional` (✅ 使用あり)
- `typing.Set` (❌ 未使用)
- `typing.Tuple` (✅ 使用あり)
- `typing.Union` (❌ 未使用)

## クラス: `CodeAnalyzer`
**Docstring**: コードの品質と構造を分析する統合ツール

### メソッド: `__init__(self: Any [✅], max_lines: int [✅], max_nest_level: int [✅], quality_checks: Optional[List[Tuple[List[str], str]]] [✅]) -> None` [❌ 未使用]
**Docstring**: 統合コード分析ツールを初期化

Args:
    max_lines: 関数の最大行数の閾値
    max_nest_level: 最大ネストレベルの閾値
    quality_checks: 追加の品質チェック (コマンドとその説明のタプルのリスト)
                   例: [(["ruff", "check", "."], "Ruffによるコードチェック")]

**内部で定義される名前:**
- `__init__`


### メソッド: `analyze_file(self: Any [✅], file_path: str [✅]) -> Dict[str, Any]` [✅ 使用あり]
**Docstring**: 単一ファイルを分析

Args:
    file_path: 分析するファイルのパス
    
Returns:
    分析結果

**内部で定義される名前:**
- `analyze_file`
- `code`
- `file_result`
- `structure_analysis`


### メソッド: `analyze_directory(self: Any [✅], directory: str [✅], patterns: Optional[List[str]] [✅], recursive: bool [✅]) -> Dict[str, Any]` [✅ 使用あり]
**Docstring**: ディレクトリ内のファイルを分析

Args:
    directory: 分析するディレクトリ
    patterns: 分析対象ファイルのパターン（例: ['*.py']）
    recursive: サブディレクトリも再帰的に分析するかどうか
    
Returns:
    分析結果

**内部で定義される名前:**
- `analyze_directory`
- `dir_path`
- `directory_result`
- `file_result`
- `git_files`
- `ignored_patterns`
- `path`
- `patterns`
- `py_files`


### メソッド: `_generate_summary(self: Any [❌], result: Dict[str, Any] [✅]) -> Dict[str, Any]` [✅ 使用あり]
**Docstring**: 分析結果のサマリーを生成

Args:
    result: 分析結果
    
Returns:
    サマリー情報

**内部で定義される名前:**
- `_generate_summary`
- `complex_files`
- `issue_count`
- `summary`


## 関数: `run_check(command: Any [✅], description: Any [✅]) -> None` [✅ 使用あり]
**Docstring**: コマンドを実行してチェックを行う

**内部で定義される名前:**
- `result`
- `run_check`


## 関数: `get_ignored_patterns() -> None` [✅ 使用あり]
**Docstring**: 無視するパターンを取得

**内部で定義される名前:**
- `get_ignored_patterns`
- `ignored_patterns`


## 関数: `should_include(path: Any [✅], ignored_patterns: Any [✅]) -> None` [✅ 使用あり]
**Docstring**: ファイルを含めるかどうかを判定

**内部で定義される名前:**
- `path_str`
- `should_include`



--------------------------------------------------

# report_generator.py の解析結果

## インポート一覧
- `argparse` (✅ 使用あり)
- `code_analyzer.CodeAnalyzer` (✅ 使用あり)
- `code_analyzer.analyze_directory` (✅ 使用あり)
- `code_analyzer.analyze_file` (✅ 使用あり)
- `datetime` (✅ 使用あり)
- `importlib` (❌ 未使用)
- `json` (✅ 使用あり)
- `os` (✅ 使用あり)
- `pathlib.Path` (✅ 使用あり)
- `typing.Any` (✅ 使用あり)
- `typing.Dict` (✅ 使用あり)
- `typing.List` (✅ 使用あり)
- `typing.Optional` (✅ 使用あり)
- `typing.Union` (❌ 未使用)
- `validator_integration.validate_functions` (✅ 使用あり)

## 関数: `generate_report(results: Dict[str, Any] [✅], format: str [✅]) -> str` [✅ 使用あり]
**Docstring**: 分析結果からレポートを生成

Args:
    results: 分析結果の辞書
    format: 出力フォーマット ('markdown', 'html', 'json')
    
Returns:
    フォーマット済みレポート

**内部で定義される名前:**
- `generate_report`
- `html`
- `md_content`


## 関数: `_generate_file_report_md(results: Dict[str, Any] [✅]) -> str` [✅ 使用あり]
**Docstring**: 単一ファイルの分析レポートをマークダウンで生成

**内部で定義される名前:**
- `_generate_file_report_md`
- `complexity`
- `file_path`
- `issue_type`
- `issues`
- `limit`
- `lineno`
- `lines`
- `name`
- `nest_level`
- `quality`
- `report`
- `structure`


## 関数: `_generate_directory_report_md(results: Dict[str, Any] [✅]) -> str` [✅ 使用あり]
**Docstring**: ディレクトリの分析レポートをマークダウンで生成

**内部で定義される名前:**
- `_generate_directory_report_md`
- `complex_files`
- `complexity`
- `directory`
- `file_details`
- `file_name`
- `issue_type`
- `issues`
- `limit`
- `lineno`
- `lines`
- `name`
- `nest_level`
- `quality_issues`
- `report`
- `summary`


## 関数: `_generate_validator_report_md(results: Dict[str, Any] [✅]) -> str` [✅ 使用あり]
**Docstring**: 関数検証結果のレポートをマークダウンで生成

Args:
    results: 関数検証の結果
    
Returns:
    マークダウン形式のレポート

**内部で定義される名前:**
- `_generate_validator_report_md`
- `classes`
- `functions`
- `issue_type`
- `issues`
- `message`
- `method_issues`
- `methods`
- `report`
- `stats`
- `status`


## 関数: `generate_enhanced_report(code_analysis_results: Dict[str, Any] [✅], validator_results: Optional[Dict[str, Any]] [✅], format: str [✅]) -> str` [✅ 使用あり]
**Docstring**: コード分析と関数検証の結果を統合したレポートを生成

Args:
    code_analysis_results: コード分析の結果
    validator_results: 関数検証の結果（オプション）
    format: 出力フォーマット ('markdown', 'html', 'json')
    
Returns:
    フォーマット済みレポート

**内部で定義される名前:**
- `base_report`
- `combined_results`
- `generate_enhanced_report`
- `html`
- `md_report`
- `validator_report`


## 関数: `save_report(results: Dict[str, Any] [✅], output_file: str [✅], format: str [✅]) -> str` [✅ 使用あり]
**Docstring**: レポートをファイルに保存

Args:
    results: 分析結果
    output_file: 出力ファイルパス
    format: レポート形式
    
Returns:
    保存したファイルパス

**内部で定義される名前:**
- `report`
- `save_report`


## 関数: `save_enhanced_report(code_analysis_results: Dict[str, Any] [✅], validator_results: Optional[Dict[str, Any]] [✅], output_file: str [✅], format: str [✅]) -> str` [✅ 使用あり]
**Docstring**: 拡張レポートをファイルに保存

Args:
    code_analysis_results: コード分析の結果
    validator_results: 関数検証の結果（オプション）
    output_file: 出力ファイルパス
    format: レポート形式
    
Returns:
    保存したファイルパス

**内部で定義される名前:**
- `report`
- `save_enhanced_report`


## 関数: `create_summary_report(directory: str [✅], output_dir: str [✅], patterns: Optional[List[str]] [✅], recursive: bool [✅], max_lines: int [✅], max_nest_level: int [✅], validate_functions: bool [✅]) -> str` [❌ 未使用]
**Docstring**: ディレクトリの分析を実行してレポートを作成する便利関数

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

**内部で定義される名前:**
- `analyzer`
- `complex_files`
- `create_summary_report`
- `dir_name`
- `output_file`
- `results`
- `target_file`
- `timestamp`
- `validate_functions`
- `validator_results`



--------------------------------------------------

# validator_integration.py の解析結果

## インポート一覧
- `argparse` (✅ 使用あり)
- `ast` (❌ 未使用)
- `inspect` (✅ 使用あり)
- `json` (✅ 使用あり)
- `os` (✅ 使用あり)
- `pathlib.Path` (✅ 使用あり)
- `snippet.test_data_generator.TestDataGenerator` (✅ 使用あり)
- `snippet.validator.ValidationError` (✅ 使用あり)
- `snippet.validator.Validator` (✅ 使用あり)
- `sys` (✅ 使用あり)
- `typing` (❌ 未使用)
- `typing.Any` (✅ 使用あり)
- `typing.Dict` (✅ 使用あり)
- `typing.List` (✅ 使用あり)
- `typing.Optional` (❌ 未使用)
- `typing.Set` (❌ 未使用)
- `typing.Tuple` (❌ 未使用)
- `typing.Union` (❌ 未使用)
- `typing._GenericAlias` (✅ 使用あり)
- `typing._SpecialGenericAlias` (❌ 未使用)
- `typing.get_type_hints` (✅ 使用あり)

## クラス: `FunctionValidator`
**Docstring**: 関数の入出力形式を検証するバリデータ

### メソッド: `__init__(self: Any [✅], test_data_count: int [✅]) -> None` [❌ 未使用]
**Docstring**: 初期化

Args:
    test_data_count: 生成するテストデータの数

**内部で定義される名前:**
- `__init__`


### メソッド: `_generate_test_value(self: Any [✅], type_hint: Any [✅]) -> Any` [✅ 使用あり]
**Docstring**: 型ヒントに基づいてテスト値を生成

Args:
    type_hint: 型ヒント
    
Returns:
    生成された値

**内部で定義される名前:**
- `_generate_test_value`
- `element_type`


### メソッド: `generate_test_data(self: Any [✅], func: Any [✅]) -> List[Dict[str, Any]]` [✅ 使用あり]
**Docstring**: 関数のテストデータを生成

Args:
    func: 対象の関数
    
Returns:
    生成されたテストデータのリスト

**内部で定義される名前:**
- `args_data`
- `generate_test_data`
- `parameters`
- `sig`
- `test_data`
- `type_hints`


### メソッド: `validate_function_types(self: Any [❌], func: Any [✅]) -> List[Dict[str, Any]]` [✅ 使用あり]
**Docstring**: 関数の型ヒントを検証

Args:
    func: 対象の関数
    
Returns:
    検出された問題のリスト

**内部で定義される名前:**
- `issues`
- `parameters`
- `sig`
- `type_hints`
- `validate_function_types`


### メソッド: `validate_function_behavior(self: Any [✅], func: Any [✅], instance: Any [✅]) -> List[Dict[str, Any]]` [✅ 使用あり]
**Docstring**: 関数の動作を検証

Args:
    func: 対象の関数
    instance: クラスメソッドの場合のインスタンス
    
Returns:
    検出された問題のリスト

**内部で定義される名前:**
- `issues`
- `result`
- `return_type`
- `test_data_list`
- `type_hints`
- `validate_function_behavior`


### メソッド: `_validate_type(self: Any [✅], value: Any [✅], expected_type: Any [✅]) -> None` [✅ 使用あり]
**Docstring**: 値の型を検証

Args:
    value: 検証する値
    expected_type: 期待される型
    
Raises:
    ValidationError: 型が一致しない場合

**内部で定義される名前:**
- `_validate_type`
- `element_type`


### メソッド: `get_function_signature(self: Any [❌], func: Any [✅]) -> str` [✅ 使用あり]
**Docstring**: 関数のシグネチャを取得

Args:
    func: 対象の関数
    
Returns:
    関数のシグネチャ文字列

**内部で定義される名前:**
- `default_str`
- `get_function_signature`
- `params`
- `return_type`
- `return_type_str`
- `sig`
- `type_hints`
- `type_str`


### メソッド: `validate_module_functions(self: Any [✅], module_or_path: Any [✅]) -> Dict[str, Any]` [✅ 使用あり]
**Docstring**: モジュール内のすべての関数を検証

Args:
    module_or_path: モジュールまたはファイルパス
    
Returns:
    検証結果

**内部で定義される名前:**
- `behavior_issues`
- `class_info`
- `func_info`
- `instance`
- `method_info`
- `module`
- `module_name`
- `results`
- `spec`
- `type_issues`
- `validate_module_functions`


## 関数: `validate_functions(module_or_path: Any [✅], test_data_count: int [✅]) -> Dict[str, Any]` [❌ 未使用]
**Docstring**: モジュール内の関数を検証するヘルパー関数

Args:
    module_or_path: モジュールまたはファイルパス
    test_data_count: 生成するテストデータの数
    
Returns:
    検証結果

**内部で定義される名前:**
- `validate_functions`
- `validator`



--------------------------------------------------

