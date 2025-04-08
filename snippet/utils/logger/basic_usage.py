"""
コンテキスト付き構造化ロガーの使用例
"""
from contextual_logger import get_logger
import time
import os

# 環境変数でログレベルを制御可能
# os.environ['LOG_LEVEL'] = 'DEBUG'

# 基本的な使い方
def basic_usage():
    # ロガーの取得
    logger = get_logger("my_application")
    
    # 各種ログレベルでのログ出力
    logger.debug("これはデバッグメッセージです")
    logger.info("ユーザーがログインしました", user_id=12345, ip_address="192.168.1.1")
    logger.warning("ディスク使用率が高くなっています", usage_percent=85)
    logger.error("データベース接続エラー", db_name="users", retry_count=3)
    logger.critical("アプリケーションがクラッシュします", memory_usage="2.5GB")
    
    # ログレベルの変更
    logger.set_level(10)  # DEBUG=10, INFO=20, WARNING=30, ERROR=40, CRITICAL=50
    logger.debug("デバッグが有効になりました")


# 例外ハンドリングの例
def exception_example():
    logger = get_logger("error_handler")
    
    try:
        # 意図的にエラーを発生させる
        result = 100 / 0
    except Exception as e:
        # 例外情報付きでエラーログを出力
        logger.error(
            "計算処理中にエラーが発生しました", 
            exc_info=e, 
            operation="division",
            input_value=100
        )


# デコレーターを使用した例
def decorator_example():
    logger = get_logger("performance")
    
    @logger.log_execution_time
    def slow_database_query(query_id):
        # 重い処理のシミュレーション
        time.sleep(1.2)
        return {"id": query_id, "results": ["データ1", "データ2"]}
    
    # 関数を実行すると、実行時間が自動的にログに記録される
    result = slow_database_query(42)
    print(f"クエリ結果: {result}")


# 複数のモジュールでの利用
class UserService:
    def __init__(self):
        # クラス専用のロガーを取得
        self.logger = get_logger("UserService")
    
    def get_user(self, user_id):
        self.logger.info("ユーザー情報を取得します", user_id=user_id)
        # ユーザー取得の処理...
        return {"id": user_id, "name": "テストユーザー"}


# 機密情報のマスキング
def security_example():
    logger = get_logger("security")
    
    # パスワードなどの機密情報は自動的にマスクされる
    logger.info(
        "認証処理", 
        username="testuser",
        password="secret123",  # 自動的にマスクされる
        token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",  # 自動的にマスクされる
        request_ip="192.168.0.1"  # 機密ではないので表示される
    )


if __name__ == "__main__":
    print("=== 基本的な使用例 ===")
    basic_usage()
    
    print("\n=== 例外ハンドリングの例 ===")
    exception_example()
    
    print("\n=== パフォーマンス測定の例 ===")
    decorator_example()
    
    print("\n=== クラスでの使用例 ===")
    user_service = UserService()
    user_service.get_user(123)
    
    print("\n=== セキュリティの例 ===")
    security_example()