# Python Development Rules

## Import Organization
- 標準ライブラリ
- サードパーティ
- ローカルインポート

## Error Handling
- 具体的な例外クラスを使用
- ログを適切に出力
- ユーザーフレンドリーなエラーメッセージ

## Type Hints
- すべての関数に型ヒントを付ける
- pydanticモデルを活用
- Anyタイプは最終手段

## Code Style
- ruffによる自動フォーマット使用
- Google スタイルdocstring必須
- pathlib.Path使用（os.path禁止）
- async/await パターンでI/O操作