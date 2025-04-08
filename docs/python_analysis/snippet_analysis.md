# snippet フォルダのPython解析レポート

生成日時: 2025-04-08 20:40:21.741961

==================================================

# cli.py の解析結果

## インポート一覧
- `analytics.code_analyzer.CodeAnalyzer` (❌ 未使用)
- `analytics.code_analyzer.analyze_directory` (✅ 使用あり)
- `analytics.code_analyzer.analyze_file` (✅ 使用あり)
- `analytics.report_generator.generate_report` (✅ 使用あり)
- `analytics.report_generator.save_report` (✅ 使用あり)
- `analytics.validator_integration.validate_functions` (✅ 使用あり)
- `argparse` (✅ 使用あり)
- `cli.main` (✅ 使用あり)
- `importlib.util` (❌ 未使用)
- `json` (✅ 使用あり)
- `os` (✅ 使用あり)
- `pathlib.Path` (❌ 未使用)
- `sys` (✅ 使用あり)
- `typing.Any` (✅ 使用あり)
- `typing.Dict` (✅ 使用あり)
- `typing.List` (✅ 使用あり)
- `typing.Optional` (✅ 使用あり)

## 関数: `generate_enhanced_report(code_analysis_results: Dict[str, Any] [✅], validator_results: Optional[Dict[str, Any]] [✅], output_file: str [✅], format: str [✅]) -> str` [✅ 使用あり]
**Docstring**: コード分析と関数検証の結果を統合したレポートを生成

Args:
    code_analysis_results: コード分析の結果
    validator_results: 関数検証の結果（オプション）
    output_file: 出力ファイルパス（省略時は返すだけ）
    format: 出力フォーマット

Returns:
    生成されたレポート、または保存したファイルパス

**内部で定義される名前:**
- `combined_results`
- `generate_enhanced_report`
- `report`
- `validator_report`


## 関数: `_generate_validator_report(results: Dict[str, Any] [✅], format: str [✅]) -> str` [✅ 使用あり]
**Docstring**: 関数検証結果のレポートを生成

Args:
    results: 関数検証の結果
    format: 出力フォーマット

Returns:
    フォーマット済みレポート

**内部で定義される名前:**
- `_generate_validator_report`
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


## 関数: `main(args: Optional[List[str]] [✅]) -> int` [✅ 使用あり]
**Docstring**: コマンドライン実行のメインエントリーポイント

Args:
    args: コマンドライン引数（テスト用、通常はNone）
    
Returns:
    終了コード

**内部で定義される名前:**
- `analyze_parser`
- `args`
- `check_parser`
- `code_analysis_results`
- `enhanced_parser`
- `main`
- `output_file`
- `parser`
- `path`
- `report_parser`
- `results`
- `save_data`
- `stats`
- `subparsers`
- `summary`
- `validate_parser`
- `validator_report`
- `validator_results`



--------------------------------------------------

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

