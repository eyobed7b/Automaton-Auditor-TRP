from pypdf import PdfReader
from typing import List, Dict, Optional
import os

class DocTools:
    @staticmethod
    def extract_text_from_pdf(pdf_path: str) -> str:
        """Extracts text from a PDF or text/markdown file."""
        text = ""
        if not os.path.exists(pdf_path):
            return "File not found."
        
        if pdf_path.lower().endswith(".pdf"):
            reader = PdfReader(pdf_path)
            for page in reader.pages:
                text += page.extract_text() or ""
        else:
            # Assume text/markdown
            with open(pdf_path, "r", encoding="utf-8") as f:
                text = f.read()
        return text

    @staticmethod
    def search_keywords(text: str, keywords: List[str]) -> Dict[str, bool]:
        """Searches for keywords in the text."""
        results = {}
        for keyword in keywords:
            results[keyword] = keyword.lower() in text.lower()
        return results

    @staticmethod
    def extract_file_paths(text: str) -> List[str]:
        """Simple heuristic to extract potential file paths from text."""
        import re
        # This regex looks for path-like strings (e.g., src/main.py, ./README.md)
        path_pattern = r'[a-zA-Z0-9_\-\./]+\.[a-zA-Z0-9]+'
        return list(set(re.findall(path_pattern, text)))
