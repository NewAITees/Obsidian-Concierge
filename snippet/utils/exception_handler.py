import functools
import logging
import traceback
import sys
import os

# ログ設定
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def exception_handler(reraise=True, log_level=logging.ERROR, 
                      production_mode=None, default_return=None):
    """
    関数実行時の例外を捕捉し詳細情報を記録するデコレータ
    
    Args:
        reraise: 例外を再スローするかどうか
        log_level: ログレベル
        production_mode: 本番環境モードフラグ（Noneの場合はPRODUCTION環境変数を使用）
        default_return: 例外発生時のデフォルト戻り値
    
    Returns:
        デコレートされた関数
    """
    # 本番環境かどうかのチェック
    if production_mode is None:
        production_mode = os.environ.get('PRODUCTION', 'false').lower() == 'true'
    
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # 呼び出し情報の収集
                func_name = func.__name__
                module_name = func.__module__
                
                # エラーメッセージの作成
                error_message = f"例外が発生しました: {module_name}.{func_name} - {str(e)}"
                
                # 本番環境と開発環境で詳細度を変える
                if production_mode:
                    # 本番環境: シンプルなエラーメッセージ
                    logger.log(log_level, error_message)
                else:
                    # 開発環境: 詳細なトレースバック
                    detailed_message = f"{error_message}\n詳細: {traceback.format_exc()}"
                    logger.log(log_level, detailed_message)
                
                # 例外を再スローするかどうか
                if reraise:
                    raise
                
                # デフォルト値を返す
                return default_return
        
        return wrapper
    
    return decorator


# 使用例
if __name__ == "__main__":
    # 開発環境の例（詳細なトレースバックを表示）
    @exception_handler(production_mode=False)
    def divide(a, b):
        return a / b
    
    # 本番環境の例（シンプルなエラーメッセージのみ）
    @exception_handler(production_mode=True, reraise=False, default_return=0)
    def risky_operation(items):
        return items[10]
    
    # 例外をキャッチしてログに記録し、再スロー
    try:
        result = divide(10, 0)
    except Exception as e:
        print(f"メイン処理でキャッチ: {e}")
    
    # 例外をキャッチしてログに記録し、デフォルト値を返す
    result = risky_operation([1, 2, 3])
    print(f"リスキー操作の結果: {result}")  # 0が返される