# obsidian_concierge/indexer フォルダのPython解析レポート

生成日時: 2025-04-08 20:40:21.555028

==================================================

# vault_indexer.py の解析結果

## インポート一覧
- `datetime.datetime` (✅ 使用あり)
- `db.chroma.ChromaRepository` (✅ 使用あり)
- `db.chroma.Document` (✅ 使用あり)
- `hashlib` (✅ 使用あり)
- `os` (❌ 未使用)
- `pathlib.Path` (✅ 使用あり)
- `typing.Any` (✅ 使用あり)
- `typing.Dict` (✅ 使用あり)
- `typing.Generator` (✅ 使用あり)
- `typing.List` (✅ 使用あり)
- `utils.config.config` (❌ 未使用)
- `utils.fs.is_text_file` (✅ 使用あり)
- `utils.fs.list_files` (✅ 使用あり)
- `utils.logging.logger` (✅ 使用あり)

## クラス: `VaultIndexer`
**Docstring**: Class for indexing Obsidian vault contents.

### メソッド: `__init__(self: Any [✅], vault_path: str [✅], repo: ChromaRepository [✅]) -> None` [❌ 未使用]
**Docstring**: Initialize vault indexer.

Args:
    vault_path: Path to Obsidian vault
    repo: ChromaDB repository instance

**内部で定義される名前:**
- `__init__`


### メソッド: `_read_markdown_file(self: Any [❌], file_path: Path [✅]) -> str` [✅ 使用あり]
**Docstring**: Read and preprocess markdown file content.

Args:
    file_path: Path to markdown file
    
Returns:
    Preprocessed file content

**内部で定義される名前:**
- `_read_markdown_file`
- `content`


### メソッド: `_generate_document_id(self: Any [✅], file_path: Path [✅]) -> str` [✅ 使用あり]
**Docstring**: Generate unique document ID for a file.

Args:
    file_path: Path to file
    
Returns:
    Unique document ID

**内部で定義される名前:**
- `_generate_document_id`
- `rel_path`


### メソッド: `_get_file_metadata(self: Any [✅], file_path: Path [✅]) -> Dict[str, Any]` [✅ 使用あり]
**Docstring**: Extract metadata from file.

Args:
    file_path: Path to file
    
Returns:
    File metadata

**内部で定義される名前:**
- `_get_file_metadata`
- `rel_path`
- `stat`


### メソッド: `_scan_vault_files(self: Any [✅]) -> Generator[Path, None, None]` [✅ 使用あり]
**Docstring**: Scan vault directory for markdown files.

Yields:
    Paths to markdown files

**内部で定義される名前:**
- `_scan_vault_files`
- `path`


### メソッド: `index_vault(self: Any [✅], batch_size: int [✅]) -> None` [❌ 未使用]
**Docstring**: Index all markdown files in the vault.

Args:
    batch_size: Number of documents to process in each batch

**内部で定義される名前:**
- `batch`
- `content`
- `doc`
- `index_vault`
- `total_indexed`


### メソッド: `reindex_file(self: Any [✅], file_path: str [✅]) -> None` [❌ 未使用]
**Docstring**: Reindex a single file.

Args:
    file_path: Path to file to reindex

**内部で定義される名前:**
- `content`
- `doc`
- `path`
- `reindex_file`


### メソッド: `remove_file(self: Any [✅], file_path: str [✅]) -> None` [❌ 未使用]
**Docstring**: Remove a file from the index.

Args:
    file_path: Path to file to remove

**内部で定義される名前:**
- `doc_id`
- `path`
- `remove_file`



--------------------------------------------------

