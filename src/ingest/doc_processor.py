from pathlib import Path
from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import InputFormat
from docling.datamodel.document import ConversionResult

class DoclingProcessor:
    def __init__(self):
        self.converter = DocumentConverter()

    def process_file(self, file_path: Path) -> ConversionResult:
        """
        Process a single file using docling.
        """
        print(f"Processing file: {file_path}")
        result = self.converter.convert(file_path)
        print(f"conversion result: {result}")
        return result
