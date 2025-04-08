# snippet/snippet フォルダのPython解析レポート

生成日時: 2025-04-08 20:40:21.814439

==================================================

# test_data_generator.py の解析結果

## インポート一覧
- `datetime` (✅ 使用あり)
- `logging` (✅ 使用あり)
- `random` (✅ 使用あり)
- `string` (✅ 使用あり)
- `time` (✅ 使用あり)
- `typing.Any` (✅ 使用あり)
- `typing.Callable` (✅ 使用あり)
- `typing.Dict` (✅ 使用あり)
- `typing.List` (✅ 使用あり)
- `typing.Optional` (✅ 使用あり)
- `typing.Type` (✅ 使用あり)
- `typing.Union` (❌ 未使用)
- `uuid` (✅ 使用あり)

## クラス: `TestDataGenerator`
**Docstring**: テストケース用のダミーデータを生成するシンプルなジェネレータ

### メソッド: `@staticmethod random_string(length: int [✅]) -> str` [✅ 使用あり]
**Docstring**: ランダムな文字列を生成

**内部で定義される名前:**
- `random_string`


### メソッド: `@staticmethod random_email() -> str` [✅ 使用あり]
**Docstring**: ランダムなメールアドレスを生成

**内部で定義される名前:**
- `domain`
- `domains`
- `random_email`
- `username`


### メソッド: `@staticmethod random_date(start_year: int [✅], end_year: int [✅]) -> datetime.date` [✅ 使用あり]
**Docstring**: ランダムな日付を生成

**内部で定義される名前:**
- `days_between`
- `end_date`
- `random_date`
- `random_days`
- `start_date`


### メソッド: `@staticmethod random_datetime(start_year: int [✅], end_year: int [✅]) -> datetime.datetime` [✅ 使用あり]
**Docstring**: ランダムな日時を生成

**内部で定義される名前:**
- `date`
- `hour`
- `minute`
- `random_datetime`
- `second`


### メソッド: `@staticmethod random_phone() -> str` [✅ 使用あり]
**Docstring**: ランダムな電話番号を生成

**内部で定義される名前:**
- `random_phone`


### メソッド: `@staticmethod random_uuid() -> str` [✅ 使用あり]
**Docstring**: ランダムなUUIDを生成

**内部で定義される名前:**
- `random_uuid`


### メソッド: `@staticmethod random_choice(items: List[Any] [✅]) -> Any` [❌ 未使用]
**Docstring**: リストからランダムに1つ選択

**内部で定義される名前:**
- `random_choice`


### メソッド: `@staticmethod random_bool(true_probability: float [✅]) -> bool` [❌ 未使用]
**Docstring**: ランダムな真偽値を生成

**内部で定義される名前:**
- `random_bool`


### メソッド: `@staticmethod random_dict(keys: List[str] [✅], value_generators: Dict[str, Callable[[], Any]] [✅]) -> Dict[str, Any]` [❌ 未使用]
**Docstring**: ランダムな辞書を生成

**内部で定義される名前:**
- `generator`
- `random_dict`
- `result`


### メソッド: `@staticmethod random_list(generator: Callable[[], Any] [✅], count: int [✅]) -> List[Any]` [❌ 未使用]
**Docstring**: ランダムなリストを生成

**内部で定義される名前:**
- `random_list`


## クラス: `Factory`
**Docstring**: ファクトリーパターンを用いたテストオブジェクト生成クラス

### メソッド: `__init__(self: Any [✅], model_class: Type [✅], default_attrs: Optional[Dict[str, Any]] [✅]) -> None` [❌ 未使用]
**Docstring**: Args:
    model_class: 生成するオブジェクトのクラス
    default_attrs: デフォルトの属性

**内部で定義される名前:**
- `__init__`


### メソッド: `build(self: Any [✅]) -> Any` [✅ 使用あり]
**Docstring**: オブジェクトを生成

Args:
    **kwargs: 上書きする属性
    
Returns:
    生成されたオブジェクト

**内部で定義される名前:**
- `attrs`
- `build`


### メソッド: `build_batch(self: Any [✅], count: int [✅]) -> List[Any]` [✅ 使用あり]
**Docstring**: 複数のオブジェクトを一括生成

Args:
    count: 生成する数
    **kwargs: 上書きする属性
    
Returns:
    生成されたオブジェクトのリスト

**内部で定義される名前:**
- `build_batch`


### メソッド: `add_builder(self: Any [✅], attr_name: str [✅], builder: Callable[[], Any] [✅]) -> 'Factory'` [✅ 使用あり]
**Docstring**: カスタムビルダーを追加

Args:
    attr_name: 属性名
    builder: ビルダー関数
    
Returns:
    自身（メソッドチェーン用）

**内部で定義される名前:**
- `add_builder`


## クラス: `User`

### メソッド: `__init__(self: Any [✅], id: Any [✅], name: Any [✅], email: Any [✅], role: Any [✅]) -> None` [❌ 未使用]

**内部で定義される名前:**
- `__init__`


### メソッド: `__str__(self: Any [✅]) -> None` [❌ 未使用]

**内部で定義される名前:**
- `__str__`


## 関数: `@logger.log_execution_time slow_function() -> None` [✅ 使用あり]

**内部で定義される名前:**
- `slow_function`



--------------------------------------------------

# validator.py の解析結果

## インポート一覧
- `datetime.datetime` (✅ 使用あり)
- `re` (✅ 使用あり)
- `typing.Any` (✅ 使用あり)
- `typing.Callable` (✅ 使用あり)
- `typing.Dict` (✅ 使用あり)
- `typing.List` (✅ 使用あり)
- `typing.Optional` (✅ 使用あり)
- `typing.Set` (✅ 使用あり)
- `typing.Tuple` (✅ 使用あり)
- `typing.Type` (✅ 使用あり)
- `typing.Union` (✅ 使用あり)

