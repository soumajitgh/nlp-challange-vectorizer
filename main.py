from src.ingest.loader import DocumentLoader
from src.ingest.doc_processor import DoclingProcessor
from src.ingest.vectorizer import ImageVectorizer
from src.storage.chroma import VectorDB
from src.config import settings
import os
import sys
from loguru import logger

def main():
    # Configure logger
    logger.remove()
    logger.add(sys.stderr, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")

    root_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(root_dir, "data")
    
    loader = DocumentLoader(data_dir)
    processor = DoclingProcessor()
    vectorizer = ImageVectorizer(model_name=settings.SIGLIP_MODEL_NAME)
    
    # Initialize VectorDB
    try:
        db = VectorDB()
    except Exception as e:
        logger.critical(f"Failed to initialize VectorDB: {e}")
        return
    
    try:
        files = loader.get_files()
        logger.info(f"Found {len(files)} files to process.")
        
        for file_path in files:
            try:
                logger.info(f"Processing {file_path.name}")
                result = processor.process_file(file_path)
                doc = result.document
                
                logger.info(f"Title: {doc.name}")
                
                if doc.pictures:
                    logger.info(f"Found {len(doc.pictures)} pictures.")
                    for i, picture in enumerate(doc.pictures):
                        image = picture.get_image(doc)
                        if image:
                            logger.info(f"Vectorizing picture {i+1}...")
                            vector = vectorizer.vectorize(image)
                            logger.success(f"Generated vector with shape: {vector.shape}")
                            
                            # Store in ChromaDB
                            # Attempt to get page number if available (docling structure dependent)
                            # picture.page_no is common in docling models, verify if needed. 
                            # If not available, default to -1 or 0
                            page_no = getattr(picture, 'page_no', -1)
                            
                            db.add_image_vector(
                                vector=vector,
                                source_file=file_path.name,
                                page_index=page_no,
                                image_index=i,
                                additional_meta={
                                    "doc_title": doc.name or "Unknown"
                                }
                            )
                        else:
                            logger.warning(f"Picture {i+1} has no image data.")
                else:
                    logger.info("No pictures found in this document.")
                    
            except Exception as e:
                logger.exception(f"Error processing {file_path}: {e}")
                
    except Exception as e:
        logger.exception("An unexpected error occurred during execution.")

if __name__ == "__main__":
    main()
