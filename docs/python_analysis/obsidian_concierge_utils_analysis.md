# obsidian_concierge/utils フォルダのPython解析レポート

生成日時: 2025-04-08 20:40:21.579242

==================================================

# __init__.py の解析結果

## インポート一覧
- `config.AppConfig` (❌ 未使用)
- `config.config` (❌ 未使用)
- `config.load_config` (❌ 未使用)
- `fs.ensure_dir` (❌ 未使用)
- `fs.get_file_extension` (❌ 未使用)
- `fs.get_file_size` (❌ 未使用)
- `fs.is_text_file` (❌ 未使用)
- `fs.list_files` (❌ 未使用)
- `fs.safe_remove` (❌ 未使用)
- `logging.LogConfig` (❌ 未使用)
- `logging.logger` (❌ 未使用)
- `logging.setup_logging` (❌ 未使用)


--------------------------------------------------

# config.py の解析結果

## インポート一覧
- `os` (✅ 使用あり)
- `pathlib.Path` (✅ 使用あり)
- `pydantic.BaseModel` (✅ 使用あり)
- `pydantic.Field` (✅ 使用あり)
- `typing.Optional` (✅ 使用あり)
- `yaml` (✅ 使用あり)

## クラス: `AppConfig` (BaseModel)
**Docstring**: Application configuration model.

## 関数: `load_config(config_path: Optional[str] [✅]) -> AppConfig` [✅ 使用あり]
**Docstring**: Load application configuration.

Args:
    config_path: Path to YAML configuration file
    
Returns:
    Application configuration

**内部で定義される名前:**
- `config_data`
- `config_path`
- `env_value`
- `load_config`



--------------------------------------------------

# fs.py の解析結果

## インポート一覧
- `logging.logger` (✅ 使用あり)
- `os` (❌ 未使用)
- `pathlib.Path` (✅ 使用あり)
- `shutil` (✅ 使用あり)
- `typing.List` (✅ 使用あり)
- `typing.Optional` (❌ 未使用)
- `typing.Set` (❌ 未使用)

## 関数: `ensure_dir(path: str | Path [✅]) -> Path` [❌ 未使用]
**Docstring**: Ensure a directory exists, creating it if necessary.

Args:
    path: Directory path to ensure
    
Returns:
    Path object of the ensured directory

**内部で定義される名前:**
- `ensure_dir`
- `path`


## 関数: `list_files(directory: str | Path [✅], pattern: str [✅], recursive: bool [✅]) -> List[Path]` [❌ 未使用]
**Docstring**: List files in a directory matching a pattern.

Args:
    directory: Directory to search in
    pattern: Glob pattern to match files against
    recursive: Whether to search recursively
    
Returns:
    List of matching file paths
    
Raises:
    FileNotFoundError: If directory doesn't exist

**内部で定義される名前:**
- `directory`
- `list_files`


## 関数: `safe_remove(path: str | Path [✅]) -> None` [❌ 未使用]
**Docstring**: Safely remove a file or directory.

Args:
    path: Path to remove

**内部で定義される名前:**
- `path`
- `safe_remove`


## 関数: `get_file_extension(path: str | Path [✅]) -> str` [❌ 未使用]
**Docstring**: Get the extension of a file (lowercase).

Args:
    path: File path
    
Returns:
    Lowercase file extension without dot

**内部で定義される名前:**
- `get_file_extension`


## 関数: `is_text_file(path: str | Path [✅], max_check_size: int [✅]) -> bool` [❌ 未使用]
**Docstring**: Check if a file appears to be a text file.

Args:
    path: File path to check
    max_check_size: Maximum number of bytes to check
    
Returns:
    True if file appears to be text, False otherwise

**内部で定義される名前:**
- `chunk`
- `is_text_file`


## 関数: `get_file_size(path: str | Path [✅]) -> int` [❌ 未使用]
**Docstring**: Get the size of a file in bytes.

Args:
    path: Path to the file
    
Returns:
    File size in bytes
    
Raises:
    FileNotFoundError: If file doesn't exist

**内部で定義される名前:**
- `get_file_size`
- `path`



--------------------------------------------------

# logging.py の解析結果

## インポート一覧
- `logging` (✅ 使用あり)
- `logging.handlers` (❌ 未使用)
- `os` (❌ 未使用)
- `pathlib.Path` (✅ 使用あり)
- `pydantic.BaseModel` (✅ 使用あり)
- `typing.Optional` (✅ 使用あり)

## クラス: `LogConfig` (BaseModel)
**Docstring**: Configuration model for logging settings.

## 関数: `setup_logging(config: LogConfig [✅]) -> logging.Logger` [✅ 使用あり]
**Docstring**: Set up logging configuration for the application.

Args:
    config: LogConfig instance containing logging configuration
    
Returns:
    Configured logger instance

**内部で定義される名前:**
- `console_handler`
- `file_handler`
- `formatter`
- `log_dir`
- `logger`
- `setup_logging`



--------------------------------------------------

