# tests/test_utils フォルダのPython解析レポート

生成日時: 2025-04-08 20:40:21.978134

==================================================

# __init__.py の解析結果


--------------------------------------------------

# test_config.py の解析結果

## インポート一覧
- `obsidian_concierge.utils.config.AppConfig` (✅ 使用あり)
- `obsidian_concierge.utils.config.load_config` (✅ 使用あり)
- `os` (✅ 使用あり)
- `pathlib.Path` (❌ 未使用)
- `pytest` (✅ 使用あり)
- `yaml` (✅ 使用あり)

## 関数: `@pytest.fixture config_file(tmp_path: Any [✅]) -> None` [❌ 未使用]
**Docstring**: Fixture for temporary config file.

**内部で定義される名前:**
- `config_data`
- `config_file`


## 関数: `test_default_config() -> None` [❌ 未使用]
**Docstring**: Test loading default configuration.

**内部で定義される名前:**
- `config`
- `test_default_config`


## 関数: `test_config_from_yaml(config_file: Any [✅]) -> None` [❌ 未使用]
**Docstring**: Test loading configuration from YAML file.

**内部で定義される名前:**
- `config`
- `test_config_from_yaml`


## 関数: `test_config_from_env() -> None` [❌ 未使用]
**Docstring**: Test loading configuration from environment variables.

**内部で定義される名前:**
- `config`
- `env_vars`
- `test_config_from_env`


## 関数: `test_invalid_config_file(tmp_path: Any [✅]) -> None` [❌ 未使用]
**Docstring**: Test handling of invalid YAML configuration file.

**内部で定義される名前:**
- `config_file`
- `test_invalid_config_file`


## 関数: `test_nonexistent_config_file() -> None` [❌ 未使用]
**Docstring**: Test handling of nonexistent configuration file.

**内部で定義される名前:**
- `test_nonexistent_config_file`


## 関数: `test_empty_config_file(tmp_path: Any [✅]) -> None` [❌ 未使用]
**Docstring**: Test handling of empty configuration file.

**内部で定義される名前:**
- `config`
- `config_file`
- `test_empty_config_file`



--------------------------------------------------

# test_fs.py の解析結果

## インポート一覧
- `obsidian_concierge.utils.fs.ensure_dir` (✅ 使用あり)
- `obsidian_concierge.utils.fs.get_file_extension` (✅ 使用あり)
- `obsidian_concierge.utils.fs.get_file_size` (✅ 使用あり)
- `obsidian_concierge.utils.fs.is_text_file` (✅ 使用あり)
- `obsidian_concierge.utils.fs.list_files` (✅ 使用あり)
- `obsidian_concierge.utils.fs.safe_remove` (✅ 使用あり)
- `os` (❌ 未使用)
- `pathlib.Path` (✅ 使用あり)
- `pytest` (✅ 使用あり)
- `tempfile.NamedTemporaryFile` (✅ 使用あり)
- `tempfile.TemporaryDirectory` (✅ 使用あり)

## 関数: `test_ensure_dir() -> None` [❌ 未使用]
**Docstring**: Test directory creation.

**内部で定義される名前:**
- `result`
- `test_dir`
- `test_ensure_dir`


## 関数: `test_list_files() -> None` [❌ 未使用]
**Docstring**: Test file listing.

**内部で定義される名前:**
- `dir_path`
- `files`
- `nested_dir`
- `test_list_files`


## 関数: `test_safe_remove() -> None` [❌ 未使用]
**Docstring**: Test safe file and directory removal.

**内部で定義される名前:**
- `test_dir`
- `test_file`
- `test_safe_remove`


## 関数: `test_get_file_extension() -> None` [❌ 未使用]
**Docstring**: Test file extension extraction.

**内部で定義される名前:**
- `test_get_file_extension`


## 関数: `test_is_text_file() -> None` [❌ 未使用]
**Docstring**: Test text file detection.

**内部で定義される名前:**
- `binary_file`
- `test_is_text_file`
- `text_file`


## 関数: `test_get_file_size() -> None` [❌ 未使用]
**Docstring**: Test file size calculation.

**内部で定義される名前:**
- `content`
- `size`
- `test_get_file_size`



--------------------------------------------------

