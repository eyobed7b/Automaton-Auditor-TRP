import pdfplumber
from typing import List, Dict, Optional
import os

class DocTools:
    @staticmethod
    def extract_text_from_pdf(pdf_path: str) -> str:
        """Extracts text from a PDF file."""
        text = ""
        if not os.path.exists(pdf_path):
            return "File not found."
        
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
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
