import os
import json
import yaml
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Union
import logging


class ConfigError(Exception):
    """設定関連のエラー"""
    pass


class ConfigManager:
    """
    JSON/YAML設定ファイルの読み込みと検証を行うユーティリティ
    環境ごとの設定マージ機能付き
    """
    
    def __init__(self, 
                 config_dir: Union[str, Path] = None,
                 env: Optional[str] = None,
                 schema: Optional[Dict[str, Any]] = None,
                 config_type: str = 'yaml'):
        """
        Args:
            config_dir: 設定ファイルが置かれているディレクトリ
            env: 環境名（development, testing, production など）
            schema: 設定ファイルのスキーマ定義（省略可）
            config_type: 設定ファイルのタイプ（'yaml' または 'json'）
        """
        self.config_dir = Path(config_dir) if config_dir else Path('config')
        self.env = env or os.environ.get('APP_ENV', 'development')
        self.schema = schema
        self.config_type = config_type.lower()
        
        if self.config_type not in ['yaml', 'json']:
            raise ConfigError(f"サポートされていない設定ファイルタイプ: {config_type}")
        
        self.file_extension = '.yaml' if self.config_type == 'yaml' else '.json'
        self.logger = logging.getLogger(__name__)
        
        # 設定を保持する辞書
        self._config = {}
        self._loaded = False
        
    def load(self, reload: bool = False) -> Dict[str, Any]:
        """
        設定ファイルを読み込む
        
        Args:
            reload: 設定を再読み込みするかどうか
            
        Returns:
            設定データ（辞書）
            
        Raises:
            ConfigError: 設定ファイル読み込みに失敗した場合
        """
        if self._loaded and not reload:
            return self._config
        
        # 読み込み順序: base.yaml/json → env固有ファイル → local上書きファイル
        config_files = [
            self.config_dir / f"base{self.file_extension}",
            self.config_dir / f"{self.env}{self.file_extension}",
            self.config_dir / f"local{self.file_extension}"
        ]
        
        # 新しい設定
        merged_config = {}
        
        for config_file in config_files:
            if not config_file.exists():
                self.logger.debug(f"設定ファイルが見つかりません（スキップします）: {config_file}")
                continue
            
            try:
                config_data = self._read_config_file(config_file)
                self.logger.debug(f"設定ファイルを読み込みました: {config_file}")
                
                # 既存設定に新しい設定をマージ
                merged_config = self._deep_merge(merged_config, config_data)
            except Exception as e:
                raise ConfigError(f"設定ファイル読み込みエラー: {config_file} - {str(e)}")
                
        # スキーマによる検証
        if self.schema:
            self._validate_config(merged_config, self.schema)
        
        self._config = merged_config
        self._loaded = True
        return self._config
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        設定値を取得
        
        Args:
            key: 設定キー（ドット区切りで階層指定可能）
            default: 設定が見つからない場合のデフォルト値
            
        Returns:
            設定値
        """
        if not self._loaded:
            self.load()
        
        if not key:
            return self._config
        
        # ドット区切りのキーを階層構造に変換
        parts = key.split('.')
        config = self._config
        
        for part in parts:
            if isinstance(config, dict) and part in config:
                config = config[part]
            else:
                return default
                
        return config
    
    def get_all(self) -> Dict[str, Any]:
        """
        すべての設定を取得
        
        Returns:
            設定データ（辞書）
        """
        if not self._loaded:
            self.load()
        return self._config
    
    def set(self, key: str, value: Any) -> None:
        """
        実行時に設定値を変更（メモリ内のみ）
        
        Args:
            key: 設定キー（ドット区切りで階層指定可能）
            value: 設定値
        """
        if not self._loaded:
            self.load()
        
        # ドット区切りのキーを階層構造に変換
        parts = key.split('.')
        config = self._config
        
        # 最後の部分以外のパスを辿る
        for part in parts[:-1]:
            if part not in config:
                config[part] = {}
            config = config[part]
        
        # 最後の部分に値を設定
        config[parts[-1]] = value
    
    def save(self, file_path: Optional[Union[str, Path]] = None) -> None:
        """
        設定をファイルに保存（オプション）
        
        Args:
            file_path: 保存先ファイルパス（省略時はlocal設定ファイル）
            
        Raises:
            ConfigError: 設定ファイル保存に失敗した場合
        """
        if not self._loaded:
            self.load()
        
        if file_path is None:
            file_path = self.config_dir / f"local{self.file_extension}"
        
        try:
            file_path = Path(file_path)
            os.makedirs(file_path.parent, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                if self.config_type == 'yaml':
                    yaml.dump(self._config, f, default_flow_style=False, allow_unicode=True)
                else:
                    json.dump(self._config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            raise ConfigError(f"設定ファイル保存エラー: {file_path} - {str(e)}")
    
    def _read_config_file(self, file_path: Path) -> Dict[str, Any]:
        """
        設定ファイルを読み込む
        
        Args:
            file_path: 設定ファイルパス
            
        Returns:
            設定データ（辞書）
            
        Raises:
            ConfigError: 設定ファイル読み込みに失敗した場合
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                if self.config_type == 'yaml':
                    return yaml.safe_load(f) or {}
                else:
                    return json.load(f)
        except Exception as e:
            raise ConfigError(f"設定ファイル読み込みエラー: {file_path} - {str(e)}")
    
    def _deep_merge(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """
        2つの設定辞書を再帰的にマージ
        
        Args:
            base: ベースとなる辞書
            override: 上書きする辞書
            
        Returns:
            マージされた辞書
        """
        result = base.copy()
        
        for key, value in override.items():
            # 両方が辞書の場合は再帰的にマージ
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def _validate_config(self, config: Dict[str, Any], schema: Dict[str, Any], path: str = '') -> None:
        """
        スキーマに基づいて設定を検証
        
        Args:
            config: 検証する設定
            schema: スキーマ定義
            path: 現在のパス（エラーメッセージ用）
            
        Raises:
            ConfigError: 検証に失敗した場合
        """
        # スキーマの定義に従って検証
        for key, schema_def in schema.items():
            current_path = f"{path}.{key}" if path else key
            
            # 必須チェック
            if schema_def.get('required', False) and key not in config:
                raise ConfigError(f"必須の設定が見つかりません: {current_path}")
            
            # 存在する場合は型チェック
            if key in config:
                value = config[key]
                expected_type = schema_def.get('type')
                
                if expected_type:
                    if expected_type == 'dict' and not isinstance(value, dict):
                        raise ConfigError(f"設定の型が不正です: {current_path} ({type(value).__name__} ≠ dict)")
                    elif expected_type == 'list' and not isinstance(value, list):
                        raise ConfigError(f"設定の型が不正です: {current_path} ({type(value).__name__} ≠ list)")
                    elif expected_type == 'str' and not isinstance(value, str):
                        raise ConfigError(f"設定の型が不正です: {current_path} ({type(value).__name__} ≠ str)")
                    elif expected_type == 'int' and not isinstance(value, int):
                        raise ConfigError(f"設定の型が不正です: {current_path} ({type(value).__name__} ≠ int)")
                    elif expected_type == 'float' and not isinstance(value, (int, float)):
                        raise ConfigError(f"設定の型が不正です: {current_path} ({type(value).__name__} ≠ float)")
                    elif expected_type == 'bool' and not isinstance(value, bool):
                        raise ConfigError(f"設定の型が不正です: {current_path} ({type(value).__name__} ≠ bool)")
                
                # 辞書の場合は再帰的に検証
                if isinstance(value, dict) and 'properties' in schema_def:
                    self._validate_config(value, schema_def['properties'], current_path)
                
                # リストの場合はアイテムを検証
                if isinstance(value, list) and 'items' in schema_def:
                    for i, item in enumerate(value):
                        item_path = f"{current_path}[{i}]"
                        
                        # アイテム型チェック
                        item_type = schema_def['items'].get('type')
                        if item_type:
                            if item_type == 'dict' and not isinstance(item, dict):
                                raise ConfigError(f"設定の型が不正です: {item_path} ({type(item).__name__} ≠ dict)")
                            elif item_type == 'str' and not isinstance(item, str):
                                raise ConfigError(f"設定の型が不正です: {item_path} ({type(item).__name__} ≠ str)")
                        
                        # アイテムが辞書の場合は再帰的に検証
                        if isinstance(item, dict) and 'properties' in schema_def['items']:
                            self._validate_config(item, schema_def['items']['properties'], item_path)
                
                # 列挙値チェック
                if 'enum' in schema_def and value not in schema_def['enum']:
                    raise ConfigError(f"設定値が許可された値ではありません: {current_path} (許可値: {schema_def['enum']})")


# 使用例
if __name__ == "__main__":
    import tempfile
    
    # テスト用の一時ディレクトリを作成
    with tempfile.TemporaryDirectory() as temp_dir:
        config_dir = Path(temp_dir)
        
        # テスト用設定ファイルを作成
        os.makedirs(config_dir, exist_ok=True)
        
        # 1. base.yaml - 基本設定
        with open(config_dir / "base.yaml", 'w', encoding='utf-8') as f:
            f.write("""
# ベース設定
app:
  name: MyApplication
  version: 1.0.0
database:
  host: localhost
  port: 5432
  name: myapp
  username: user
  password: password
logging:
  level: INFO
  file: logs/app.log
""")
        
        # 2. production.yaml - 本番環境設定
        with open(config_dir / "production.yaml", 'w', encoding='utf-8') as f:
            f.write("""
# 本番環境設定
app:
  debug: false
database:
  host: db.example.com
  password: prod_password
logging:
  level: WARNING
""")
        
        # 3. development.yaml - 開発環境設定
        with open(config_dir / "development.yaml", 'w', encoding='utf-8') as f:
            f.write("""
# 開発環境設定
app:
  debug: true
database:
  password: dev_password
logging:
  level: DEBUG
""")
        
        # 4. local.yaml - ローカル上書き設定
        with open(config_dir / "local.yaml", 'w', encoding='utf-8') as f:
            f.write("""
# ローカル上書き設定
database:
  port: 5433
  username: local_user
""")
        
        # スキーマ定義（検証用）
        config_schema = {
            'app': {
                'type': 'dict',
                'required': True,
                'properties': {
                    'name': {'type': 'str', 'required': True},
                    'version': {'type': 'str', 'required': True},
                    'debug': {'type': 'bool', 'required': False}
                }
            },
            'database': {
                'type': 'dict',
                'required': True,
                'properties': {
                    'host': {'type': 'str', 'required': True},
                    'port': {'type': 'int', 'required': True},
                    'name': {'type': 'str', 'required': True},
                    'username': {'type': 'str', 'required': True},
                    'password': {'type': 'str', 'required': True}
                }
            },
            'logging': {
                'type': 'dict',
                'required': True,
                'properties': {
                    'level': {'type': 'str', 'required': True, 'enum': ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']},
                    'file': {'type': 'str', 'required': True}
                }
            }
        }
        
        print(f"==== 設定ファイル管理テスト ({config_dir}) ====")
        
        # 1. 開発環境設定の読み込み
        print("\n1. 開発環境設定の読み込み:")
        dev_config = ConfigManager(config_dir=config_dir, env='development', schema=config_schema)
        dev_settings = dev_config.load()
        
        print(f"アプリ名: {dev_config.get('app.name')}")
        print(f"データベースホスト: {dev_config.get('database.host')}")
        print(f"データベースポート: {dev_config.get('database.port')}")
        print(f"ログレベル: {dev_config.get('logging.level')}")
        print(f"デバッグモード: {dev_config.get('app.debug')}")
        
        # 2. 本番環境設定の読み込み
        print("\n2. 本番環境設定の読み込み:")
        prod_config = ConfigManager(config_dir=config_dir, env='production', schema=config_schema)
        prod_settings = prod_config.load()
        
        print(f"アプリ名: {prod_config.get('app.name')}")
        print(f"データベースホスト: {prod_config.get('database.host')}")
        print(f"データベースポート: {prod_config.get('database.port')}")
        print(f"ログレベル: {prod_config.get('logging.level')}")
        print(f"デバッグモード: {prod_config.get('app.debug')}")
        
        # 3. 設定変更と保存
        print("\n3. 設定変更とローカル設定への保存:")
        dev_config.set('app.custom_setting', 'カスタム値')
        dev_config.set('database.max_connections', 100)
        local_file = config_dir / 'custom_local.yaml'
        dev_config.save(local_file)
        
        print(f"設定を保存しました: {local_file}")
        
        # 保存した設定を読み込み
        with open(local_file, 'r', encoding='utf-8') as f:
            saved_content = f.read()
            print(f"保存された設定内容:\n{saved_content}")
        
        # 4. JSONフォーマットでの設定
        print("\n4. JSON形式での設定:")
        # JSON設定ファイルを作成
        with open(config_dir / "base.json", 'w', encoding='utf-8') as f:
            f.write("""
{
  "app": {
    "name": "JSONApp",
    "version": "2.0.0"
  },
  "features": {
    "enabled": true,
    "modules": ["module1", "module2"]
  }
}
""")
        
        json_config = ConfigManager(config_dir=config_dir, config_type='json')
        json_settings = json_config.load()
        
        print(f"JSONアプリ名: {json_config.get('app.name')}")
        print(f"有効モジュール: {json_config.get('features.modules')}")
        
        print("\nすべてのテストが成功しました！")