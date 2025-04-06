import random
import string
import uuid
import datetime
import time
import logging
from typing import Any, Callable, Dict, List, Optional, Type, Union


class TestDataGenerator:
    """
    テストケース用のダミーデータを生成するシンプルなジェネレータ
    """
    
    @staticmethod
    def random_string(length: int = 10) -> str:
        """ランダムな文字列を生成"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    @staticmethod
    def random_email() -> str:
        """ランダムなメールアドレスを生成"""
        domains = ['example.com', 'test.org', 'dummy.net', 'sample.io']
        username = TestDataGenerator.random_string(8).lower()
        domain = random.choice(domains)
        return f"{username}@{domain}"
    
    @staticmethod
    def random_date(start_year: int = 2000, end_year: int = 2023) -> datetime.date:
        """ランダムな日付を生成"""
        start_date = datetime.date(start_year, 1, 1)
        end_date = datetime.date(end_year, 12, 31)
        days_between = (end_date - start_date).days
        random_days = random.randint(0, days_between)
        return start_date + datetime.timedelta(days=random_days)
    
    @staticmethod
    def random_datetime(start_year: int = 2000, end_year: int = 2023) -> datetime.datetime:
        """ランダムな日時を生成"""
        date = TestDataGenerator.random_date(start_year, end_year)
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        return datetime.datetime.combine(date, datetime.time(hour, minute, second))
    
    @staticmethod
    def random_phone() -> str:
        """ランダムな電話番号を生成"""
        return f"0{random.randint(1, 9)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
    
    @staticmethod
    def random_uuid() -> str:
        """ランダムなUUIDを生成"""
        return str(uuid.uuid4())
    
    @staticmethod
    def random_choice(items: List[Any]) -> Any:
        """リストからランダムに1つ選択"""
        return random.choice(items)
    
    @staticmethod
    def random_bool(true_probability: float = 0.5) -> bool:
        """ランダムな真偽値を生成"""
        return random.random() < true_probability
    
    @staticmethod
    def random_dict(keys: List[str], value_generators: Dict[str, Callable[[], Any]]) -> Dict[str, Any]:
        """ランダムな辞書を生成"""
        result = {}
        for key in keys:
            generator = value_generators.get(key, lambda: TestDataGenerator.random_string())
            result[key] = generator()
        return result
    
    @staticmethod
    def random_list(generator: Callable[[], Any], count: int) -> List[Any]:
        """ランダムなリストを生成"""
        return [generator() for _ in range(count)]


class Factory:
    """
    ファクトリーパターンを用いたテストオブジェクト生成クラス
    """
    
    def __init__(self, model_class: Type, default_attrs: Optional[Dict[str, Any]] = None):
        """
        Args:
            model_class: 生成するオブジェクトのクラス
            default_attrs: デフォルトの属性
        """
        self.model_class = model_class
        self.default_attrs = default_attrs or {}
        self.custom_builders = {}
    
    def build(self, **kwargs) -> Any:
        """
        オブジェクトを生成
        
        Args:
            **kwargs: 上書きする属性
            
        Returns:
            生成されたオブジェクト
        """
        # デフォルト属性とカスタム属性をマージ
        attrs = self.default_attrs.copy()
        
        # カスタムビルダーがあれば実行
        for key, builder in self.custom_builders.items():
            if key not in kwargs:  # 明示的に上書きされていなければビルダーを使用
                attrs[key] = builder()
        
        # 引数で渡された属性で上書き
        attrs.update(kwargs)
        
        # オブジェクトを生成
        return self.model_class(**attrs)
    
    def build_batch(self, count: int, **kwargs) -> List[Any]:
        """
        複数のオブジェクトを一括生成
        
        Args:
            count: 生成する数
            **kwargs: 上書きする属性
            
        Returns:
            生成されたオブジェクトのリスト
        """
        return [self.build(**kwargs) for _ in range(count)]
    
    def add_builder(self, attr_name: str, builder: Callable[[], Any]) -> 'Factory':
        """
        カスタムビルダーを追加
        
        Args:
            attr_name: 属性名
            builder: ビルダー関数
            
        Returns:
            自身（メソッドチェーン用）
        """
        self.custom_builders[attr_name] = builder
        return self


# 使用例
if __name__ == "__main__":
    # ロガーの取得
    logger = get_logger("example_app")
    
    # 通常のログ出力
    logger.info("アプリケーション起動", app_version="1.0.0", environment="dev")
    
    # 警告ログ
    logger.warning("設定ファイルが見つかりません", config_file="config.yaml")
    
    # エラーログ（例外情報付き）
    try:
        1 / 0
    except Exception as e:
        logger.error("ゼロ除算エラー", exc_info=e, operation="division")
    
    # デコレーターの使用例
    @logger.log_execution_time
    def slow_function():
        time.sleep(1.5)
        return "完了"
    
    slow_function()
    
    # ログレベルの変更
    logger.set_level(logging.DEBUG)
    logger.debug("詳細なデバッグ情報", variable_x=42, status="checking")

    # 1. シンプルなデータ生成
    print("==== 基本的なランダムデータ ====")
    print(f"ランダム文字列: {TestDataGenerator.random_string()}")
    print(f"ランダムメール: {TestDataGenerator.random_email()}")
    print(f"ランダム日付: {TestDataGenerator.random_date()}")
    print(f"ランダム日時: {TestDataGenerator.random_datetime()}")
    print(f"ランダム電話: {TestDataGenerator.random_phone()}")
    print(f"ランダムUUID: {TestDataGenerator.random_uuid()}")
    
    # 2. ファクトリーパターンの使用例
    print("\n==== ファクトリーパターンの使用例 ====")
    
    # ユーザーモデルの定義（例）
    class User:
        def __init__(self, id=None, name=None, email=None, role=None):
            self.id = id
            self.name = name
            self.email = email
            self.role = role
            
        def __str__(self):
            return f"User(id={self.id}, name={self.name}, email={self.email}, role={self.role})"
    
    # ユーザーファクトリーの作成
    user_factory = Factory(
        User,
        default_attrs={
            'role': 'user'
        }
    )
    
    # カスタムビルダーを追加
    user_factory.add_builder('id', TestDataGenerator.random_uuid)
    user_factory.add_builder('name', lambda: f"User {TestDataGenerator.random_string(4)}")
    user_factory.add_builder('email', TestDataGenerator.random_email)
    
    # 単一のユーザーを生成
    user = user_factory.build()
    print(f"\n生成されたユーザー: {user}")
    
    # 管理者ユーザーを生成（属性を上書き）
    admin = user_factory.build(role='admin')
    print(f"生成された管理者: {admin}")
    
    # 複数のユーザーを一括生成
    users = user_factory.build_batch(3)
    print("\n一括生成されたユーザー:")
    for u in users:
        print(f"  {u}")