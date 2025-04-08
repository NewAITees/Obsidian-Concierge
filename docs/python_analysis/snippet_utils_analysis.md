# snippet/utils フォルダのPython解析レポート

生成日時: 2025-04-08 20:40:21.867506

==================================================

# __init__.py の解析結果

## インポート一覧
- `env_loader.EnvLoader` (❌ 未使用)
- `exception_handler.exception_handler` (❌ 未使用)
- `file_utils.FileStructureAnalyzer` (❌ 未使用)
- `file_utils.FileUtils` (❌ 未使用)
- `file_utils.SafeFileOps` (❌ 未使用)
- `input_sanitizer.InputSanitizer` (❌ 未使用)
- `validator.ValidationError` (❌ 未使用)
- `validator.Validator` (❌ 未使用)


--------------------------------------------------

# config_manage.py の解析結果

## インポート一覧
- `json` (✅ 使用あり)
- `logging` (✅ 使用あり)
- `os` (✅ 使用あり)
- `pathlib.Path` (✅ 使用あり)
- `tempfile` (✅ 使用あり)
- `typing.Any` (✅ 使用あり)
- `typing.Dict` (✅ 使用あり)
- `typing.List` (❌ 未使用)
- `typing.Optional` (✅ 使用あり)
- `typing.Set` (❌ 未使用)
- `typing.Union` (✅ 使用あり)
- `yaml` (✅ 使用あり)

## クラス: `ConfigError` (Exception)
**Docstring**: 設定関連のエラー

## クラス: `ConfigManager`
**Docstring**: JSON/YAML設定ファイルの読み込みと検証を行うユーティリティ
環境ごとの設定マージ機能付き

### メソッド: `__init__(self: Any [✅], config_dir: Union[str, Path] [✅], env: Optional[str] [✅], schema: Optional[Dict[str, Any]] [✅], config_type: str [✅]) -> None` [❌ 未使用]
**Docstring**: Args:
    config_dir: 設定ファイルが置かれているディレクトリ
    env: 環境名（development, testing, production など）
    schema: 設定ファイルのスキーマ定義（省略可）
    config_type: 設定ファイルのタイプ（'yaml' または 'json'）

**内部で定義される名前:**
- `__init__`


### メソッド: `load(self: Any [✅], reload: bool [✅]) -> Dict[str, Any]` [✅ 使用あり]
**Docstring**: 設定ファイルを読み込む

Args:
    reload: 設定を再読み込みするかどうか
    
Returns:
    設定データ（辞書）
    
Raises:
    ConfigError: 設定ファイル読み込みに失敗した場合

**内部で定義される名前:**
- `config_data`
- `config_files`
- `load`
- `merged_config`


### メソッド: `get(self: Any [✅], key: str [✅], default: Any [✅]) -> Any` [✅ 使用あり]
**Docstring**: 設定値を取得

Args:
    key: 設定キー（ドット区切りで階層指定可能）
    default: 設定が見つからない場合のデフォルト値
    
Returns:
    設定値

**内部で定義される名前:**
- `config`
- `get`
- `parts`


### メソッド: `get_all(self: Any [✅]) -> Dict[str, Any]` [❌ 未使用]
**Docstring**: すべての設定を取得

Returns:
    設定データ（辞書）

**内部で定義される名前:**
- `get_all`


### メソッド: `set(self: Any [✅], key: str [✅], value: Any [✅]) -> None` [✅ 使用あり]
**Docstring**: 実行時に設定値を変更（メモリ内のみ）

Args:
    key: 設定キー（ドット区切りで階層指定可能）
    value: 設定値

**内部で定義される名前:**
- `config`
- `parts`
- `set`


### メソッド: `save(self: Any [✅], file_path: Optional[Union[str, Path]] [✅]) -> None` [✅ 使用あり]
**Docstring**: 設定をファイルに保存（オプション）

Args:
    file_path: 保存先ファイルパス（省略時はlocal設定ファイル）
    
Raises:
    ConfigError: 設定ファイル保存に失敗した場合

**内部で定義される名前:**
- `file_path`
- `save`


### メソッド: `_read_config_file(self: Any [✅], file_path: Path [✅]) -> Dict[str, Any]` [✅ 使用あり]
**Docstring**: 設定ファイルを読み込む

Args:
    file_path: 設定ファイルパス
    
Returns:
    設定データ（辞書）
    
