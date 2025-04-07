## テスト実行に関する注意点

### Poetryを使用したテスト実行
- テストを実行する際は、必ずPoetryの仮想環境内で実行する
- 基本的なテスト実行コマンド:
  ```bash
  poetry run pytest tests/ -v
  ```
- `-v` オプションで詳細な出力を得られる
- 特定のテストファイルやディレクトリのみを実行する場合:
  ```bash
  poetry run pytest tests/test_specific_file.py -v
  poetry run pytest tests/specific_directory/ -v
  ```

### ChromaDB関連のテストについて
- 初回実行時にはembeddingモデル（all-MiniLM-L6-v2）のダウンロードが自動的に行われる
- ダウンロードには数分かかる場合がある
- モデルは `~/.cache/chroma/onnx_models/` にキャッシュされる
- 2回目以降の実行ではキャッシュされたモデルが使用される 