import chromadb
from typing import Dict, Any
import uuid
from datetime import datetime, timezone
from loguru import logger
import numpy as np

from src.config import settings

class VectorDB:
    def __init__(self):
        logger.info(f"Initializing ChromaDB at {settings.CHROMA_PERSIST_DIRECTORY}")
        
        self.client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIRECTORY)

        self.collection = self.client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"} # Cosine distance
        )
        logger.info(f"Collection '{settings.CHROMA_COLLECTION_NAME}' ready.")

    def add_image_vector(self, 
                         vector: np.ndarray, 
                         source_file: str, 
                         page_index: int, 
                         image_index: int,
                         additional_meta: Dict[str, Any] = None):
        """
        Add a single image vector to the store.
        """
        if additional_meta is None:
            additional_meta = {}
            
        # Current timestamp in ISO format
        indexed_at = datetime.now(timezone.utc).isoformat()
        
        metadata = {
            "type": "image",
            "indexedAt": indexed_at,
            "source_file": source_file,
            "page_index": page_index,
            "image_index": image_index,
            **additional_meta
        }
        
        # Convert numpy array to list for Chroma
        embedding = vector.tolist() if isinstance(vector, np.ndarray) else vector
        
        # Generate a unique ID
        doc_id = f"{source_file}_{page_index}_{image_index}_{uuid.uuid4().hex[:8]}"
        
        try:
            self.collection.add(
                embeddings=[embedding],
                metadatas=[metadata],
                ids=[doc_id]
            )
                
            logger.debug(f"Stored vector for {doc_id}")
        except Exception as e:
            logger.error(f"Failed to store vector for {doc_id}: {e}")
            raise e

    def count(self):
        return self.collection.count()