Raises:
    ConfigError: 設定ファイル読み込みに失敗した場合

**内部で定義される名前:**
- `_read_config_file`


### メソッド: `_deep_merge(self: Any [✅], base: Dict[str, Any] [✅], override: Dict[str, Any] [✅]) -> Dict[str, Any]` [✅ 使用あり]
**Docstring**: 2つの設定辞書を再帰的にマージ

Args:
    base: ベースとなる辞書
    override: 上書きする辞書
    
Returns:
    マージされた辞書

**内部で定義される名前:**
- `_deep_merge`
- `result`


### メソッド: `_validate_config(self: Any [✅], config: Dict[str, Any] [✅], schema: Dict[str, Any] [✅], path: str [✅]) -> None` [✅ 使用あり]
**Docstring**: スキーマに基づいて設定を検証

Args:
    config: 検証する設定
    schema: スキーマ定義
    path: 現在のパス（エラーメッセージ用）
    
Raises:
    ConfigError: 検証に失敗した場合

**内部で定義される名前:**
- `_validate_config`
- `current_path`
- `expected_type`
- `item_path`
- `item_type`
- `value`



--------------------------------------------------

# env_loader.py の解析結果

## インポート一覧
- `os` (✅ 使用あり)
- `pathlib.Path` (✅ 使用あり)
- `re` (✅ 使用あり)
- `typing.Any` (✅ 使用あり)
- `typing.Dict` (✅ 使用あり)
- `typing.List` (✅ 使用あり)
- `typing.Optional` (✅ 使用あり)
- `typing.Union` (❌ 未使用)

## クラス: `EnvLoader`
**Docstring**: 環境に応じて .env ファイルを読み込むユーティリティ
必須環境変数のチェック機能付き

### メソッド: `__init__(self: Any [✅], base_dir: Optional[str] [✅], env: Optional[str] [✅], required_vars: Optional[List[str]] [✅]) -> None` [❌ 未使用]
**Docstring**: Args:
    base_dir: .env ファイルが置かれているディレクトリ
    env: 環境名 (development, testing, production など)
    required_vars: 必須の環境変数リスト

**内部で定義される名前:**
- `__init__`


### メソッド: `load(self: Any [✅], override: bool [✅]) -> Dict[str, str]` [✅ 使用あり]
**Docstring**: 環境変数をロード

Args:
    override: 既存の環境変数を上書きするかどうか
    
Returns:
    ロードされた環境変数の辞書

Raises:
    ValueError: 必須環境変数が見つからない場合
    FileNotFoundError: .env ファイルが見つからない場合

**内部で定義される名前:**
- `env_files`
- `file_vars`
- `load`
- `loaded_vars`
- `missing_vars`


### メソッド: `_parse_env_file(self: Any [❌], file_path: Path [✅]) -> Dict[str, str]` [✅ 使用あり]
**Docstring**: .env ファイルをパース

Args:
    file_path: .env ファイルのパス
    
Returns:
    パースされた環境変数の辞書

**内部で定義される名前:**
- `_parse_env_file`
- `line`
- `match`
- `result`
- `value`


### メソッド: `get(self: Any [✅], key: str [✅], default: Any [✅], as_type: Optional[type] [✅]) -> Any` [✅ 使用あり]
**Docstring**: 環境変数を取得（オプションで型変換）

Args:
    key: 環境変数名
    default: デフォルト値
    as_type: 型変換関数（int, float, bool など）
    
Returns:
    環境変数の値（変換後）

**内部で定義される名前:**
- `get`
- `value`



--------------------------------------------------

# exception_handler.py の解析結果

## インポート一覧
- `functools` (✅ 使用あり)
- `logging` (✅ 使用あり)
- `os` (✅ 使用あり)
- `sys` (❌ 未使用)
- `traceback` (✅ 使用あり)

## 関数: `exception_handler(reraise: Any [✅], log_level: Any [✅], production_mode: Any [✅], default_return: Any [✅]) -> None` [✅ 使用あり]
**Docstring**: 関数実行時の例外を捕捉し詳細情報を記録するデコレータ

Args:
    reraise: 例外を再スローするかどうか
    log_level: ログレベル
    production_mode: 本番環境モードフラグ（Noneの場合はPRODUCTION環境変数を使用）
    default_return: 例外発生時のデフォルト戻り値

