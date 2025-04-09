# ディレクトリ分析レポート: .

分析日時: 2025-04-09T21:36:39.530131
対象ディレクトリ: .

## サマリー
- 分析ファイル数: 48
- 問題のあるファイル数: 18
- 複雑度の問題数: 33
- 品質チェック: ❌ 失敗

## 複雑度の高いファイル
- snippet/analytics/validator_integration.py: 6件の問題
- snippet/cli.py: 5件の問題
- snippet/scripts/analyze_python_files.py: 3件の問題
- snippet/utils/config_manage.py: 3件の問題
- snippet/analytics/report_generator.py: 3件の問題

## 品質チェックの問題
- **Ruffによるコードチェック**: warning: The top-level linter settings are deprecated in favour of their counterparts in the `lint` section. Please update the following options in `pyproject.toml`:
  - 'ignore' -> 'lint.ignore'
  - 'select' -> 'lint.select'

- **MypyによるPythonの型チェック**: snippet/scripts/code_complexity_checker.py:12: error: Function is missing a type annotation  [no-untyped-def]
snippet/scripts/code_complexity_checker.py:22: error: Function is missing a type annotation  [no-untyped-def]
snippet/scripts/code_complexity_checker.py:28: error: Function is missing a type annotation  [no-untyped-def]
snippet/scripts/code_complexity_checker.py:44: error: Function is missing a type annotation  [no-untyped-def]
snippet/scripts/code_complexity_checker.py:51: error: Function is missing a type annotation  [no-untyped-def]
snippet/scripts/code_complexity_checker.py:102: error: Function is missing a return type annotation  [no-untyped-def]
snippet/scripts/code_complexity_checker.py:102: note: Use "-> None" if function does not return a value
obsidian_concierge/services/search.py:8: error: Skipping analyzing "obsidian_concierge.repository.chroma": module is installed, but missing library stubs or py.typed marker  [import-untyped]
snippet/utils/input_sanitizer.py:183: error: Incompatible types in assignment (expression has type "dict[str, Any]", target has type "str")  [assignment]
snippet/utils/input_sanitizer.py:185: error: Incompatible types in assignment (expression has type "list[Any]", target has type "str")  [assignment]
snippet/utils/input_sanitizer.py:209: error: Argument 1 to "append" of "list" has incompatible type "dict[str, Any]"; expected "str"  [arg-type]
snippet/utils/input_sanitizer.py:211: error: Argument 1 to "append" of "list" has incompatible type "list[Any]"; expected "str"  [arg-type]
snippet/utils/input_sanitizer.py:246: error: Incompatible types in assignment (expression has type "str", variable has type "int")  [assignment]
snippet/utils/logger/basic_usage.py:4: error: Cannot find implementation or library stub for module named "contextual_logger"  [import-not-found]
snippet/utils/logger/basic_usage.py:12: error: Function is missing a return type annotation  [no-untyped-def]
snippet/utils/logger/basic_usage.py:12: note: Use "-> None" if function does not return a value
snippet/utils/logger/basic_usage.py:29: error: Function is missing a return type annotation  [no-untyped-def]
snippet/utils/logger/basic_usage.py:29: note: Use "-> None" if function does not return a value
snippet/utils/logger/basic_usage.py:46: error: Function is missing a return type annotation  [no-untyped-def]
snippet/utils/logger/basic_usage.py:50: error: Function is missing a type annotation  [no-untyped-def]
snippet/utils/logger/basic_usage.py:62: error: Function is missing a return type annotation  [no-untyped-def]
snippet/utils/logger/basic_usage.py:62: note: Use "-> None" if function does not return a value
snippet/utils/logger/basic_usage.py:66: error: Function is missing a type annotation  [no-untyped-def]
snippet/utils/logger/basic_usage.py:73: error: Function is missing a return type annotation  [no-untyped-def]
snippet/utils/logger/basic_usage.py:73: note: Use "-> None" if function does not return a value
snippet/validator.py:329: error: Function is missing a type annotation  [no-untyped-def]
snippet/snippet/validator.py:329: error: Function is missing a type annotation  [no-untyped-def]
snippet/scripts/save_file_structure.py:7: error: Function is missing a return type annotation  [no-untyped-def]
snippet/scripts/save_file_structure.py:8: error: Need type annotation for "ignored_patterns" (hint: "ignored_patterns: set[<type>] = ...")  [var-annotated]
snippet/scripts/save_file_structure.py:22: error: Function is missing a type annotation  [no-untyped-def]
snippet/scripts/save_file_structure.py:29: error: Function is missing a type annotation  [no-untyped-def]
snippet/scripts/save_file_structure.py:31: error: Need type annotation for "file_tree"  [var-annotated]
snippet/scripts/save_file_structure.py:37: error: Unsupported target for indexed assignment ("Collection[Any]")  [index]
snippet/scripts/save_file_structure.py:38: error: Value of type "Collection[Any]" is not indexable  [index]
snippet/scripts/save_file_structure.py:39: error: "Collection[Any]" has no attribute "append"  [attr-defined]
snippet/scripts/save_file_structure.py:42: error: Function is missing a type annotation  [no-untyped-def]
snippet/scripts/save_file_structure.py:74: error: Function is missing a return type annotation  [no-untyped-def]
snippet/scripts/save_file_structure.py:74: note: Use "-> None" if function does not return a value
snippet/scripts/save_file_structure.py:114: error: Cannot find implementation or library stub for module named "analyze_python_files"  [import-not-found]
snippet/utils/exception_handler.py:16: error: Function is missing a type annotation  [no-untyped-def]
snippet/utils/exception_handler.py:34: error: Function is missing a type annotation  [no-untyped-def]
snippet/utils/exception_handler.py:36: error: Function is missing a type annotation  [no-untyped-def]
snippet/utils/exception_handler.py:72: error: Function is missing a type annotation  [no-untyped-def]
snippet/utils/exception_handler.py:77: error: Function is missing a type annotation  [no-untyped-def]
snippet/utils/config_manage.py:3: error: Library stubs not installed for "yaml"  [import-untyped]
snippet/utils/config_manage.py:21: error: Incompatible default for argument "config_dir" (default has type "None", argument has type "str | Path")  [assignment]
snippet/utils/config_manage.py:21: note: PEP 484 prohibits implicit Optional. Accordingly, mypy has changed its default to no_implicit_optional=True
snippet/utils/config_manage.py:21: note: Use https://github.com/hauntsaninja/no_implicit_optional to automatically upgrade your codebase
snippet/utils/config_manage.py:44: error: Need type annotation for "_config" (hint: "_config: dict[<type>, <type>] = ...")  [var-annotated]
snippet/utils/config_manage.py:71: error: Need type annotation for "merged_config" (hint: "merged_config: dict[<type>, <type>] = ...")  [var-annotated]
snippet/utils/config_manage.py:205: error: Returning Any from function declared to return "dict[str, Any]"  [no-any-return]
snippet/scripts/analyze_python_files.py:51: error: Function is missing a type annotation  [no-untyped-def]
snippet/scripts/analyze_python_files.py:86: error: Incompatible types in assignment (expression has type "str", variable has type "alias")  [assignment]
snippet/scripts/analyze_python_files.py:87: error: Argument 1 to <set> has incompatible type "alias"; expected "str"  [arg-type]
snippet/scripts/analyze_python_files.py:127: error: Incompatible types in assignment (expression has type "str", variable has type "alias")  [assignment]
snippet/scripts/analyze_python_files.py:159: error: Incompatible types in assignment (expression has type "str", variable has type "alias")  [assignment]
snippet/scripts/analyze_python_files.py:166: error: Function is missing a return type annotation  [no-untyped-def]
snippet/scripts/analyze_python_files.py:166: note: Use "-> None" if function does not return a value
snippet/scripts/analyze_python_files.py:190: error: Need type annotation for "files_by_folder" (hint: "files_by_folder: dict[<type>, <type>] = ...")  [var-annotated]
snippet/test_data_generator.py:94: error: Need type annotation for "custom_builders" (hint: "custom_builders: dict[<type>, <type>] = ...")  [var-annotated]
snippet/test_data_generator.py:96: error: Function is missing a type annotation for one or more arguments  [no-untyped-def]
snippet/test_data_generator.py:120: error: Function is missing a type annotation for one or more arguments  [no-untyped-def]
snippet/test_data_generator.py:151: error: Name "get_logger" is not defined  [name-defined]
snippet/test_data_generator.py:167: error: Function is missing a return type annotation  [no-untyped-def]
snippet/test_data_generator.py:191: error: Function is missing a type annotation  [no-untyped-def]
snippet/test_data_generator.py:197: error: Function is missing a type annotation  [no-untyped-def]
snippet/utils/safe_file_ops.py:43: error: Returning Any from function declared to return "str"  [no-any-return]
snippet/utils/safe_file_ops.py:189: error: Returning Any from function declared to return "dict[str, Any]"  [no-any-return]
snippet/utils/safe_file_ops.py:192: error: Returning Any from function declared to return "dict[str, Any]"  [no-any-return]
snippet/utils/safe_file_ops.py:238: error: Incompatible types in assignment (expression has type "Reader", variable has type "DictReader[str]")  [assignment]
snippet/utils/safe_file_ops.py:413: error: Function is missing a type annotation  [no-untyped-def]
snippet/utils/logger/contextual_logger.py:18: error: Function is missing a type annotation  [no-untyped-def]
snippet/utils/logger/contextual_logger.py:79: error: Function is missing a return type annotation  [no-untyped-def]
snippet/utils/logger/contextual_logger.py:81: error: Item "None" of "FrameType | None" has no attribute "f_back"  [union-attr]
snippet/utils/logger/contextual_logger.py:81: error: Item "None" of "FrameType | Any | None" has no attribute "f_back"  [union-attr]
snippet/utils/logger/contextual_logger.py:82: error: Item "None" of "FrameType | Any | None" has no attribute "f_code"  [union-attr]
snippet/utils/logger/contextual_logger.py:83: error: Item "None" of "FrameType | Any | None" has no attribute "f_code"  [union-attr]
snippet/utils/logger/contextual_logger.py:84: error: Item "None" of "FrameType | Any | None" has no attribute "f_lineno"  [union-attr]
snippet/utils/logger/contextual_logger.py:94: error: Function is missing a type annotation  [no-untyped-def]
snippet/utils/logger/contextual_logger.py:108: error: Function is missing a type annotation  [no-untyped-def]
snippet/utils/logger/contextual_logger.py:121: error: Function is missing a type annotation  [no-untyped-def]
snippet/utils/logger/contextual_logger.py:125: error: Function is missing a type annotation  [no-untyped-def]
snippet/utils/logger/contextual_logger.py:129: error: Function is missing a type annotation  [no-untyped-def]
snippet/utils/logger/contextual_logger.py:133: error: Function is missing a type annotation  [no-untyped-def]
snippet/utils/logger/contextual_logger.py:140: error: Function is missing a type annotation  [no-untyped-def]
snippet/utils/logger/contextual_logger.py:147: error: Function is missing a type annotation  [no-untyped-def]
snippet/utils/logger/contextual_logger.py:155: error: Function is missing a type annotation  [no-untyped-def]
snippet/utils/logger/contextual_logger.py:158: error: Function is missing a type annotation  [no-untyped-def]
snippet/utils/logger/contextual_logger.py:173: error: Function is missing a type annotation  [no-untyped-def]
snippet/utils/logger/contextual_logger.py:202: error: Function is missing a return type annotation  [no-untyped-def]
snippet/utils/__init__.py:7: error: Skipping analyzing "snippet.utils.file_utils": module is installed, but missing library stubs or py.typed marker  [import-untyped]
snippet/utils/__init__.py:9: error: Skipping analyzing "snippet.utils.validator": module is installed, but missing library stubs or py.typed marker  [import-untyped]
snippet/snippet/test_data_generator.py:94: error: Need type annotation for "custom_builders" (hint: "custom_builders: dict[<type>, <type>] = ...")  [var-annotated]
snippet/snippet/test_data_generator.py:96: error: Function is missing a type annotation for one or more arguments  [no-untyped-def]
snippet/snippet/test_data_generator.py:120: error: Function is missing a type annotation for one or more arguments  [no-untyped-def]
snippet/snippet/test_data_generator.py:151: error: Name "get_logger" is not defined  [name-defined]
snippet/snippet/test_data_generator.py:167: error: Function is missing a return type annotation  [no-untyped-def]
snippet/snippet/test_data_generator.py:191: error: Function is missing a type annotation  [no-untyped-def]
snippet/snippet/test_data_generator.py:197: error: Function is missing a type annotation  [no-untyped-def]
snippet/analytics/validator_integration.py:21: error: Module "typing" has no attribute "_GenericAlias"; maybe "GenericAlias"?  [attr-defined]
snippet/analytics/validator_integration.py:24: error: Module "typing" has no attribute "_SpecialGenericAlias"  [attr-defined]
snippet/analytics/validator_integration.py:45: error: Need type annotation for "issues" (hint: "issues: list[<type>] = ...")  [var-annotated]
snippet/analytics/validator_integration.py:102: error: Function is missing a type annotation for one or more arguments  [no-untyped-def]
snippet/analytics/validator_integration.py:145: error: Function is missing a type annotation for one or more arguments  [no-untyped-def]
snippet/analytics/validator_integration.py:192: error: Function is missing a type annotation for one or more arguments  [no-untyped-def]
snippet/analytics/validator_integration.py:305: error: Function is missing a type annotation for one or more arguments  [no-untyped-def]
snippet/analytics/validator_integration.py:350: error: Function is missing a type annotation for one or more arguments  [no-untyped-def]
snippet/analytics/validator_integration.py:379: error: Name "importlib" is not defined  [name-defined]
snippet/analytics/validator_integration.py:380: error: Name "importlib" is not defined  [name-defined]
snippet/analytics/validator_integration.py:401: error: Value of type "Collection[str]" is not indexable  [index]
snippet/analytics/validator_integration.py:401: error: Unsupported target for indexed assignment ("Collection[str]")  [index]
snippet/analytics/validator_integration.py:414: error: "Sequence[str]" has no attribute "extend"  [attr-defined]
snippet/analytics/validator_integration.py:415: error: Value of type "Collection[str]" is not indexable  [index]
snippet/analytics/validator_integration.py:415: error: Unsupported target for indexed assignment ("Collection[str]")  [index]
snippet/analytics/validator_integration.py:421: error: "Sequence[str]" has no attribute "extend"  [attr-defined]
snippet/analytics/validator_integration.py:422: error: Value of type "Collection[str]" is not indexable  [index]
snippet/analytics/validator_integration.py:422: error: Unsupported target for indexed assignment ("Collection[str]")  [index]
snippet/analytics/validator_integration.py:424: error: "Sequence[str]" has no attribute "append"  [attr-defined]
snippet/analytics/validator_integration.py:431: error: Value of type "Collection[str]" is not indexable  [index]
snippet/analytics/validator_integration.py:431: error: Unsupported target for indexed assignment ("Collection[str]")  [index]
snippet/analytics/validator_integration.py:434: error: "Collection[str]" has no attribute "append"  [attr-defined]
snippet/analytics/validator_integration.py:455: error: "Sequence[str]" has no attribute "append"  [attr-defined]
snippet/analytics/validator_integration.py:466: error: Value of type "Collection[str]" is not indexable  [index]
snippet/analytics/validator_integration.py:466: error: Unsupported target for indexed assignment ("Collection[str]")  [index]
snippet/analytics/validator_integration.py:479: error: "Sequence[str]" has no attribute "extend"  [attr-defined]
snippet/analytics/validator_integration.py:480: error: Value of type "Collection[str]" is not indexable  [index]
snippet/analytics/validator_integration.py:480: error: Unsupported target for indexed assignment ("Collection[str]")  [index]
snippet/analytics/validator_integration.py:487: error: "Sequence[str]" has no attribute "extend"  [attr-defined]
snippet/analytics/validator_integration.py:488: error: Value of type "Collection[str]" is not indexable  [index]
snippet/analytics/validator_integration.py:488: error: Unsupported target for indexed assignment ("Collection[str]")  [index]
snippet/analytics/validator_integration.py:490: error: "Sequence[str]" has no attribute "append"  [attr-defined]
snippet/analytics/validator_integration.py:497: error: Value of type "Collection[str]" is not indexable  [index]
snippet/analytics/validator_integration.py:497: error: Unsupported target for indexed assignment ("Collection[str]")  [index]
snippet/analytics/validator_integration.py:500: error: "Sequence[str]" has no attribute "append"  [attr-defined]
snippet/analytics/validator_integration.py:503: error: "Collection[str]" has no attribute "append"  [attr-defined]
snippet/analytics/validator_integration.py:508: error: Function is missing a type annotation for one or more arguments  [no-untyped-def]
obsidian_concierge/utils/config.py:12: error: Library stubs not installed for "yaml"  [import-untyped]
obsidian_concierge/utils/config.py:12: note: Hint: "python3 -m pip install types-PyYAML"
obsidian_concierge/utils/config.py:12: note: (or run "mypy --install-types" to install all missing stub packages)
obsidian_concierge/utils/config.py:70: error: Need type annotation for "config_data" (hint: "config_data: dict[<type>, <type>] = ...")  [var-annotated]
obsidian_concierge/utils/config.py:74: error: Incompatible types in assignment (expression has type "Path", variable has type "str | None")  [assignment]
obsidian_concierge/utils/config.py:75: error: "str" has no attribute "exists"  [attr-defined]
obsidian_concierge/utils/config.py:82: error: "Callable[[BaseModel], dict[str, FieldInfo]]" has no attribute "__iter__" (not iterable)  [attr-defined]
obsidian_concierge/utils/config.py:87: error: Argument 1 to "AppConfig" has incompatible type "**dict[Any, str]"; expected "int"  [arg-type]
snippet/analytics/code_analyzer.py:14: error: Library stubs not installed for "tqdm"  [import-untyped]
snippet/analytics/code_analyzer.py:14: note: Hint: "python3 -m pip install types-tqdm"
snippet/analytics/code_analyzer.py:23: error: Function is missing a type annotation  [no-untyped-def]
snippet/analytics/code_analyzer.py:23: error: All conditional function variants must have identical signatures  [misc]
snippet/analytics/code_analyzer.py:23: note: Original:
snippet/analytics/code_analyzer.py:23: note:     def run_check(command: list[str], description: str) -> tuple[bool, str]
snippet/analytics/code_analyzer.py:23: note: Redefinition:
snippet/analytics/code_analyzer.py:23: note:     def run_check(command: Any, description: Any) -> Any
snippet/analytics/code_analyzer.py:45: error: Function is missing a return type annotation  [no-untyped-def]
snippet/analytics/code_analyzer.py:47: error: Need type annotation for "ignored_patterns" (hint: "ignored_patterns: set[<type>] = ...")  [var-annotated]
snippet/analytics/code_analyzer.py:61: error: Function is missing a type annotation  [no-untyped-def]
snippet/analytics/code_analyzer.py:109: error: Need type annotation for "results" (hint: "results: dict[<type>, <type>] = ...")  [var-annotated]
snippet/analytics/code_analyzer.py:152: error: Unsupported target for indexed assignment ("Collection[str]")  [index]
snippet/analytics/code_analyzer.py:153: error: Value of type "Collection[str]" is not indexable  [index]
snippet/analytics/code_analyzer.py:236: error: Unsupported target for indexed assignment ("object")  [index]
snippet/analytics/code_analyzer.py:239: error: Unsupported target for indexed assignment ("object")  [index]
snippet/analytics/code_analyzer.py:250: error: Unsupported target for indexed assignment ("object")  [index]
snippet/analytics/code_analyzer.py:251: error: Value of type "object" is not indexable  [index]
snippet/cli.py:15: error: Library stubs not installed for "tqdm"  [import-untyped]
snippet/cli.py:28: error: Incompatible default for argument "output_file" (default has type "None", argument has type "str")  [assignment]
snippet/cli.py:28: note: PEP 484 prohibits implicit Optional. Accordingly, mypy has changed its default to no_implicit_optional=True
snippet/cli.py:28: note: Use https://github.com/hauntsaninja/no_implicit_optional to automatically upgrade your codebase
snippet/cli.py:215: error: Incompatible default for argument "max_workers" (default has type "None", argument has type "int")  [assignment]
snippet/cli.py:215: note: PEP 484 prohibits implicit Optional. Accordingly, mypy has changed its default to no_implicit_optional=True
snippet/cli.py:215: note: Use https://github.com/hauntsaninja/no_implicit_optional to automatically upgrade your codebase
snippet/cli.py:254: error: Unsupported target for indexed assignment ("dict[str, int] | None")  [index]
snippet/cli.py:254: error: Incompatible types in assignment (expression has type "dict[str, Any]", target has type "int")  [assignment]
snippet/cli.py:258: error: Value of type "dict[str, int] | None" is not indexable  [index]
snippet/cli.py:258: error: Unsupported target for indexed assignment ("dict[str, int] | None")  [index]
snippet/cli.py:259: error: Value of type "dict[str, int] | None" is not indexable  [index]
snippet/cli.py:259: error: Unsupported target for indexed assignment ("dict[str, int] | None")  [index]
snippet/cli.py:261: error: Unsupported target for indexed assignment ("dict[str, int] | None")  [index]
snippet/cli.py:265: error: Unsupported target for indexed assignment ("dict[str, int] | None")  [index]
snippet/cli.py:265: error: Incompatible types in assignment (expression has type "dict[str, str]", target has type "int")  [assignment]
snippet/cli.py:341: error: Incompatible types in assignment (expression has type "Namespace", variable has type "list[str] | None")  [assignment]
snippet/cli.py:344: error: Item "list[str]" of "list[str] | None" has no attribute "command"  [union-attr]
snippet/cli.py:344: error: Item "None" of "list[str] | None" has no attribute "command"  [union-attr]
snippet/cli.py:345: error: Item "list[str]" of "list[str] | None" has no attribute "path"  [union-attr]
snippet/cli.py:345: error: Item "None" of "list[str] | None" has no attribute "path"  [union-attr]
snippet/cli.py:352: error: Item "list[str]" of "list[str] | None" has no attribute "max_lines"  [union-attr]
snippet/cli.py:352: error: Item "None" of "list[str] | None" has no attribute "max_lines"  [union-attr]
snippet/cli.py:353: error: Item "list[str]" of "list[str] | None" has no attribute "max_nest"  [union-attr]
snippet/cli.py:353: error: Item "None" of "list[str] | None" has no attribute "max_nest"  [union-attr]
snippet/cli.py:360: error: Item "list[str]" of "list[str] | None" has no attribute "max_lines"  [union-attr]
snippet/cli.py:360: error: Item "None" of "list[str] | None" has no attribute "max_lines"  [union-attr]
snippet/cli.py:361: error: Item "list[str]" of "list[str] | None" has no attribute "max_nest"  [union-attr]
snippet/cli.py:361: error: Item "None" of "list[str] | None" has no attribute "max_nest"  [union-attr]
snippet/cli.py:362: error: Item "list[str]" of "list[str] | None" has no attribute "skip_quality_checks"  [union-attr]
snippet/cli.py:362: error: Item "None" of "list[str] | None" has no attribute "skip_quality_checks"  [union-attr]
snippet/cli.py:367: error: Item "list[str]" of "list[str] | None" has no attribute "patterns"  [union-attr]
snippet/cli.py:367: error: Item "None" of "list[str] | None" has no attribute "patterns"  [union-attr]
snippet/cli.py:368: error: Item "list[str]" of "list[str] | None" has no attribute "recursive"  [union-attr]
snippet/cli.py:368: error: Item "None" of "list[str] | None" has no attribute "recursive"  [union-attr]
snippet/cli.py:375: error: Item "list[str]" of "list[str] | None" has no attribute "validate_functions"  [union-attr]
snippet/cli.py:375: error: Item "None" of "list[str] | None" has no attribute "validate_functions"  [union-attr]
snippet/cli.py:384: error: Item "list[str]" of "list[str] | None" has no attribute "output"  [union-attr]
snippet/cli.py:384: error: Item "None" of "list[str] | None" has no attribute "output"  [union-attr]
snippet/cli.py:392: error: Item "list[str]" of "list[str] | None" has no attribute "output"  [union-attr]
snippet/cli.py:392: error: Item "None" of "list[str] | None" has no attribute "output"  [union-attr]
snippet/cli.py:393: error: Item "list[str]" of "list[str] | None" has no attribute "output"  [union-attr]
snippet/cli.py:393: error: Item "None" of "list[str] | None" has no attribute "output"  [union-attr]
snippet/cli.py:396: error: Item "list[str]" of "list[str] | None" has no attribute "output"  [union-attr]
snippet/cli.py:396: error: Item "None" of "list[str] | None" has no attribute "output"  [union-attr]
snippet/cli.py:399: error: Item "list[str]" of "list[str] | None" has no attribute "report"  [union-attr]
snippet/cli.py:399: error: Item "None" of "list[str] | None" has no attribute "report"  [union-attr]
snippet/cli.py:400: error: Item "list[str]" of "list[str] | None" has no attribute "report"  [union-attr]
snippet/cli.py:400: error: Item "None" of "list[str] | None" has no attribute "report"  [union-attr]
snippet/cli.py:405: error: Item "list[str]" of "list[str] | None" has no attribute "report"  [union-attr]
snippet/cli.py:405: error: Item "None" of "list[str] | None" has no attribute "report"  [union-attr]
snippet/cli.py:406: error: Item "list[str]" of "list[str] | None" has no attribute "format"  [union-attr]
snippet/cli.py:406: error: Item "None" of "list[str] | None" has no attribute "format"  [union-attr]
snippet/cli.py:409: error: Item "list[str]" of "list[str] | None" has no attribute "report"  [union-attr]
snippet/cli.py:409: error: Item "None" of "list[str] | None" has no attribute "report"  [union-attr]
snippet/cli.py:409: error: Item "list[str]" of "list[str] | None" has no attribute "format"  [union-attr]
snippet/cli.py:409: error: Item "None" of "list[str] | None" has no attribute "format"  [union-attr]
snippet/cli.py:435: error: Item "list[str]" of "list[str] | None" has no attribute "command"  [union-attr]
snippet/cli.py:435: error: Item "None" of "list[str] | None" has no attribute "command"  [union-attr]
snippet/cli.py:436: error: Item "list[str]" of "list[str] | None" has no attribute "path"  [union-attr]
snippet/cli.py:436: error: Item "None" of "list[str] | None" has no attribute "path"  [union-attr]
snippet/cli.py:441: error: Item "list[str]" of "list[str] | None" has no attribute "test_count"  [union-attr]
snippet/cli.py:441: error: Item "None" of "list[str] | None" has no attribute "test_count"  [union-attr]
snippet/cli.py:445: error: Item "list[str]" of "list[str] | None" has no attribute "output"  [union-attr]
snippet/cli.py:445: error: Item "None" of "list[str] | None" has no attribute "output"  [union-attr]
snippet/cli.py:447: error: Item "list[str]" of "list[str] | None" has no attribute "output"  [union-attr]
snippet/cli.py:447: error: Item "None" of "list[str] | None" has no attribute "output"  [union-attr]
snippet/cli.py:449: error: Item "list[str]" of "list[str] | None" has no attribute "output"  [union-attr]
snippet/cli.py:449: error: Item "None" of "list[str] | None" has no attribute "output"  [union-attr]
snippet/cli.py:452: error: Item "list[str]" of "list[str] | None" has no attribute "report"  [union-attr]
snippet/cli.py:452: error: Item "None" of "list[str] | None" has no attribute "report"  [union-attr]
snippet/cli.py:453: error: Item "list[str]" of "list[str] | None" has no attribute "format"  [union-attr]
snippet/cli.py:453: error: Item "None" of "list[str] | None" has no attribute "format"  [union-attr]
snippet/cli.py:455: error: Item "list[str]" of "list[str] | None" has no attribute "report"  [union-attr]
snippet/cli.py:455: error: Item "None" of "list[str] | None" has no attribute "report"  [union-attr]
snippet/cli.py:457: error: Item "list[str]" of "list[str] | None" has no attribute "report"  [union-attr]
snippet/cli.py:457: error: Item "None" of "list[str] | None" has no attribute "report"  [union-attr]
snippet/cli.py:477: error: Item "list[str]" of "list[str] | None" has no attribute "command"  [union-attr]
snippet/cli.py:477: error: Item "None" of "list[str] | None" has no attribute "command"  [union-attr]
snippet/cli.py:481: error: Item "list[str]" of "list[str] | None" has no attribute "code_analysis"  [union-attr]
snippet/cli.py:481: error: Item "None" of "list[str] | None" has no attribute "code_analysis"  [union-attr]
snippet/cli.py:486: error: Item "list[str]" of "list[str] | None" has no attribute "validator_results"  [union-attr]
snippet/cli.py:486: error: Item "None" of "list[str] | None" has no attribute "validator_results"  [union-attr]
snippet/cli.py:487: error: Item "list[str]" of "list[str] | None" has no attribute "validator_results"  [union-attr]
snippet/cli.py:487: error: Item "None" of "list[str] | None" has no attribute "validator_results"  [union-attr]
snippet/cli.py:494: error: Item "list[str]" of "list[str] | None" has no attribute "output"  [union-attr]
snippet/cli.py:494: error: Item "None" of "list[str] | None" has no attribute "output"  [union-attr]
snippet/cli.py:495: error: Item "list[str]" of "list[str] | None" has no attribute "format"  [union-attr]
snippet/cli.py:495: error: Item "None" of "list[str] | None" has no attribute "format"  [union-attr]
snippet/cli.py:501: error: Item "list[str]" of "list[str] | None" has no attribute "command"  [union-attr]
snippet/cli.py:501: error: Item "None" of "list[str] | None" has no attribute "command"  [union-attr]
snippet/cli.py:503: error: Item "list[str]" of "list[str] | None" has no attribute "results"  [union-attr]
snippet/cli.py:503: error: Item "None" of "list[str] | None" has no attribute "results"  [union-attr]
snippet/cli.py:504: error: Item "list[str]" of "list[str] | None" has no attribute "results"  [union-attr]
snippet/cli.py:504: error: Item "None" of "list[str] | None" has no attribute "results"  [union-attr]
snippet/cli.py:505: error: Name "json" is used before definition  [used-before-def]
snippet/cli.py:507: error: Item "list[str]" of "list[str] | None" has no attribute "output"  [union-attr]
snippet/cli.py:507: error: Item "None" of "list[str] | None" has no attribute "output"  [union-attr]
snippet/cli.py:507: error: Item "list[str]" of "list[str] | None" has no attribute "format"  [union-attr]
snippet/cli.py:507: error: Item "None" of "list[str] | None" has no attribute "format"  [union-attr]
snippet/cli.py:511: error: Item "list[str]" of "list[str] | None" has no attribute "command"  [union-attr]
snippet/cli.py:511: error: Item "None" of "list[str] | None" has no attribute "command"  [union-attr]
snippet/cli.py:513: error: Item "list[str]" of "list[str] | None" has no attribute "path"  [union-attr]
snippet/cli.py:513: error: Item "None" of "list[str] | None" has no attribute "path"  [union-attr]
snippet/cli.py:521: error: Item "list[str]" of "list[str] | None" has no attribute "patterns"  [union-attr]
snippet/cli.py:521: error: Item "None" of "list[str] | None" has no attribute "patterns"  [union-attr]
snippet/cli.py:522: error: Item "list[str]" of "list[str] | None" has no attribute "recursive"  [union-attr]
snippet/cli.py:522: error: Item "None" of "list[str] | None" has no attribute "recursive"  [union-attr]
snippet/testing/test_all.py:5: error: Library stubs not installed for "yaml"  [import-untyped]
snippet/testing/test_all.py:9: error: Skipping analyzing "snippet.utils.logger.config_manage": module is installed, but missing library stubs or py.typed marker  [import-untyped]
snippet/testing/test_all.py:12: error: Cannot find implementation or library stub for module named "validator"  [import-not-found]
snippet/testing/test_all.py:13: error: Cannot find implementation or library stub for module named "test_data_generator"  [import-not-found]
snippet/testing/test_all.py:14: error: Cannot find implementation or library stub for module named "scripts.code_complexity_checker"  [import-not-found]
snippet/testing/test_all.py:16: error: Cannot find implementation or library stub for module named "logger.contextual_logger"  [import-not-found]
snippet/testing/test_all.py:20: error: Function is missing a return type annotation  [no-untyped-def]
snippet/testing/test_all.py:20: note: Use "-> None" if function does not return a value
snippet/testing/test_all.py:23: error: Function is missing a return type annotation  [no-untyped-def]
snippet/testing/test_all.py:23: note: Use "-> None" if function does not return a value
snippet/testing/test_all.py:28: error: Function is missing a return type annotation  [no-untyped-def]
snippet/testing/test_all.py:28: note: Use "-> None" if function does not return a value
snippet/testing/test_all.py:33: error: Function is missing a return type annotation  [no-untyped-def]
snippet/testing/test_all.py:33: note: Use "-> None" if function does not return a value
snippet/testing/test_all.py:39: error: Function is missing a return type annotation  [no-untyped-def]
snippet/testing/test_all.py:39: note: Use "-> None" if function does not return a value
snippet/testing/test_all.py:45: error: Function is missing a return type annotation  [no-untyped-def]
snippet/testing/test_all.py:45: note: Use "-> None" if function does not return a value
snippet/testing/test_all.py:53: error: Function is missing a return type annotation  [no-untyped-def]
snippet/testing/test_all.py:53: note: Use "-> None" if function does not return a value
snippet/testing/test_all.py:57: error: Function is missing a return type annotation  [no-untyped-def]
snippet/testing/test_all.py:57: note: Use "-> None" if function does not return a value
snippet/testing/test_all.py:61: error: Function is missing a return type annotation  [no-untyped-def]
snippet/testing/test_all.py:61: note: Use "-> None" if function does not return a value
snippet/testing/test_all.py:83: error: Function is missing a return type annotation  [no-untyped-def]
snippet/testing/test_all.py:83: note: Use "-> None" if function does not return a value
snippet/testing/test_all.py:89: error: Function is missing a return type annotation  [no-untyped-def]
snippet/testing/test_all.py:89: note: Use "-> None" if function does not return a value
snippet/testing/test_all.py:96: error: Function is missing a return type annotation  [no-untyped-def]
snippet/testing/test_all.py:96: note: Use "-> None" if function does not return a value
snippet/testing/test_all.py:103: error: Function is missing a return type annotation  [no-untyped-def]
snippet/testing/test_all.py:103: note: Use "-> None" if function does not return a value
snippet/testing/test_all.py:110: error: Function is missing a return type annotation  [no-untyped-def]
snippet/testing/test_all.py:110: note: Use "-> None" if function does not return a value
snippet/testing/test_all.py:113: error: Function is missing a return type annotation  [no-untyped-def]
snippet/testing/test_all.py:113: note: Use "-> None" if function does not return a value
snippet/testing/test_all.py:119: error: Function is missing a return type annotation  [no-untyped-def]
snippet/testing/test_all.py:119: note: Use "-> None" if function does not return a value
snippet/testing/test_all.py:124: error: Function is missing a return type annotation  [no-untyped-def]
snippet/testing/test_all.py:124: note: Use "-> None" if function does not return a value
snippet/testing/test_all.py:128: error: Function is missing a return type annotation  [no-untyped-def]
snippet/testing/test_all.py:128: note: Use "-> None" if function does not return a value
snippet/testing/test_all.py:135: error: Function is missing a return type annotation  [no-untyped-def]
snippet/testing/test_all.py:135: note: Use "-> None" if function does not return a value
snippet/testing/test_all.py:138: error: Function is missing a return type annotation  [no-untyped-def]
snippet/testing/test_all.py:138: note: Use "-> None" if function does not return a value
snippet/testing/test_all.py:146: error: Function is missing a return type annotation  [no-untyped-def]
snippet/testing/test_all.py:146: note: Use "-> None" if function does not return a value
snippet/testing/test_all.py:159: error: Function is missing a return type annotation  [no-untyped-def]
snippet/testing/test_all.py:161: error: Function is missing a type annotation  [no-untyped-def]
snippet/testing/test_all.py:167: error: Function is missing a return type annotation  [no-untyped-def]
snippet/testing/test_all.py:169: error: Function is missing a type annotation  [no-untyped-def]
snippet/testing/test_all.py:177: error: Function is missing a return type annotation  [no-untyped-def]
snippet/testing/test_all.py:177: note: Use "-> None" if function does not return a value
snippet/testing/test_all.py:181: error: Function is missing a return type annotation  [no-untyped-def]
snippet/testing/test_all.py:181: note: Use "-> None" if function does not return a value
snippet/testing/test_all.py:185: error: Function is missing a return type annotation  [no-untyped-def]
snippet/testing/test_all.py:185: note: Use "-> None" if function does not return a value
snippet/testing/test_all.py:198: error: Function is missing a return type annotation  [no-untyped-def]
snippet/testing/test_all.py:198: note: Use "-> None" if function does not return a value
snippet/testing/test_all.py:233: error: Function is missing a return type annotation  [no-untyped-def]
snippet/testing/test_all.py:233: note: Use "-> None" if function does not return a value
snippet/testing/test_all.py:237: error: Function is missing a return type annotation  [no-untyped-def]
snippet/testing/test_all.py:237: note: Use "-> None" if function does not return a value
snippet/testing/test_all.py:248: error: Function is missing a return type annotation  [no-untyped-def]
snippet/testing/test_all.py:248: note: Use "-> None" if function does not return a value
snippet/testing/test_all.py:259: error: Function is missing a return type annotation  [no-untyped-def]
snippet/testing/test_all.py:259: note: Use "-> None" if function does not return a value
snippet/testing/test_all.py:272: error: Function is missing a return type annotation  [no-untyped-def]
snippet/testing/test_all.py:272: note: Use "-> None" if function does not return a value
snippet/testing/test_all.py:294: error: Function is missing a return type annotation  [no-untyped-def]
snippet/testing/test_all.py:294: note: Use "-> None" if function does not return a value
snippet/testing/test_all.py:299: error: Function is missing a return type annotation  [no-untyped-def]
snippet/testing/test_all.py:299: note: Use "-> None" if function does not return a value
snippet/testing/test_all.py:300: error: Cannot find implementation or library stub for module named "save_file_structure"  [import-not-found]
snippet/testing/test_all.py:321: error: Function is missing a return type annotation  [no-untyped-def]
snippet/testing/test_all.py:321: note: Use "-> None" if function does not return a value
tests/test_utils/test_fs.py:16: error: Function is missing a return type annotation  [no-untyped-def]
tests/test_utils/test_fs.py:16: note: Use "-> None" if function does not return a value
tests/test_utils/test_fs.py:27: error: Function is missing a return type annotation  [no-untyped-def]
tests/test_utils/test_fs.py:27: note: Use "-> None" if function does not return a value
tests/test_utils/test_fs.py:52: error: Function is missing a return type annotation  [no-untyped-def]
tests/test_utils/test_fs.py:52: note: Use "-> None" if function does not return a value
tests/test_utils/test_fs.py:72: error: Function is missing a return type annotation  [no-untyped-def]
tests/test_utils/test_fs.py:72: note: Use "-> None" if function does not return a value
tests/test_utils/test_fs.py:81: error: Function is missing a return type annotation  [no-untyped-def]
tests/test_utils/test_fs.py:81: note: Use "-> None" if function does not return a value
tests/test_utils/test_fs.py:97: error: Function is missing a return type annotation  [no-untyped-def]
tests/test_utils/test_fs.py:97: note: Use "-> None" if function does not return a value
tests/test_utils/test_config.py:7: error: Library stubs not installed for "yaml"  [import-untyped]
tests/test_utils/test_config.py:14: error: Function is missing a type annotation  [no-untyped-def]
tests/test_utils/test_config.py:37: error: Function is missing a return type annotation  [no-untyped-def]
tests/test_utils/test_config.py:37: note: Use "-> None" if function does not return a value
tests/test_utils/test_config.py:61: error: Function is missing a type annotation  [no-untyped-def]
tests/test_utils/test_config.py:78: error: Function is missing a return type annotation  [no-untyped-def]
tests/test_utils/test_config.py:78: note: Use "-> None" if function does not return a value
tests/test_utils/test_config.py:109: error: Function is missing a type annotation  [no-untyped-def]
tests/test_utils/test_config.py:118: error: Function is missing a return type annotation  [no-untyped-def]
tests/test_utils/test_config.py:118: note: Use "-> None" if function does not return a value
tests/test_utils/test_config.py:124: error: Function is missing a type annotation  [no-untyped-def]
obsidian_concierge/main.py:43: error: Function is missing a return type annotation  [no-untyped-def]
obsidian_concierge/main.py:48: error: Function is missing a return type annotation  [no-untyped-def]
obsidian_concierge/main.py:48: note: Use "-> None" if function does not return a value
obsidian_concierge/llm/ollama.py:80: error: Incompatible types in assignment (expression has type "list[str]", target has type "float")  [assignment]
obsidian_concierge/llm/ollama.py:105: error: Returning Any from function declared to return "str"  [no-any-return]
obsidian_concierge/llm/ollama.py:188: error: Returning Any from function declared to return "list[float]"  [no-any-return]
obsidian_concierge/db/chroma.py:25: error: Function is missing a type annotation for one or more arguments  [no-untyped-def]
obsidian_concierge/db/chroma.py:73: error: Argument "metadatas" to "add" of "Collection" has incompatible type "list[dict[str, Any]]"; expected "Mapping[str, str | int | float | bool] | list[Mapping[str, str | int | float | bool]] | None"  [arg-type]
obsidian_concierge/db/chroma.py:111: error: Value of type "list[list[str]] | None" is not indexable  [index]
obsidian_concierge/db/chroma.py:112: error: Argument "metadata" to "Document" has incompatible type "Mapping[str, str | int | float | bool]"; expected "dict[str, Any]"  [arg-type]
tests/test_db/test_chroma.py:13: error: Function is missing a return type annotation  [no-untyped-def]
tests/test_db/test_chroma.py:43: error: Function is missing a return type annotation  [no-untyped-def]
tests/test_db/test_chroma.py:50: error: "ChromaRepository" has no attribute "get_document"; maybe "delete_documents"?  [attr-defined]
tests/test_db/test_chroma.py:57: error: Function is missing a return type annotation  [no-untyped-def]
tests/test_db/test_chroma.py:76: error: Function is missing a return type annotation  [no-untyped-def]
tests/test_db/test_chroma.py:90: error: "ChromaRepository" has no attribute "get_document"; maybe "delete_documents"?  [attr-defined]
tests/test_db/test_chroma.py:96: error: Function is missing a return type annotation  [no-untyped-def]
tests/test_db/test_chroma.py:105: error: "ChromaRepository" has no attribute "get_document"; maybe "delete_documents"?  [attr-defined]
tests/test_db/test_chroma.py:106: error: "ChromaRepository" has no attribute "get_document"; maybe "delete_documents"?  [attr-defined]
tests/test_db/test_chroma.py:107: error: "ChromaRepository" has no attribute "get_document"; maybe "delete_documents"?  [attr-defined]
tests/test_db/test_chroma.py:110: error: Function is missing a return type annotation  [no-untyped-def]
tests/test_db/test_chroma.py:112: error: "ChromaRepository" has no attribute "get_document"; maybe "delete_documents"?  [attr-defined]
tests/test_db/test_chroma.py:115: error: Function is missing a return type annotation  [no-untyped-def]
obsidian_concierge/core/search.py:59: error: Argument "n_results" to "query" of "ChromaRepository" has incompatible type "int | None"; expected "int"  [arg-type]
tests/test_indexer/test_vault_indexer.py:16: error: Function is missing a return type annotation  [no-untyped-def]
tests/test_indexer/test_vault_indexer.py:22: error: Function is missing a type annotation  [no-untyped-def]
tests/test_indexer/test_vault_indexer.py:37: error: "str" has no attribute "parent"  [attr-defined]
tests/test_indexer/test_vault_indexer.py:38: error: "str" has no attribute "write_text"  [attr-defined]
tests/test_indexer/test_vault_indexer.py:43: error: Function is missing a type annotation  [no-untyped-def]
tests/test_indexer/test_vault_indexer.py:50: error: Function is missing a type annotation  [no-untyped-def]
tests/test_indexer/test_vault_indexer.py:56: error: Function is missing a type annotation  [no-untyped-def]
tests/test_indexer/test_vault_indexer.py:63: error: Function is missing a type annotation  [no-untyped-def]
tests/test_indexer/test_vault_indexer.py:77: error: Function is missing a type annotation  [no-untyped-def]
tests/test_indexer/test_vault_indexer.py:91: error: Function is missing a type annotation  [no-untyped-def]
tests/test_indexer/test_vault_indexer.py:105: error: Function is missing a type annotation  [no-untyped-def]
tests/test_indexer/test_vault_indexer.py:116: error: Function is missing a type annotation  [no-untyped-def]
tests/test_indexer/test_vault_indexer.py:130: error: Function is missing a type annotation  [no-untyped-def]
tests/test_indexer/test_vault_indexer.py:143: error: Function is missing a type annotation  [no-untyped-def]
obsidian_concierge/services/qa.py:8: error: Skipping analyzing "obsidian_concierge.repository.chroma": module is installed, but missing library stubs or py.typed marker  [import-untyped]
obsidian_concierge/services/qa.py:24: error: "None" not callable  [misc]
obsidian_concierge/api/routes.py:13: error: Skipping analyzing "obsidian_concierge.repository.chroma": module is installed, but missing library stubs or py.typed marker  [import-untyped]
obsidian_concierge/api/routes.py:13: note: See https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-imports
obsidian_concierge/api/routes.py:91: error: "QAService" has no attribute "answer_question"  [attr-defined]
obsidian_concierge/api/app.py:32: error: Function is missing a return type annotation  [no-untyped-def]
Found 350 errors in 31 files (checked 48 source files)

