@echo off
:: 仮想環境が有効でない場合は有効化
if not defined VIRTUAL_ENV (
    if exist ai_chat\Scripts\activate.bat (
        call ai_chat\Scripts\activate.bat
    ) else (
        echo 仮想環境が見つかりません。
        exit /b 1
    )
)

:: Pythonスクリプトを実行
python scripts\check.py
if errorlevel 1 (
    echo チェックに失敗しました。
    exit /b 1
)

echo すべてのチェックが完了しました。
exit /b 0
