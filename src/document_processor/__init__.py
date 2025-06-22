from typing import List, Union
from pypdf import PdfReader
import csv

class DocumentProcessor:
    @staticmethod
    def process_pdf(file_path: str) -> List[str]:
        """Extract text from PDF file"""
        reader = PdfReader(file_path)
        return [page.extract_text() for page in reader.pages]

    @staticmethod
    def process_txt(file_path: str) -> List[str]:
        """Read text file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return [f.read()]

    @staticmethod
    def process_csv(file_path: str) -> List[str]:
        """Extract text from CSV file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            return [' '.join(row) for row in reader]

    @classmethod
    def process_document(cls, file_path: str) -> List[str]:
        """Process document based on file extension"""
        if file_path.endswith('.pdf'):
            return cls.process_pdf(file_path)
        elif file_path.endswith('.txt'):
            return cls.process_txt(file_path)
        elif file_path.endswith('.csv'):
            return cls.process_csv(file_path)
        else:
            raise ValueError("Unsupported file format")