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

:: 必要なパッケージのインストール
echo 開発用パッケージをインストールしています...
pip install -r requirements.txt

:: pre-commitのインストールと設定
echo pre-commitをインストールしています...
pip install pre-commit
pre-commit install

:: Gitフックの設定
echo Gitフックを設定しています...
pre-commit install --hook-type pre-commit
pre-commit install --hook-type pre-push

echo 開発環境のセットアップが完了しました。
exit /b 0
