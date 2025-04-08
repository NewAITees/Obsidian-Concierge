# obsidian_concierge/db フォルダのPython解析レポート

生成日時: 2025-04-08 20:40:21.531117

==================================================

# chroma.py の解析結果

## インポート一覧
- `chromadb` (✅ 使用あり)
- `chromadb.config.Settings` (✅ 使用あり)
- `chromadb.utils.embedding_functions` (✅ 使用あり)
- `pydantic.BaseModel` (✅ 使用あり)
- `re` (❌ 未使用)
- `typing.Any` (✅ 使用あり)
- `typing.Dict` (✅ 使用あり)
- `typing.List` (✅ 使用あり)
- `typing.Optional` (✅ 使用あり)
- `utils.config.config` (✅ 使用あり)
- `utils.logging.logger` (✅ 使用あり)

## クラス: `Document` (BaseModel)
**Docstring**: Document model for ChromaDB storage.

## クラス: `ChromaRepository`
**Docstring**: Repository class for ChromaDB operations.

### メソッド: `__init__(self: Any [✅], collection_name: str [✅]) -> None` [❌ 未使用]
**Docstring**: Initialize ChromaDB repository.

Args:
    collection_name: Name of the ChromaDB collection to use

**内部で定義される名前:**
- `__init__`


### メソッド: `_convert_metadata_for_storage(self: Any [❌], metadata: Dict[str, Any] [✅]) -> Dict[str, Any]` [✅ 使用あり]
**Docstring**: Convert metadata to a format suitable for storage in ChromaDB.

**内部で定義される名前:**
- `_convert_metadata_for_storage`
- `converted_metadata`
- `tags`


### メソッド: `_convert_metadata_from_storage(self: Any [❌], metadata: Dict[str, Any] [✅]) -> Dict[str, Any]` [✅ 使用あり]
**Docstring**: Convert metadata from storage format to application format.

**内部で定義される名前:**
- `_convert_metadata_from_storage`
- `converted_metadata`
- `tag`
- `tag_fields`
- `tags`


### メソッド: `add_documents(self: Any [✅], documents: List[Document] [✅]) -> None` [❌ 未使用]
**Docstring**: Add multiple documents to the collection.

Args:
    documents: List of documents to add

**内部で定義される名前:**
- `add_documents`
- `contents`
- `ids`
- `metadatas`


### メソッド: `query(self: Any [✅], query_text: str [✅], n_results: int [✅], where: Optional[Dict[str, Any]] [✅]) -> List[Document]` [✅ 使用あり]
**Docstring**: Query documents by similarity and optional metadata filters.

**内部で定義される名前:**
- `conditions`
- `doc_content`
- `doc_id`
- `doc_metadata`
- `documents`
- `query`
- `results`
- `tags`
- `where`


### メソッド: `update_document(self: Any [✅], document: Document [✅]) -> None` [❌ 未使用]
**Docstring**: Update an existing document.

Args:
    document: Document to update

**内部で定義される名前:**
- `metadata`
- `update_document`


### メソッド: `delete_documents(self: Any [✅], ids: List[str] [✅]) -> None` [❌ 未使用]
**Docstring**: Delete documents by their IDs.

Args:
    ids: List of document IDs to delete

**内部で定義される名前:**
- `delete_documents`


### メソッド: `get_document(self: Any [✅], id: str [✅]) -> Optional[Document]` [❌ 未使用]
**Docstring**: Get a document by its ID.

Args:
    id: Document ID to retrieve
    
Returns:
    Document if found, None otherwise

**内部で定義される名前:**
- `get_document`
- `metadata`
- `result`



--------------------------------------------------