- **Pytestによるテスト実行**: ============================= test session starts ==============================
platform linux -- Python 3.11.11, pytest-8.3.5, pluggy-1.5.0
rootdir: /home/persona/analysis/Obsidian-Concierge
configfile: pyproject.toml
plugins: anyio-4.9.0, asyncio-0.23.8
asyncio: mode=Mode.STRICT
collected 28 items / 1 error

==================================== ERRORS ====================================
_________________ ERROR collecting snippet/testing/test_all.py _________________
ImportError while importing test module '/home/persona/analysis/Obsidian-Concierge/snippet/testing/test_all.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
../../.pyenv/versions/3.11.11/lib/python3.11/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
snippet/testing/test_all.py:9: in <module>
    from snippet.utils.logger.config_manage import ConfigManager
snippet/utils/__init__.py:7: in <module>
    from .file_utils import SafeFileOps, FileStructureAnalyzer, FileUtils
E   ModuleNotFoundError: No module named 'snippet.utils.file_utils'
=============================== warnings summary ===============================
obsidian_concierge/utils/config.py:82
  /home/persona/analysis/Obsidian-Concierge/obsidian_concierge/utils/config.py:82: PydanticDeprecatedSince20: The `__fields__` attribute is deprecated, use `model_fields` instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.11/migration/
    for field in AppConfig.__fields__:

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== short test summary info ============================
ERROR snippet/testing/test_all.py
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
========================= 1 warning, 1 error in 4.46s ==========================