## クラス: `ValidationError` (Exception)
**Docstring**: バリデーションエラー

### メソッド: `__init__(self: Any [✅], message: str [✅], path: Optional[str] [✅]) -> None` [✅ 使用あり]

**内部で定義される名前:**
- `__init__`


## クラス: `Validator`
**Docstring**: データ構造を検証するシンプルなバリデーター
辞書やリストの構造を検証し、期待される型と実際の値を比較

### メソッド: `@staticmethod validate_type(value: Any [✅], expected_type: Union[Type, Tuple[Type, ...]] [✅], path: str [✅]) -> None` [✅ 使用あり]
**Docstring**: 値の型を検証

Args:
    value: 検証する値
    expected_type: 期待される型（タプルの場合はいずれかの型）
    path: エラーメッセージ用のパス
    
Raises:
    ValidationError: 型が一致しない場合

**内部で定義される名前:**
- `actual_type_str`
- `expected_type_str`
- `type_names`
- `validate_type`


### メソッド: `@staticmethod validate_in(value: Any [✅], valid_values: List[Any] [✅], path: str [✅]) -> None` [✅ 使用あり]
**Docstring**: 値が許容値リストに含まれているか検証

Args:
    value: 検証する値
    valid_values: 許容値のリスト
    path: エラーメッセージ用のパス
    
Raises:
    ValidationError: 値が許容値に含まれない場合

**内部で定義される名前:**
- `validate_in`


### メソッド: `@staticmethod validate_length(value: Union[str, List, Dict, Set] [✅], min_length: Optional[int] [✅], max_length: Optional[int] [✅], path: str [✅]) -> None` [✅ 使用あり]
**Docstring**: 文字列、リスト、辞書、集合の長さを検証

Args:
    value: 検証する値
    min_length: 最小長さ（省略可）
    max_length: 最大長さ（省略可）
    path: エラーメッセージ用のパス
    
Raises:
    ValidationError: 長さが範囲外の場合

**内部で定義される名前:**
- `length`
- `validate_length`


### メソッド: `@staticmethod validate_range(value: Union[int, float] [✅], min_value: Optional[Union[int, float]] [✅], max_value: Optional[Union[int, float]] [✅], path: str [✅]) -> None` [✅ 使用あり]
**Docstring**: 数値の範囲を検証

Args:
    value: 検証する値
    min_value: 最小値（省略可）
    max_value: 最大値（省略可）
    path: エラーメッセージ用のパス
    
Raises:
    ValidationError: 値が範囲外の場合

**内部で定義される名前:**
- `validate_range`


### メソッド: `@staticmethod validate_regex(value: str [✅], pattern: str [✅], path: str [✅]) -> None` [✅ 使用あり]
**Docstring**: 文字列を正規表現でチェック

Args:
    value: 検証する文字列
    pattern: 正規表現パターン
    path: エラーメッセージ用のパス
    
Raises:
    ValidationError: パターンにマッチしない場合

**内部で定義される名前:**
- `validate_regex`


### メソッド: `@staticmethod validate_email(value: str [✅], path: str [✅]) -> None` [❌ 未使用]
**Docstring**: メールアドレスを検証

Args:
    value: 検証するメールアドレス
    path: エラーメッセージ用のパス
    
Raises:
    ValidationError: 無効なメールアドレスの場合

**内部で定義される名前:**
- `pattern`
- `validate_email`


### メソッド: `@staticmethod validate_date(value: str [✅], format_str: str [✅], path: str [✅]) -> None` [❌ 未使用]
**Docstring**: 日付文字列を検証

Args:
    value: 検証する日付文字列
    format_str: 日付フォーマット
    path: エラーメッセージ用のパス
    
Raises:
    ValidationError: 日付形式が不正な場合

**内部で定義される名前:**
- `validate_date`


### メソッド: `@staticmethod validate_dict_schema(value: Dict[str, Any] [✅], schema: Dict[str, Dict[str, Any]] [✅], path: str [✅]) -> None` [✅ 使用あり]
**Docstring**: 辞書のスキーマを検証

Args:
    value: 検証する辞書
    schema: スキーマ定義
    path: エラーメッセージ用のパス
    
スキーマの例:
    {
        "name": {"type": str, "required": True},
        "age": {"type": int, "required": True, "min": 0, "max": 120},
        "email": {"type": str, "required": False, "validator": validate_email}
    }
    
Raises:
    ValidationError: スキーマに適合しない場合

**内部で定義される名前:**
- `expected_type`
- `field_path`
- `field_schema`
- `is_required`
- `max_length`
- `max_value`
- `min_length`
- `min_value`
- `valid_values`
- `validate_dict_schema`
- `validator`


### メソッド: `@staticmethod validate_list_items(value: List[Any] [✅], item_validator: Callable[[Any, str], None] [✅], path: str [✅]) -> None` [✅ 使用あり]
**Docstring**: リストの各項目を検証

Args:
    value: 検証するリスト
    item_validator: 各項目を検証する関数
    path: エラーメッセージ用のパス
    
Raises:
    ValidationError: いずれかの項目が検証エラーになった場合

**内部で定義される名前:**
- `item_path`
- `validate_list_items`


## 関数: `validate_positive_int(item: Any [✅], path: Any [✅]) -> None` [❌ 未使用]

**内部で定義される名前:**
- `validate_positive_int`



--------------------------------------------------