Returns:
    デコレートされた関数

**内部で定義される名前:**
- `decorator`
- `detailed_message`
- `error_message`
- `exception_handler`
- `func_name`
- `module_name`
- `production_mode`
- `wrapper`


## 関数: `decorator(func: Any [✅]) -> None` [❌ 未使用]

**内部で定義される名前:**
- `decorator`
- `detailed_message`
- `error_message`
- `func_name`
- `module_name`
- `wrapper`


## 関数: `@exception_handler(production_mode=False) divide(a: Any [✅], b: Any [✅]) -> None` [✅ 使用あり]

**内部で定義される名前:**
- `divide`


## 関数: `@exception_handler(production_mode=True, reraise=False, default_return=0) risky_operation(items: Any [✅]) -> None` [✅ 使用あり]

**内部で定義される名前:**
- `risky_operation`


## 関数: `@functools.wraps(func) wrapper() -> None` [❌ 未使用]

**内部で定義される名前:**
- `detailed_message`
- `error_message`
- `func_name`
- `module_name`
- `wrapper`



--------------------------------------------------

# input_sanitizer.py の解析結果

## インポート一覧
- `html` (✅ 使用あり)
- `re` (✅ 使用あり)
- `typing.Any` (✅ 使用あり)
- `typing.Dict` (✅ 使用あり)
- `typing.List` (✅ 使用あり)
- `typing.Optional` (✅ 使用あり)
- `typing.Union` (❌ 未使用)

## クラス: `InputSanitizer`
**Docstring**: 入力値のサニタイズを行うユーティリティクラス
HTMLエスケープやSQLインジェクション対策を提供

### メソッド: `@staticmethod sanitize_html(text: str [✅]) -> str` [✅ 使用あり]
**Docstring**: HTMLタグをエスケープ

Args:
    text: 処理対象のテキスト
    
Returns:
    エスケープされたテキスト

**内部で定義される名前:**
- `sanitize_html`
- `text`


### メソッド: `@staticmethod strip_tags(text: str [✅]) -> str` [✅ 使用あり]
**Docstring**: HTMLタグを削除

Args:
    text: 処理対象のテキスト
    
Returns:
    タグが削除されたテキスト

**内部で定義される名前:**
- `strip_tags`


### メソッド: `@staticmethod sanitize_sql(text: str [✅]) -> str` [✅ 使用あり]
**Docstring**: SQLインジェクション対策のためのエスケープ

注意: これはパラメータ化クエリの代わりにはなりません。
常にプリペアドステートメントを使用してください。

Args:
    text: 処理対象のテキスト
    
Returns:
    エスケープされたテキスト

**内部で定義される名前:**
- `result`
- `sanitize_sql`
- `special_chars`
- `sql_keywords`


### メソッド: `@staticmethod sanitize_filename(text: str [✅]) -> str` [✅ 使用あり]
**Docstring**: ファイル名から危険な文字を削除

Args:
    text: 処理対象のテキスト
    
Returns:
    安全なファイル名

**内部で定義される名前:**
- `sanitize_filename`
- `text`


### メソッド: `@staticmethod sanitize_integer(value: Any [✅], default: int [✅], min_value: Optional[int] [✅], max_value: Optional[int] [✅]) -> int` [✅ 使用あり]
**Docstring**: 整数値をサニタイズ

Args:
    value: 処理対象の値
    default: 変換できない場合のデフォルト値
    min_value: 最小値
    max_value: 最大値
    
Returns:
    サニタイズされた整数値

**内部で定義される名前:**
- `result`
- `sanitize_integer`


### メソッド: `@staticmethod sanitize_email(email: str [✅]) -> str` [✅ 使用あり]
**Docstring**: メールアドレスをサニタイズ

Args:
    email: メールアドレス
    
Returns:
    サニタイズされたメールアドレス（無効な場合は空文字）

**内部で定義される名前:**
- `pattern`
- `sanitize_email`


### メソッド: `@staticmethod sanitize_dict(data: Dict[str, Any] [✅], allowed_keys: List[str] [✅]) -> Dict[str, Any]` [✅ 使用あり]
**Docstring**: 辞書から許可されたキーのみを抽出

Args:
    data: 処理対象の辞書
    allowed_keys: 許可するキーのリスト
    
Returns:
    サニタイズされた辞書

**内部で定義される名前:**
- `sanitize_dict`


