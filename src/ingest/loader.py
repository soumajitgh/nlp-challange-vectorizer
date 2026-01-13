from pathlib import Path
from typing import List

class DocumentLoader:
    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)

    def get_files(self, extensions: List[str] = None) -> List[Path]:
        """
        Get list of files from the data directory matching extensions.
        If extensions is None, looks for common document types.
        """
        if not self.data_dir.exists():
            raise FileNotFoundError(f"Directory {self.data_dir} not found")

        if extensions is None:
            extensions = ['.pdf', '.docx', '.md', '.html']

        files = []
        for ext in extensions:
            files.extend(list(self.data_dir.rglob(f"*{ext}")))
        
        return files
