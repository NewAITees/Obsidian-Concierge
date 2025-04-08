import json
import logging
import inspect
import os
import time
from datetime import datetime
from functools import wraps
from logging.handlers import RotatingFileHandler
import traceback


class ContextualLogger:
    """
    コンテキスト情報（ファイル名、関数名、行番号）を自動的に付加する
    構造化ロガークラス。JSON形式でログを出力し、ログレベルを一括制御できる。
    """

    def __init__(self, name=None, log_dir='logs', log_level=logging.INFO, 
                 max_bytes=10*1024*1024, backup_count=5):
        """
        ロガーの初期化
        
        Args:
            name (str, optional): ロガー名。指定しない場合は呼び出し元モジュール名
            log_dir (str): ログファイルを保存するディレクトリ
            log_level (int): デフォルトのログレベル
            max_bytes (int): ログファイルの最大サイズ
            backup_count (int): 保持するバックアップファイル数
        """
        self.log_level = log_level
        
        # 呼び出し元情報を取得してロガー名を決定
        if name is None:
            frame = inspect.stack()[1]
            module = inspect.getmodule(frame[0])
            name = module.__name__ if module else 'root'
        
        # ロガーの設定
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        
        # 同じハンドラーが重複して追加されるのを防ぐ
        if not self.logger.handlers:
            # ログディレクトリがなければ作成
            os.makedirs(log_dir, exist_ok=True)
            
            # アプリケーションログ（通常ログ）
            app_log_path = os.path.join(log_dir, 'application')
            os.makedirs(app_log_path, exist_ok=True)
            app_log_file = os.path.join(app_log_path, f'app-{datetime.now().strftime("%Y-%m-%d")}.log')
            
            # エラーログ（ERRORとCRITICAL）
            error_log_path = os.path.join(log_dir, 'error')
            os.makedirs(error_log_path, exist_ok=True)
            error_log_file = os.path.join(error_log_path, f'error-{datetime.now().strftime("%Y-%m-%d")}.log')
            
            # 通常ログのハンドラ設定
            app_handler = RotatingFileHandler(
                app_log_file, maxBytes=max_bytes, backupCount=backup_count, mode='a'
            )
            app_handler.setLevel(log_level)
            app_handler.setFormatter(logging.Formatter('%(message)s'))
            self.logger.addHandler(app_handler)
            
            # エラーログのハンドラ設定
            error_handler = RotatingFileHandler(
                error_log_file, maxBytes=max_bytes, backupCount=backup_count, mode='a'
            )
            error_handler.setLevel(logging.ERROR)
            error_handler.setFormatter(logging.Formatter('%(message)s'))
            self.logger.addHandler(error_handler)
            
            # コンソール出力用ハンドラ
            console_handler = logging.StreamHandler()
            console_handler.setLevel(log_level)
            console_handler.setFormatter(logging.Formatter('%(message)s'))
            self.logger.addHandler(console_handler)

    def _get_context_info(self):
        """呼び出し元のコンテキスト情報（ファイル名、関数名、行番号）を取得"""
        frame = inspect.currentframe().f_back.f_back  # 2レベル上の呼び出し元
        filename = os.path.basename(frame.f_code.co_filename)
        function_name = frame.f_code.co_name
        line_number = frame.f_lineno
        
        return {
            "file": filename,
            "function": function_name,
            "line": line_number,
            "timestamp": datetime.now().isoformat(),
            "unix_timestamp": time.time()
        }

    def _format_log(self, message, level, extra=None):
        """ログメッセージをJSON形式に整形"""
        log_data = self._get_context_info()
        log_data["message"] = message
        log_data["level"] = logging.getLevelName(level)
        
        # 追加情報があれば追加
        if extra:
            # 機密情報をマスク処理
            masked_extra = self._mask_sensitive_data(extra)
            log_data.update(masked_extra)
            
        return json.dumps(log_data)

    def _mask_sensitive_data(self, data):
        """機密情報をマスク処理"""
        sensitive_keys = ['password', 'token', 'secret', 'credit_card', 'ssn']
        masked_data = {}
        
        for key, value in data.items():
            if any(sensitive in key.lower() for sensitive in sensitive_keys):
                masked_data[key] = '********'
            else:
                masked_data[key] = value
                
        return masked_data

    def debug(self, message, **extra):
        """DEBUGレベルのログ出力"""
        self.logger.debug(self._format_log(message, logging.DEBUG, extra))
        
    def info(self, message, **extra):
        """INFOレベルのログ出力"""
        self.logger.info(self._format_log(message, logging.INFO, extra))
        
    def warning(self, message, **extra):
        """WARNINGレベルのログ出力"""
        self.logger.warning(self._format_log(message, logging.WARNING, extra))
        
    def error(self, message, exc_info=None, **extra):
        """ERRORレベルのログ出力。例外情報も記録可能"""
        if exc_info:
            extra['exception'] = str(exc_info)
            extra['traceback'] = traceback.format_exc()
        self.logger.error(self._format_log(message, logging.ERROR, extra))
        
    def critical(self, message, exc_info=None, **extra):
        """CRITICALレベルのログ出力。例外情報も記録可能"""
        if exc_info:
            extra['exception'] = str(exc_info)
            extra['traceback'] = traceback.format_exc()
        self.logger.critical(self._format_log(message, logging.CRITICAL, extra))

    def set_level(self, level):
        """ログレベルを変更"""
        self.log_level = level
        self.logger.setLevel(level)
        for handler in self.logger.handlers:
            if handler.level < logging.ERROR:  # エラーログハンドラは除外
                handler.setLevel(level)

    def log_execution_time(self, func):
        """関数の実行時間をログに記録するデコレーター"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            self.info(
                f"Function executed: {func.__name__}",
                execution_time_ms=round(execution_time * 1000),
                execution_time_s=round(execution_time, 3)
            )
            return result
        return wrapper


# 便利な使用のためのシングルトンインスタンス
def get_logger(name=None, log_dir='logs', log_level=None):
    """アプリケーション全体で利用可能なロガーインスタンスを取得"""
    if log_level is None:
        # 環境変数からログレベルを取得（デフォルトはINFO）
        log_level_name = os.environ.get('LOG_LEVEL', 'INFO')
        log_level = getattr(logging, log_level_name, logging.INFO)
    
    return ContextualLogger(name=name, log_dir=log_dir, log_level=log_level)


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