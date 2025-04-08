# tests/test_indexer フォルダのPython解析レポート

生成日時: 2025-04-08 20:40:21.965465

==================================================

# __init__.py の解析結果


--------------------------------------------------

# test_vault_indexer.py の解析結果

## インポート一覧
- `obsidian_concierge.db.chroma.ChromaRepository` (✅ 使用あり)
- `obsidian_concierge.db.chroma.Document` (❌ 未使用)
- `obsidian_concierge.indexer.vault_indexer.VaultIndexer` (✅ 使用あり)
- `os` (❌ 未使用)
- `pathlib.Path` (❌ 未使用)
- `pytest` (✅ 使用あり)
- `typing.Generator` (❌ 未使用)
- `unittest.mock.Mock` (✅ 使用あり)
- `unittest.mock.patch` (❌ 未使用)

## 関数: `@pytest.fixture mock_repo() -> None` [❌ 未使用]
**Docstring**: Fixture for mock ChromaRepository.

**内部で定義される名前:**
- `mock_repo`


## 関数: `@pytest.fixture temp_vault(tmp_path: Any [✅]) -> None` [❌ 未使用]
**Docstring**: Fixture for temporary vault directory with sample files.

**内部で定義される名前:**
- `file_path`
- `files`
- `temp_vault`
- `vault_dir`


## 関数: `test_vault_indexer_initialization(temp_vault: Any [✅], mock_repo: Any [✅]) -> None` [❌ 未使用]
**Docstring**: Test VaultIndexer initialization.

**内部で定義される名前:**
- `indexer`
- `test_vault_indexer_initialization`


## 関数: `test_vault_indexer_invalid_path(mock_repo: Any [✅]) -> None` [❌ 未使用]
**Docstring**: Test VaultIndexer initialization with invalid path.

**内部で定義される名前:**
- `test_vault_indexer_invalid_path`


## 関数: `test_read_markdown_file(temp_vault: Any [✅], mock_repo: Any [✅]) -> None` [❌ 未使用]
**Docstring**: Test reading markdown file content.

**内部で定義される名前:**
- `content`
- `indexer`
- `test_read_markdown_file`


## 関数: `test_generate_document_id(temp_vault: Any [✅], mock_repo: Any [✅]) -> None` [❌ 未使用]
**Docstring**: Test document ID generation.

**内部で定義される名前:**
- `doc_id`
- `file_path`
- `indexer`
- `other_path`
- `test_generate_document_id`


## 関数: `test_get_file_metadata(temp_vault: Any [✅], mock_repo: Any [✅]) -> None` [❌ 未使用]
**Docstring**: Test file metadata extraction.

**内部で定義される名前:**
- `file_path`
- `indexer`
- `metadata`
- `test_get_file_metadata`


## 関数: `test_scan_vault_files(temp_vault: Any [✅], mock_repo: Any [✅]) -> None` [❌ 未使用]
**Docstring**: Test scanning vault for markdown files.

**内部で定義される名前:**
- `file_paths`
- `files`
- `indexer`
- `test_scan_vault_files`


## 関数: `test_index_vault(temp_vault: Any [✅], mock_repo: Any [✅]) -> None` [❌ 未使用]
**Docstring**: Test indexing entire vault.

**内部で定義される名前:**
- `calls`
- `indexer`
- `test_index_vault`
- `total_docs`


## 関数: `test_reindex_file(temp_vault: Any [✅], mock_repo: Any [✅]) -> None` [❌ 未使用]
**Docstring**: Test reindexing a single file.

**内部で定義される名前:**
- `doc`
- `file_path`
- `indexer`
- `test_reindex_file`


## 関数: `test_remove_file(temp_vault: Any [✅], mock_repo: Any [✅]) -> None` [❌ 未使用]
**Docstring**: Test removing a file from index.

**内部で定義される名前:**
- `doc_id`
- `file_path`
- `indexer`
- `test_remove_file`


## 関数: `test_error_handling(temp_vault: Any [✅], mock_repo: Any [✅]) -> None` [❌ 未使用]
**Docstring**: Test error handling during indexing.

**内部で定義される名前:**
- `indexer`
- `test_error_handling`



--------------------------------------------------