### メソッド: `@staticmethod sanitize_all_dict_values(data: Dict[str, Any] [✅]) -> Dict[str, Any]` [✅ 使用あり]
**Docstring**: 辞書のすべての文字列値をHTMLエスケープ

Args:
    data: 処理対象の辞書
    
Returns:
    サニタイズされた辞書

**内部で定義される名前:**
- `result`
- `sanitize_all_dict_values`


### メソッド: `@staticmethod sanitize_all_list_values(data: List[Any] [✅]) -> List[Any]` [✅ 使用あり]
**Docstring**: リストのすべての文字列値をHTMLエスケープ

Args:
    data: 処理対象のリスト
    
Returns:
    サニタイズされたリスト

**内部で定義される名前:**
- `result`
- `sanitize_all_list_values`



--------------------------------------------------

# safe_file_ops.py の解析結果

## インポート一覧
- `csv` (✅ 使用あり)
- `hashlib` (✅ 使用あり)
- `json` (✅ 使用あり)
- `os` (✅ 使用あり)
- `pathlib.Path` (✅ 使用あり)
- `shutil` (✅ 使用あり)
- `tempfile` (✅ 使用あり)
- `typing.Any` (✅ 使用あり)
- `typing.Callable` (✅ 使用あり)
- `typing.Dict` (✅ 使用あり)
- `typing.List` (✅ 使用あり)
- `typing.Optional` (✅ 使用あり)
- `typing.Union` (✅ 使用あり)

## クラス: `FileOperationError` (Exception)
**Docstring**: ファイル操作に関するエラー

## クラス: `SafeFileOps`
**Docstring**: 安全なファイル操作を提供するユーティリティクラス
一時ファイルを使った安全な書き込み処理とエラーハンドリングを提供

### メソッド: `@staticmethod safe_read(file_path: Union[str, Path] [✅], encoding: str [✅], default: Any [✅]) -> str` [✅ 使用あり]
**Docstring**: 安全にファイルを読み込む

Args:
    file_path: 読み込むファイルのパス
    encoding: 文字エンコーディング
    default: エラー時のデフォルト値
    
Returns:
    ファイルの内容
    
Raises:
    FileOperationError: デフォルト値が指定されておらず、ファイル読み込みに失敗した場合

**内部で定義される名前:**
- `safe_read`


### メソッド: `@staticmethod safe_write(file_path: Union[str, Path] [✅], content: str [✅], encoding: str [✅]) -> None` [✅ 使用あり]
**Docstring**: 安全にファイルに書き込む（一時ファイルを使用）

Args:
    file_path: 書き込み先ファイルのパス
    content: 書き込む内容
    encoding: 文字エンコーディング
    
Raises:
    FileOperationError: ファイル書き込みに失敗した場合

**内部で定義される名前:**
- `file_path`
- `safe_write`
- `temp_dir`
- `tmp_path`


### メソッド: `@staticmethod safe_append(file_path: Union[str, Path] [✅], content: str [✅], encoding: str [✅]) -> None` [❌ 未使用]
**Docstring**: 安全にファイルに追記する

Args:
    file_path: 追記先ファイルのパス
    content: 追記する内容
    encoding: 文字エンコーディング
    
Raises:
    FileOperationError: ファイル追記に失敗した場合

**内部で定義される名前:**
- `file_path`
- `safe_append`


### メソッド: `@staticmethod safe_delete(file_path: Union[str, Path] [✅]) -> bool` [❌ 未使用]
**Docstring**: 安全にファイルを削除する

Args:
    file_path: 削除するファイルのパス
    
Returns:
    削除が成功したかどうか
    
Raises:
    FileOperationError: ファイル削除に失敗した場合

**内部で定義される名前:**
- `safe_delete`


### メソッド: `@staticmethod safe_rename(src_path: Union[str, Path] [✅], dst_path: Union[str, Path] [✅]) -> None` [❌ 未使用]
**Docstring**: 安全にファイルをリネーム/移動する

Args:
    src_path: 元のファイルパス
    dst_path: 移動先のファイルパス
    
Raises:
    FileOperationError: ファイル移動に失敗した場合

**内部で定義される名前:**
- `dst_path`
- `safe_rename`


### メソッド: `@staticmethod safe_copy(src_path: Union[str, Path] [✅], dst_path: Union[str, Path] [✅]) -> None` [✅ 使用あり]
**Docstring**: 安全にファイルをコピーする

