# snippet/testing フォルダのPython解析レポート

生成日時: 2025-04-08 20:40:21.841883

==================================================

# test_all.py の解析結果

## インポート一覧
- `datetime.date` (✅ 使用あり)
- `datetime.datetime` (❌ 未使用)
- `json` (❌ 未使用)
- `logger.contextual_logger.ContextualLogger` (✅ 使用あり)
- `logger.contextual_logger.get_logger` (❌ 未使用)
- `os` (✅ 使用あり)
- `pathlib.Path` (✅ 使用あり)
- `save_file_structure.format_file_structure` (✅ 使用あり)
- `save_file_structure.save_file_structure` (✅ 使用あり)
- `scripts.code_complexity_checker.CodeComplexityChecker` (✅ 使用あり)
- `shutil` (✅ 使用あり)
- `snippet.utils.env_loader.EnvLoader` (✅ 使用あり)
- `snippet.utils.exception_handler.exception_handler` (✅ 使用あり)
- `snippet.utils.input_sanitizer.InputSanitizer` (✅ 使用あり)
- `snippet.utils.logger.config_manage.ConfigManager` (✅ 使用あり)
- `tempfile` (✅ 使用あり)
- `test_data_generator.Factory` (❌ 未使用)
- `test_data_generator.TestDataGenerator` (✅ 使用あり)
- `unittest` (✅ 使用あり)
- `validator.ValidationError` (✅ 使用あり)
- `validator.Validator` (✅ 使用あり)
- `yaml` (✅ 使用あり)

## クラス: `TestInputSanitizer` (unittest.TestCase)

### メソッド: `setUp(self: Any [✅]) -> None` [❌ 未使用]

**内部で定義される名前:**
- `setUp`


### メソッド: `test_sanitize_html(self: Any [✅]) -> None` [❌ 未使用]

**内部で定義される名前:**
- `html`
- `sanitized`
- `test_sanitize_html`


### メソッド: `test_strip_tags(self: Any [✅]) -> None` [❌ 未使用]

**内部で定義される名前:**
- `html`
- `stripped`
- `test_strip_tags`


### メソッド: `test_sanitize_sql(self: Any [✅]) -> None` [❌ 未使用]

**内部で定義される名前:**
- `sanitized`
- `sql`
- `test_sanitize_sql`


### メソッド: `test_sanitize_filename(self: Any [✅]) -> None` [❌ 未使用]

**内部で定義される名前:**
- `filename`
- `sanitized`
- `test_sanitize_filename`


### メソッド: `test_sanitize_email(self: Any [✅]) -> None` [❌ 未使用]

**内部で定義される名前:**
- `invalid_email`
- `test_sanitize_email`
- `valid_email`


## クラス: `TestEnvLoader` (unittest.TestCase)

### メソッド: `setUp(self: Any [✅]) -> None` [❌ 未使用]

**内部で定義される名前:**
- `setUp`


### メソッド: `tearDown(self: Any [✅]) -> None` [❌ 未使用]

**内部で定義される名前:**
- `tearDown`


### メソッド: `test_load_env_file(self: Any [✅]) -> None` [❌ 未使用]

**内部で定義される名前:**
- `env_content`
- `loaded_vars`
- `test_load_env_file`


## クラス: `TestValidator` (unittest.TestCase)

### メソッド: `test_validate_type(self: Any [✅]) -> None` [❌ 未使用]

**内部で定義される名前:**
- `test_validate_type`


### メソッド: `test_validate_length(self: Any [✅]) -> None` [❌ 未使用]

**内部で定義される名前:**
- `test_validate_length`


### メソッド: `test_validate_range(self: Any [✅]) -> None` [❌ 未使用]

**内部で定義される名前:**
- `test_validate_range`


### メソッド: `test_validate_email(self: Any [✅]) -> None` [❌ 未使用]

**内部で定義される名前:**
- `test_validate_email`


## クラス: `TestDataGeneratorTests` (unittest.TestCase)

### メソッド: `setUp(self: Any [✅]) -> None` [❌ 未使用]

**内部で定義される名前:**
- `setUp`


