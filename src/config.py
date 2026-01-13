from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    CHROMA_PERSIST_DIRECTORY: str = "chroma_data"
    CHROMA_COLLECTION_NAME: str = "document_embeddings"
    
    # Model settings (can be moved here too if needed)
    SIGLIP_MODEL_NAME: str = "google/siglip-base-patch16-224"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