- **Banditによるセキュリティチェック**: [main]	INFO	profile include tests: None
[main]	INFO	profile exclude tests: None
[main]	INFO	cli include tests: None
[main]	INFO	cli exclude tests: None
[main]	INFO	running on Python 3.11.11


## ファイル別の問題詳細
### code_complexity_checker.py
- 行 7: `CodeComplexityChecker` は長すぎます (115行、上限100行)

### validator.py
- 行 15: `Validator` は長すぎます (251行、上限100行)

### analyze_python_files.py
- 行 34: `analyze_function_body` はネストが深すぎます (レベル5、上限4)
- 行 56: `analyze_python_file` は長すぎます (109行、上限100行)
- 行 56: `analyze_python_file` はネストが深すぎます (レベル6、上限4)

### config_manage.py
- 行 14: `ConfigManager` は長すぎます (280行、上限100行)
- 行 14: `ConfigManager` はネストが深すぎます (レベル9、上限4)
- 行 231: `_validate_config` はネストが深すぎます (レベル9、上限4)

### env_loader.py
- 行 7: `EnvLoader` は長すぎます (125行、上限100行)

### input_sanitizer.py
- 行 6: `InputSanitizer` は長すぎます (209行、上限100行)

### code_analyzer.py
- 行 70: `CodeAnalyzer` は長すぎます (229行、上限100行)

