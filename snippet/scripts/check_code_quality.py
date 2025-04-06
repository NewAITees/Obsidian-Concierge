#!/usr/bin/env python3
"""コードの品質チェックを行うスクリプト"""

import subprocess
import sys
from pathlib import Path


def run_check(command: list[str], description: str) -> tuple[bool, str]:
    """コマンドを実行してチェックを行う

    Args:
        command (List[str]): 実行するコマンド
        description (str): チェックの説明

    Returns:
        Tuple[bool, str]: チェックの結果（成功したかどうか）とエラーメッセージ
    """
    print(f"\nチェック: {description}...")
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
            shell=False,  # シェルインジェクションを防ぐ
        )
        if result.returncode != 0:
            return False, result.stderr or result.stdout
        return True, ""
    except subprocess.SubprocessError as e:
        return False, str(e)


def main() -> int:
    """メイン関数"""
    # 必要なチェックを実行
    checks = [
        (["ruff", "check", "."], "Ruffによるコードチェック"),
        (["mypy", "."], "MypyによるPythonの型チェック"),
        (["pytest"], "Pytestによるテスト実行"),
        (["bandit", "-r", "."], "Banditによるセキュリティチェック"),
    ]

    failed = False
    for command, description in checks:
        success, error = run_check(command, description)
        if not success:
            print(f"エラー: {description}に失敗しました")
            print(error)
            failed = True

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
