"""
Vault indexer implementation.

This module provides functionality for indexing Obsidian vault contents
into ChromaDB for efficient searching and retrieval.
"""

import os
import hashlib
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Generator

from ..db.chroma import ChromaRepository, Document
from ..utils.config import config
from ..utils.fs import list_files, is_text_file
from ..utils.logging import logger


class VaultIndexer:
    """Class for indexing Obsidian vault contents."""
    
    def __init__(self, vault_path: str, repo: ChromaRepository):
        """
        Initialize vault indexer.
        
        Args:
            vault_path: Path to Obsidian vault
            repo: ChromaDB repository instance
        """
        self.vault_path = Path(vault_path)
        if not self.vault_path.exists():
            raise ValueError(f"Vault path does not exist: {vault_path}")
            
        self.repo = repo
        logger.info(f"Initialized vault indexer for: {vault_path}")
    
    def _read_markdown_file(self, file_path: Path) -> str:
        """
        Read and preprocess markdown file content.
        
        Args:
            file_path: Path to markdown file
            
        Returns:
            Preprocessed file content
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # TODO: Add more preprocessing steps as needed
            # - Remove YAML frontmatter
            # - Handle special Obsidian syntax
            # - Extract and process tags
            return content
            
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            return ""
    
    def _generate_document_id(self, file_path: Path) -> str:
        """
        Generate unique document ID for a file.
        
        Args:
            file_path: Path to file
            
        Returns:
            Unique document ID
        """
        # Use relative path from vault root for consistent IDs
        rel_path = file_path.relative_to(self.vault_path)
        return hashlib.sha256(str(rel_path).encode()).hexdigest()
    
    def _get_file_metadata(self, file_path: Path) -> Dict[str, Any]:
        """
        Extract metadata from file.
        
        Args:
            file_path: Path to file
            
        Returns:
            File metadata
        """
        stat = file_path.stat()
        rel_path = str(file_path.relative_to(self.vault_path))
        
        return {
            "path": rel_path,
            "filename": file_path.name,
            "extension": file_path.suffix.lower(),
            "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "size_bytes": stat.st_size
        }
    
    def _scan_vault_files(self) -> Generator[Path, None, None]:
        """
        Scan vault directory for markdown files.
        
        Yields:
            Paths to markdown files
        """
        for file_path in list_files(self.vault_path, recursive=True):
            path = Path(file_path)
            # Only process markdown files
            if path.suffix.lower() == ".md" and is_text_file(path):
                yield path
    
    def index_vault(self, batch_size: int = 100) -> None:
        """
        Index all markdown files in the vault.
        
        Args:
            batch_size: Number of documents to process in each batch
        """
        batch: List[Document] = []
        total_indexed = 0
        
        try:
            for file_path in self._scan_vault_files():
                # Create document
                content = self._read_markdown_file(file_path)
                if not content:
                    continue
                    
                doc = Document(
                    id=self._generate_document_id(file_path),
                    content=content,
                    metadata=self._get_file_metadata(file_path)
                )
                batch.append(doc)
                
                # Process batch
                if len(batch) >= batch_size:
                    self.repo.add_documents(batch)
                    total_indexed += len(batch)
                    batch = []
                    
            # Process remaining documents
            if batch:
                self.repo.add_documents(batch)
                total_indexed += len(batch)
                
            logger.info(f"Successfully indexed {total_indexed} documents")
            
        except Exception as e:
            logger.error(f"Error during indexing: {e}")
            # Add any remaining documents
            if batch:
                self.repo.add_documents(batch)
                total_indexed += len(batch)
            raise
    
    def reindex_file(self, file_path: str) -> None:
        """
        Reindex a single file.
        
        Args:
            file_path: Path to file to reindex
        """
        path = Path(file_path)
        if not path.exists() or path.suffix.lower() != ".md":
            return
            
        try:
            content = self._read_markdown_file(path)
            if not content:
                return
                
            doc = Document(
                id=self._generate_document_id(path),
                content=content,
                metadata=self._get_file_metadata(path)
            )
            
            self.repo.update_document(doc)
            logger.info(f"Reindexed file: {file_path}")
            
        except Exception as e:
            logger.error(f"Error reindexing file {file_path}: {e}")
            raise
    
    def remove_file(self, file_path: str) -> None:
        """
        Remove a file from the index.
        
        Args:
            file_path: Path to file to remove
        """
        path = Path(file_path)
        doc_id = self._generate_document_id(path)
        
        self.repo.delete_documents([doc_id])
        logger.info(f"Removed file from index: {file_path}") 