### メソッド: `test_random_string(self: Any [✅]) -> None` [❌ 未使用]

**内部で定義される名前:**
- `string1`
- `string2`
- `test_random_string`


### メソッド: `test_random_email(self: Any [✅]) -> None` [❌ 未使用]

**内部で定義される名前:**
- `email`
- `test_random_email`


### メソッド: `test_random_date(self: Any [✅]) -> None` [❌ 未使用]

**内部で定義される名前:**
- `date_obj`
- `test_random_date`


### メソッド: `test_random_phone(self: Any [✅]) -> None` [❌ 未使用]

**内部で定義される名前:**
- `phone`
- `test_random_phone`


## クラス: `TestCodeComplexityChecker` (unittest.TestCase)

### メソッド: `setUp(self: Any [✅]) -> None` [❌ 未使用]

**内部で定義される名前:**
- `setUp`


### メソッド: `test_simple_code(self: Any [✅]) -> None` [❌ 未使用]

**内部で定義される名前:**
- `code`
- `test_simple_code`


### メソッド: `test_complex_code(self: Any [✅]) -> None` [❌ 未使用]

**内部で定義される名前:**
- `code`
- `test_complex_code`


## クラス: `TestExceptionHandler` (unittest.TestCase)

### メソッド: `test_exception_handling(self: Any [✅]) -> None` [❌ 未使用]

**内部で定義される名前:**
- `divide`
- `result`
- `test_exception_handling`


### メソッド: `test_exception_reraising(self: Any [✅]) -> None` [❌ 未使用]

**内部で定義される名前:**
- `divide`
- `test_exception_reraising`


## クラス: `TestContextualLogger` (unittest.TestCase)

### メソッド: `setUp(self: Any [✅]) -> None` [❌ 未使用]

**内部で定義される名前:**
- `setUp`


### メソッド: `tearDown(self: Any [✅]) -> None` [❌ 未使用]

**内部で定義される名前:**
- `tearDown`


### メソッド: `test_logging_levels(self: Any [✅]) -> None` [❌ 未使用]

**内部で定義される名前:**
- `app_log_dir`
- `error_log_dir`
- `test_logging_levels`


## クラス: `TestConfigManager` (unittest.TestCase)

### メソッド: `setUp(self: Any [✅]) -> None` [❌ 未使用]

**内部で定義される名前:**
- `setUp`


### メソッド: `tearDown(self: Any [✅]) -> None` [❌ 未使用]

**内部で定義される名前:**
- `tearDown`


### メソッド: `test_load_config(self: Any [✅]) -> None` [❌ 未使用]

**内部で定義される名前:**
- `config`
- `test_load_config`


### メソッド: `test_get_config_value(self: Any [✅]) -> None` [❌ 未使用]

**内部で定義される名前:**
- `test_get_config_value`


### メソッド: `test_set_config_value(self: Any [✅]) -> None` [❌ 未使用]

**内部で定義される名前:**
- `test_set_config_value`


## クラス: `TestSaveFileStructure` (unittest.TestCase)

### メソッド: `setUp(self: Any [✅]) -> None` [❌ 未使用]

**内部で定義される名前:**
- `setUp`


### メソッド: `tearDown(self: Any [✅]) -> None` [❌ 未使用]

**内部で定義される名前:**
- `tearDown`


### メソッド: `test_format_file_structure(self: Any [✅]) -> None` [❌ 未使用]

**内部で定義される名前:**
- `files`
- `structure`
- `test_format_file_structure`


### メソッド: `test_save_file_structure(self: Any [✅]) -> None` [❌ 未使用]

**内部で定義される名前:**
- `content`
- `output_file`
- `test_save_file_structure`


## 関数: `@exception_handler(reraise=False, default_return=0) divide(a: Any [✅], b: Any [✅]) -> None` [✅ 使用あり]

**内部で定義される名前:**
- `divide`


## 関数: `@exception_handler(reraise=True) divide(a: Any [✅], b: Any [✅]) -> None` [✅ 使用あり]

**内部で定義される名前:**
- `divide`



--------------------------------------------------

