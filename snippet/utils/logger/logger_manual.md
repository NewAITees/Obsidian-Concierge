"""
サンプルのロガー設定ファイル（logging_config.yaml）
コード内でこのように読み込みます：

import yaml
from contextual_logger import ContextualLogger

with open('logging_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

logger = ContextualLogger(
    name=config['logger']['name'],
    log_dir=config['logger']['log_dir'],
    log_level=getattr(logging, config['logger']['log_level']),
    max_bytes=config['logger']['max_bytes'],
    backup_count=config['logger']['backup_count']
)
"""

logger:
  name: app
  log_dir: logs
  log_level: INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
  max_bytes: 10485760  # 10MB
  backup_count: 5

environments:
  development:
    log_level: DEBUG
    console_output: true
  testing:
    log_level: INFO
    console_output: true
  production:
    log_level: WARNING
    console_output: false

sensitive_keys:
  - password
  - token
  - secret
  - api_key
  - credit_card
  - ssn

# 異なるサービスごとのログレベル
service_log_levels:
  database: INFO
  api: DEBUG
  auth: WARNING
  scheduler: INFO