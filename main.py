from src.ingest.loader import DocumentLoader
from src.ingest.doc_processor import DoclingProcessor
import os

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(root_dir, "data")
    
    loader = DocumentLoader(data_dir)
    processor = DoclingProcessor()
    
    files = loader.get_files()
    print(f"Found {len(files)} files to process.")
    
    for file_path in files:
        try:
            result = processor.process_file(file_path)
            doc = result.document
            
            print(f"\n--- Processed {file_path.name} ---")
            print(f"Title: {doc.name}")
            
            # Export to markdown to show structured text
            md_output = doc.export_to_markdown()
            print(f"Content Preview (Markdown):\n{md_output[:500]}...")
            
            # Separation of data examples
            if doc.tables:
                print(f"Found {len(doc.tables)} tables.")
            
            if doc.pictures:
                print(f"Found {len(doc.pictures)} pictures.")
                
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    main()