# snippet/utils/logger フォルダのPython解析レポート

生成日時: 2025-04-08 20:40:21.933357

==================================================

# __init__.py の解析結果


--------------------------------------------------

# basic_usage.py の解析結果

## インポート一覧
- `contextual_logger.get_logger` (✅ 使用あり)
- `os` (❌ 未使用)
- `time` (✅ 使用あり)

## クラス: `UserService`

### メソッド: `__init__(self: Any [✅]) -> None` [❌ 未使用]

**内部で定義される名前:**
- `__init__`


### メソッド: `get_user(self: Any [✅], user_id: Any [✅]) -> None` [✅ 使用あり]

**内部で定義される名前:**
- `get_user`


## 関数: `basic_usage() -> None` [✅ 使用あり]

**内部で定義される名前:**
- `basic_usage`
- `logger`


## 関数: `exception_example() -> None` [✅ 使用あり]

**内部で定義される名前:**
- `exception_example`
- `logger`
- `result`


## 関数: `decorator_example() -> None` [✅ 使用あり]

**内部で定義される名前:**
- `decorator_example`
- `logger`
- `result`
- `slow_database_query`


## 関数: `security_example() -> None` [✅ 使用あり]

**内部で定義される名前:**
- `logger`
- `security_example`


## 関数: `@logger.log_execution_time slow_database_query(query_id: Any [✅]) -> None` [✅ 使用あり]

**内部で定義される名前:**
- `slow_database_query`



--------------------------------------------------

# contextual_logger.py の解析結果

## インポート一覧
- `datetime.datetime` (✅ 使用あり)
- `functools.wraps` (✅ 使用あり)
- `inspect` (✅ 使用あり)
- `json` (✅ 使用あり)
- `logging` (✅ 使用あり)
- `logging.handlers.RotatingFileHandler` (✅ 使用あり)
- `os` (✅ 使用あり)
- `time` (✅ 使用あり)
- `traceback` (✅ 使用あり)

## クラス: `ContextualLogger`
**Docstring**: コンテキスト情報（ファイル名、関数名、行番号）を自動的に付加する
構造化ロガークラス。JSON形式でログを出力し、ログレベルを一括制御できる。

### メソッド: `__init__(self: Any [✅], name: Any [✅], log_dir: Any [✅], log_level: Any [✅], max_bytes: Any [✅], backup_count: Any [✅]) -> None` [❌ 未使用]
**Docstring**: ロガーの初期化

Args:
    name (str, optional): ロガー名。指定しない場合は呼び出し元モジュール名
    log_dir (str): ログファイルを保存するディレクトリ
    log_level (int): デフォルトのログレベル
    max_bytes (int): ログファイルの最大サイズ
    backup_count (int): 保持するバックアップファイル数

**内部で定義される名前:**
- `__init__`
- `app_handler`
- `app_log_file`
- `app_log_path`
- `console_handler`
- `error_handler`
- `error_log_file`
- `error_log_path`
- `frame`
- `module`
- `name`


### メソッド: `_get_context_info(self: Any [❌]) -> None` [✅ 使用あり]
**Docstring**: 呼び出し元のコンテキスト情報（ファイル名、関数名、行番号）を取得

**内部で定義される名前:**
- `_get_context_info`
- `filename`
- `frame`
- `function_name`
- `line_number`


### メソッド: `_format_log(self: Any [✅], message: Any [✅], level: Any [✅], extra: Any [✅]) -> None` [✅ 使用あり]
**Docstring**: ログメッセージをJSON形式に整形

**内部で定義される名前:**
- `_format_log`
- `log_data`
- `masked_extra`


### メソッド: `_mask_sensitive_data(self: Any [❌], data: Any [✅]) -> None` [✅ 使用あり]
**Docstring**: 機密情報をマスク処理

**内部で定義される名前:**
- `_mask_sensitive_data`
- `masked_data`
- `sensitive_keys`


### メソッド: `debug(self: Any [✅], message: Any [✅]) -> None` [✅ 使用あり]
**Docstring**: DEBUGレベルのログ出力

**内部で定義される名前:**
- `debug`


### メソッド: `info(self: Any [✅], message: Any [✅]) -> None` [✅ 使用あり]
**Docstring**: INFOレベルのログ出力

**内部で定義される名前:**
- `info`


### メソッド: `warning(self: Any [✅], message: Any [✅]) -> None` [✅ 使用あり]
**Docstring**: WARNINGレベルのログ出力

**内部で定義される名前:**
- `warning`


### メソッド: `error(self: Any [✅], message: Any [✅], exc_info: Any [✅]) -> None` [✅ 使用あり]
**Docstring**: ERRORレベルのログ出力。例外情報も記録可能

**内部で定義される名前:**
- `error`


### メソッド: `critical(self: Any [✅], message: Any [✅], exc_info: Any [✅]) -> None` [✅ 使用あり]
**Docstring**: CRITICALレベルのログ出力。例外情報も記録可能

**内部で定義される名前:**
- `critical`


### メソッド: `set_level(self: Any [✅], level: Any [✅]) -> None` [✅ 使用あり]
**Docstring**: ログレベルを変更

**内部で定義される名前:**
- `set_level`


### メソッド: `log_execution_time(self: Any [✅], func: Any [✅]) -> None` [❌ 未使用]
**Docstring**: 関数の実行時間をログに記録するデコレーター

**内部で定義される名前:**
- `execution_time`
- `log_execution_time`
- `result`
- `start_time`
- `wrapper`


## 関数: `get_logger(name: Any [✅], log_dir: Any [✅], log_level: Any [✅]) -> None` [✅ 使用あり]
**Docstring**: アプリケーション全体で利用可能なロガーインスタンスを取得

**内部で定義される名前:**
- `get_logger`
- `log_level`
- `log_level_name`


## 関数: `@logger.log_execution_time slow_function() -> None` [✅ 使用あり]

**内部で定義される名前:**
- `slow_function`


## 関数: `@wraps(func) wrapper() -> None` [❌ 未使用]

**内部で定義される名前:**
- `execution_time`
- `result`
- `start_time`
- `wrapper`



--------------------------------------------------