### report_generator.py
- 行 143: `_generate_directory_report_md` はネストが深すぎます (レベル5、上限4)
- 行 215: `_generate_validator_report_md` は長すぎます (117行、上限100行)
- 行 215: `_generate_validator_report_md` はネストが深すぎます (レベル10、上限4)

### validator_integration.py
- 行 30: `FunctionValidator` は長すぎます (476行、上限100行)
- 行 30: `FunctionValidator` はネストが深すぎます (レベル11、上限4)
- 行 47: `_generate_test_value` はネストが深すぎます (レベル11、上限4)
- 行 253: `_validate_type` はネストが深すぎます (レベル6、上限4)
- 行 350: `validate_module_functions` は長すぎます (156行、上限100行)
- 行 350: `validate_module_functions` はネストが深すぎます (レベル5、上限4)

### validator.py
- 行 15: `Validator` は長すぎます (251行、上限100行)

### cli.py
- 行 87: `_generate_validator_report` は長すぎます (123行、上限100行)
- 行 87: `_generate_validator_report` はネストが深すぎます (レベル12、上限4)
- 行 212: `analyze_files_parallel` はネストが深すぎます (レベル5、上限4)
- 行 275: `main` は長すぎます (265行、上限100行)
- 行 275: `main` はネストが深すぎます (レベル6、上限4)

### contextual_logger.py
- 行 12: `ContextualLogger` は長すぎます (158行、上限100行)

### safe_file_ops.py
- 行 16: `SafeFileOps` は長すぎます (329行、上限100行)

### ollama.py
- 行 25: `OllamaClient` は長すぎます (167行、上限100行)

### chroma.py
- 行 22: `ChromaRepository` は長すぎます (130行、上限100行)

### vault_indexer.py
- 行 20: `VaultIndexer` は長すぎます (177行、上限100行)

### qa.py
- 行 28: `QAService` は長すぎます (111行、上限100行)

### qa.py
- 行 13: `QAService` は長すぎます (151行、上限100行)
