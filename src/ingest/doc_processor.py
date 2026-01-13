from pathlib import Path
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.document import ConversionResult
from docling.datamodel.pipeline_options import PdfPipelineOptions
from loguru import logger

class DoclingProcessor:
    def __init__(self):
        pipeline_options = PdfPipelineOptions()
        pipeline_options.generate_page_images = True
        pipeline_options.generate_picture_images = True
        
        self.converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )

    def process_file(self, file_path: Path) -> ConversionResult:
        """
        Process a single file using docling.
        """
        logger.debug(f"Processing file: {file_path}")
        result = self.converter.convert(file_path)
        logger.debug(f"Conversion finished for: {file_path.name}")
        return result
