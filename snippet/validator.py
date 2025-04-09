import re
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union, Type


class ValidationError(Exception):
    """バリデーションエラー"""
    
    def __init__(self, message: str, path: Optional[str] = None):
        self.message = message
        self.path = path
        super().__init__(f"{path}: {message}" if path else message)


class Validator:
    """
    データ構造を検証するシンプルなバリデーター
    辞書やリストの構造を検証し、期待される型と実際の値を比較
    """
    
    @staticmethod
    def validate_type(value: Any, expected_type: Union[Type, Tuple[Type, ...]], path: str = "value") -> None:
        """
        値の型を検証
        
        Args:
            value: 検証する値
            expected_type: 期待される型（タプルの場合はいずれかの型）
            path: エラーメッセージ用のパス
            
        Raises:
            ValidationError: 型が一致しない場合
        """
        if not isinstance(value, expected_type):
            if isinstance(expected_type, tuple):
                type_names = [t.__name__ for t in expected_type]
                expected_type_str = " または ".join(type_names)
            else:
                expected_type_str = expected_type.__name__
                
            actual_type_str = type(value).__name__
            raise ValidationError(
                f"型が一致しません。期待: {expected_type_str}, 実際: {actual_type_str}", 
                path
            )
    
    @staticmethod
    def validate_in(value: Any, valid_values: List[Any], path: str = "value") -> None:
        """
        値が許容値リストに含まれているか検証
        
        Args:
            value: 検証する値
            valid_values: 許容値のリスト
            path: エラーメッセージ用のパス
            
        Raises:
            ValidationError: 値が許容値に含まれない場合
        """
        if value not in valid_values:
            raise ValidationError(
                f"値が許容されていません。許容値: {valid_values}", 
                path
            )
    
    @staticmethod
    def validate_length(value: Union[str, List, Dict, Set], 
                         min_length: Optional[int] = None, 
                         max_length: Optional[int] = None, 
                         path: str = "value") -> None:
        """
        文字列、リスト、辞書、集合の長さを検証
        
        Args:
            value: 検証する値
            min_length: 最小長さ（省略可）
            max_length: 最大長さ（省略可）
            path: エラーメッセージ用のパス
            
        Raises:
            ValidationError: 長さが範囲外の場合
        """
        length = len(value)
        
        if min_length is not None and length < min_length:
            raise ValidationError(
                f"長さが短すぎます。最小: {min_length}, 実際: {length}", 
                path
            )
            
        if max_length is not None and length > max_length:
            raise ValidationError(
                f"長さが長すぎます。最大: {max_length}, 実際: {length}", 
                path
            )
    
    @staticmethod
    def validate_range(value: Union[int, float], 
                       min_value: Optional[Union[int, float]] = None, 
                       max_value: Optional[Union[int, float]] = None, 
                       path: str = "value") -> None:
        """
        数値の範囲を検証
        
        Args:
            value: 検証する値
            min_value: 最小値（省略可）
            max_value: 最大値（省略可）
            path: エラーメッセージ用のパス
            
        Raises:
            ValidationError: 値が範囲外の場合
        """
        if min_value is not None and value < min_value:
            raise ValidationError(
                f"値が小さすぎます。最小: {min_value}, 実際: {value}", 
                path
            )
            
        if max_value is not None and value > max_value:
            raise ValidationError(
                f"値が大きすぎます。最大: {max_value}, 実際: {value}", 
                path
            )
    
    @staticmethod
    def validate_regex(value: str, pattern: str, path: str = "value") -> None:
        """
        文字列を正規表現でチェック
        
        Args:
            value: 検証する文字列
            pattern: 正規表現パターン
            path: エラーメッセージ用のパス
            
        Raises:
            ValidationError: パターンにマッチしない場合
        """
        if not re.match(pattern, value):
            raise ValidationError(
                f"パターンにマッチしません: {pattern}", 
                path
            )
    
    @staticmethod
    def validate_email(value: str, path: str = "email") -> None:
        """
        メールアドレスを検証
        
        Args:
            value: 検証するメールアドレス
            path: エラーメッセージ用のパス
            
        Raises:
            ValidationError: 無効なメールアドレスの場合
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        try:
            Validator.validate_regex(value, pattern, path)
        except ValidationError:
            raise ValidationError("無効なメールアドレスです", path)
    
    @staticmethod
    def validate_date(value: str, format_str: str = "%Y-%m-%d", path: str = "date") -> None:
        """
        日付文字列を検証
        
        Args:
            value: 検証する日付文字列
            format_str: 日付フォーマット
            path: エラーメッセージ用のパス
            
        Raises:
            ValidationError: 日付形式が不正な場合
        """
        try:
            datetime.strptime(value, format_str)
        except ValueError:
            raise ValidationError(f"無効な日付形式です。期待: {format_str}", path)
    
    @staticmethod
    def validate_dict_schema(value: Dict[str, Any], schema: Dict[str, Dict[str, Any]], path: str = "") -> None:
        """
        辞書のスキーマを検証
        
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
        """
        # 型チェック
        Validator.validate_type(value, dict, path)
        
        # 必須キーのチェック
        for key, field_schema in schema.items():
            is_required = field_schema.get("required", False)
            
            if is_required and key not in value:
                raise ValidationError(f"必須キーがありません: {key}", path)
        
        # 各フィールドの検証
        for key, val in value.items():
            if key not in schema:
                continue
            
            field_schema = schema[key]
            field_path = f"{path}.{key}" if path else key
            
            # 型検証
            expected_type = field_schema.get("type")
            if expected_type and val is not None:
                Validator.validate_type(val, expected_type, field_path)
            
            # 数値範囲検証
            if isinstance(val, (int, float)):
                min_value = field_schema.get("min")
                max_value = field_schema.get("max")
                if min_value is not None or max_value is not None:
                    Validator.validate_range(val, min_value, max_value, field_path)
            
            # 長さ検証
            if isinstance(val, (str, list, dict, set)):
                min_length = field_schema.get("min_length")
                max_length = field_schema.get("max_length")
                if min_length is not None or max_length is not None:
                    Validator.validate_length(val, min_length, max_length, field_path)
            
            # 許容値リスト検証
            valid_values = field_schema.get("values")
            if valid_values is not None:
                Validator.validate_in(val, valid_values, field_path)
            
            # カスタムバリデーター
            validator = field_schema.get("validator")
            if validator and callable(validator):
                validator(val, field_path)
    
    @staticmethod
    def validate_list_items(value: List[Any], item_validator: Callable[[Any, str], None], path: str = "list") -> None:
        """
        リストの各項目を検証
        
        Args:
            value: 検証するリスト
            item_validator: 各項目を検証する関数
            path: エラーメッセージ用のパス
            
        Raises:
            ValidationError: いずれかの項目が検証エラーになった場合
        """
        Validator.validate_type(value, list, path)
        
        for i, item in enumerate(value):
            item_path = f"{path}[{i}]"
            item_validator(item, item_path)


# 使用例
if __name__ == "__main__":
    # 1. シンプルな型検証
    try:
        print("==== 型検証 ====")
        Validator.validate_type("test", str)
        Validator.validate_type(123, int)
        Validator.validate_type(True, bool)
        Validator.validate_type([1, 2, 3], list)
        Validator.validate_type({"a": 1}, dict)
        
        # 複数の型を許容
        Validator.validate_type(123, (int, float, str))
        Validator.validate_type("123", (int, float, str))
        
        # エラーケース
        Validator.validate_type("test", int)
    except ValidationError as e:
        print(f"検証エラー: {e}")
    
    # 2. 辞書スキーマ検証
    print("\n==== 辞書スキーマ検証 ====")
    
    # ユーザースキーマ定義
    user_schema = {
        "name": {"type": str, "required": True, "min_length": 2, "max_length": 50},
        "age": {"type": int, "required": True, "min": 0, "max": 120},
        "email": {"type": str, "required": True, "validator": Validator.validate_email},
        "role": {"type": str, "required": False, "values": ["admin", "user", "guest"]}
    }
    
    # 有効なユーザーデータ
    valid_user = {
        "name": "John Doe",
        "age": 30,
        "email": "john@example.com",
        "role": "admin"
    }
    
    # 無効なユーザーデータ
    invalid_user = {
        "name": "A",  # min_length=2 に違反
        "age": 150,   # max=120 に違反
        "email": "invalid-email",  # メールアドレス形式に違反
        "role": "superuser"  # 許容値に含まれない
    }
    
    try:
        # 有効なデータの検証
        Validator.validate_dict_schema(valid_user, user_schema)
        print("有効なユーザーデータ: 検証成功")
        
        # 無効なデータの検証
        Validator.validate_dict_schema(invalid_user, user_schema)
    except ValidationError as e:
        print(f"無効なユーザーデータ: 検証エラー - {e}")
    
    # 3. リスト検証
    print("\n==== リスト検証 ====")
    
    # 各項目が正の整数であることを検証する関数
    def validate_positive_int(item, path):
        Validator.validate_type(item, int, path)
        Validator.validate_range(item, min_value=1, path=path)
    
    try:
        # 有効なリスト
        valid_list = [1, 5, 10, 20]
        Validator.validate_list_items(valid_list, validate_positive_int)
        print("有効なリスト: 検証成功")
        
        # 無効なリスト
        invalid_list = [1, -5, 10, "20"]
        Validator.validate_list_items(invalid_list, validate_positive_int)
    except ValidationError as e:
        print(f"無効なリスト: 検証エラー - {e}")