Args:
    src_path: コピー元のファイルパス
    dst_path: コピー先のファイルパス
    
Raises:
    FileOperationError: ファイルコピーに失敗した場合

**内部で定義される名前:**
- `dst_path`
- `safe_copy`


### メソッド: `@staticmethod read_json(file_path: Union[str, Path] [✅], encoding: str [✅], default: Optional[Any] [✅]) -> Dict[str, Any]` [✅ 使用あり]
**Docstring**: JSONファイルを読み込む

Args:
    file_path: 読み込むJSONファイルのパス
    encoding: 文字エンコーディング
    default: ファイルが存在しない場合のデフォルト値
    
Returns:
    JSONデータ（辞書）
    
Raises:
    FileOperationError: デフォルト値が指定されておらず、ファイル読み込みに失敗した場合

**内部で定義される名前:**
- `read_json`


### メソッド: `@staticmethod write_json(file_path: Union[str, Path] [✅], data: Dict[str, Any] [✅], encoding: str [✅], indent: int [✅]) -> None` [✅ 使用あり]
**Docstring**: JSONファイルに書き込む

Args:
    file_path: 書き込み先JSONファイルのパス
    data: 書き込むデータ（辞書）
    encoding: 文字エンコーディング
    indent: JSONのインデントスペース数
    
Raises:
    FileOperationError: ファイル書き込みに失敗した場合

**内部で定義される名前:**
- `content`
- `write_json`


### メソッド: `@staticmethod read_csv(file_path: Union[str, Path] [✅], encoding: str [✅], delimiter: str [✅], has_header: bool [✅]) -> List[Dict[str, str]]` [✅ 使用あり]
**Docstring**: CSVファイルを読み込む

Args:
    file_path: 読み込むCSVファイルのパス
    encoding: 文字エンコーディング
    delimiter: 区切り文字
    has_header: ヘッダー行があるかどうか
    
Returns:
    CSVデータ（辞書のリスト）
    
Raises:
    FileOperationError: ファイル読み込みに失敗した場合

**内部で定義される名前:**
- `data`
- `read_csv`
- `reader`


### メソッド: `@staticmethod write_csv(file_path: Union[str, Path] [✅], data: List[Dict[str, Any]] [✅], fieldnames: Optional[List[str]] [✅], encoding: str [✅], delimiter: str [✅]) -> None` [✅ 使用あり]
**Docstring**: CSVファイルに書き込む

Args:
    file_path: 書き込み先CSVファイルのパス
    data: 書き込むデータ（辞書のリスト）
    fieldnames: 列名のリスト（None の場合は最初の辞書のキーを使用）
    encoding: 文字エンコーディング
    delimiter: 区切り文字
    
Raises:
    FileOperationError: ファイル書き込みに失敗した場合

**内部で定義される名前:**
- `fieldnames`
- `file_path`
- `temp_dir`
- `tmp_path`
- `write_csv`
- `writer`


### メソッド: `@staticmethod get_file_hash(file_path: Union[str, Path] [✅], algorithm: str [✅], chunk_size: int [✅]) -> str` [✅ 使用あり]
**Docstring**: ファイルのハッシュ値を計算

Args:
    file_path: ハッシュ値を計算するファイルのパス
    algorithm: ハッシュアルゴリズム（md5, sha1, sha256 など）
    chunk_size: 一度に読み込むバイト数
    
Returns:
    ハッシュ値（16進数文字列）
    
Raises:
    FileOperationError: ファイル読み込みに失敗した場合

**内部で定義される名前:**
- `get_file_hash`
- `hasher`


### メソッド: `@staticmethod process_file_safely(file_path: Union[str, Path] [✅], processor: Callable[[str], str] [✅], encoding: str [✅]) -> None` [✅ 使用あり]
**Docstring**: ファイルを安全に処理する

Args:
    file_path: 処理するファイルのパス
    processor: ファイルの内容を処理する関数
    encoding: 文字エンコーディング
    
Raises:
    FileOperationError: ファイル処理に失敗した場合

**内部で定義される名前:**
- `content`
- `process_file_safely`
- `processed_content`


## 関数: `uppercase_processor(content: Any [✅]) -> None` [❌ 未使用]

**内部で定義される名前:**
- `uppercase_processor`



--------------------------------------------------

