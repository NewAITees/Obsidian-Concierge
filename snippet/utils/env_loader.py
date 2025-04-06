import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Union, Any


class EnvLoader:
    """
    環境に応じて .env ファイルを読み込むユーティリティ
    必須環境変数のチェック機能付き
    """
    
    def __init__(self, 
                 base_dir: Optional[str] = None,
                 env: Optional[str] = None,
                 required_vars: Optional[List[str]] = None):
        """
        Args:
            base_dir: .env ファイルが置かれているディレクトリ
            env: 環境名 (development, testing, production など)
            required_vars: 必須の環境変数リスト
        """
        self.base_dir = Path(base_dir or os.getcwd())
        self.env = env or os.environ.get('ENV', 'development')
        self.required_vars = required_vars or []
        self.loaded = False
    
    def load(self, override: bool = False) -> Dict[str, str]:
        """
        環境変数をロード
        
        Args:
            override: 既存の環境変数を上書きするかどうか
            
        Returns:
            ロードされた環境変数の辞書
        
        Raises:
            ValueError: 必須環境変数が見つからない場合
            FileNotFoundError: .env ファイルが見つからない場合
        """
        loaded_vars = {}
        
        # 環境変数ファイルのリスト
        env_files = [
            self.base_dir / '.env',                 # 基本の .env
            self.base_dir / f'.env.{self.env}',     # 環境別の .env
            self.base_dir / f'.env.{self.env}.local' # ローカル環境の上書き
        ]
        
        # ファイルをロード
        for env_file in env_files:
            if env_file.exists():
                file_vars = self._parse_env_file(env_file)
                loaded_vars.update(file_vars)
        
        # 環境変数を設定
        for key, value in loaded_vars.items():
            if override or key not in os.environ:
                os.environ[key] = value
        
        # 必須環境変数の確認
        missing_vars = []
        for var in self.required_vars:
            if var not in os.environ:
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(
                f"必須環境変数が設定されていません: {', '.join(missing_vars)}"
            )
        
        self.loaded = True
        return loaded_vars
    
    def _parse_env_file(self, file_path: Path) -> Dict[str, str]:
        """
        .env ファイルをパース
        
        Args:
            file_path: .env ファイルのパス
            
        Returns:
            パースされた環境変数の辞書
        """
        result = {}
        
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                
                # コメントや空行をスキップ
                if not line or line.startswith('#'):
                    continue
                
                # KEY=VALUE の形式をパース
                match = re.match(r'^([A-Za-z_0-9]+)=(.*?)$', line)
                if match:
                    key, value = match.groups()
                    
                    # 引用符を取り除く
                    value = value.strip('\'"')
                    
                    result[key] = value
        
        return result
    
    def get(self, key: str, default: Any = None, as_type: Optional[type] = None) -> Any:
        """
        環境変数を取得（オプションで型変換）
        
        Args:
            key: 環境変数名
            default: デフォルト値
            as_type: 型変換関数（int, float, bool など）
            
        Returns:
            環境変数の値（変換後）
        """
        if not self.loaded:
            self.load()
        
        value = os.environ.get(key, default)
        
        if value is not None and as_type is not None:
            # 特別な処理（bool型）
            if as_type is bool and isinstance(value, str):
                return value.lower() in ('true', 'yes', '1', 'y', 'on')
            return as_type(value)
        
        return value


# 使用例
if __name__ == "__main__":
    # サンプル .env ファイルを作成
    with open('.env', 'w') as f:
        f.write("""
# データベース設定
DB_HOST=localhost
DB_PORT=5432
DB_USER=admin
DB_PASSWORD=secret

# アプリケーション設定
APP_DEBUG=true
APP_PORT=8000
""")
    
    # 開発環境用の .env ファイルを作成
    with open('.env.development', 'w') as f:
        f.write("""
# 開発環境のみの設定
APP_DEBUG=true
LOG_LEVEL=DEBUG
""")
    
    try:
        # 環境変数をロード（必須項目チェック付き）
        env_loader = EnvLoader(required_vars=['DB_HOST', 'DB_USER', 'DB_PASSWORD'])
        loaded_vars = env_loader.load()
        
        print("ロードされた環境変数:")
        for key, value in loaded_vars.items():
            print(f"  {key}={value}")
        
        # 型変換付きで環境変数を取得
        debug_mode = env_loader.get('APP_DEBUG', as_type=bool)
        app_port = env_loader.get('APP_PORT', as_type=int)
        log_level = env_loader.get('LOG_LEVEL', default='INFO')
        
        print(f"\n使用される設定:")
        print(f"  デバッグモード: {debug_mode} (型: {type(debug_mode)})")
        print(f"  アプリポート: {app_port} (型: {type(app_port)})")
        print(f"  ログレベル: {log_level}")
        
    finally:
        # サンプルファイルを削除
        for file in ['.env', '.env.development']:
            if os.path.exists(file):
                os.remove(file)