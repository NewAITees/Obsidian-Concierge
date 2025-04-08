# tests/test_db フォルダのPython解析レポート

生成日時: 2025-04-08 20:40:21.957534

==================================================

# __init__.py の解析結果


--------------------------------------------------

# test_chroma.py の解析結果

## インポート一覧
- `obsidian_concierge.db.chroma.ChromaRepository` (✅ 使用あり)
- `obsidian_concierge.db.chroma.Document` (✅ 使用あり)
- `pytest` (✅ 使用あり)
- `typing.List` (✅ 使用あり)
- `uuid` (✅ 使用あり)

## 関数: `@pytest.fixture chroma_repo() -> None` [❌ 未使用]
**Docstring**: Fixture for ChromaRepository instance.

**内部で定義される名前:**
- `chroma_repo`
- `repo`


## 関数: `@pytest.fixture sample_documents() -> List[Document]` [❌ 未使用]
**Docstring**: Fixture for sample documents.

**内部で定義される名前:**
- `sample_documents`


## 関数: `test_add_documents(chroma_repo: ChromaRepository [✅], sample_documents: List[Document] [✅]) -> None` [❌ 未使用]
**Docstring**: Test adding documents to the repository.

**内部で定義される名前:**
- `stored_doc`
- `test_add_documents`


## 関数: `test_query_documents(chroma_repo: ChromaRepository [✅], sample_documents: List[Document] [✅]) -> None` [❌ 未使用]
**Docstring**: Test querying documents by similarity.

**内部で定義される名前:**
- `results`
- `test_query_documents`


## 関数: `test_update_document(chroma_repo: ChromaRepository [✅], sample_documents: List[Document] [✅]) -> None` [❌ 未使用]
**Docstring**: Test updating a document.

**内部で定義される名前:**
- `stored_doc`
- `test_update_document`
- `updated_doc`


## 関数: `test_delete_documents(chroma_repo: ChromaRepository [✅], sample_documents: List[Document] [✅]) -> None` [❌ 未使用]
**Docstring**: Test deleting documents.

**内部で定義される名前:**
- `test_delete_documents`


## 関数: `test_get_nonexistent_document(chroma_repo: ChromaRepository [✅]) -> None` [❌ 未使用]
**Docstring**: Test getting a nonexistent document.

**内部で定義される名前:**
- `test_get_nonexistent_document`


## 関数: `test_empty_operations(chroma_repo: ChromaRepository [✅]) -> None` [❌ 未使用]
**Docstring**: Test operations with empty inputs.

**内部で定義される名前:**
- `results`
- `test_empty_operations`



--------------------------------------------------

