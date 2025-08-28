import os
import requests
import pdfplumber
import tempfile
from typing import Optional
from pathlib import Path


class PDFHandler:
    def __init__(self, download_dir: Optional[str] = None, max_retries: int = 3):
        self.download_dir = Path(download_dir) if download_dir else Path(tempfile.gettempdir()) / "apfs_papers"
        self.download_dir.mkdir(exist_ok=True)
        self.max_retries = max_retries
    
    def download_pdf(self, pdf_url: str, arxiv_id: str) -> Optional[Path]:
        filename = f"{arxiv_id.replace('/', '_')}.pdf"
        file_path = self.download_dir / filename
        
        if file_path.exists():
            print(f"PDF already exists: {file_path}")
            return file_path
        
        for attempt in range(self.max_retries):
            try:
                print(f"Downloading PDF: {arxiv_id}")
                response = requests.get(pdf_url, stream=True, timeout=30)
                response.raise_for_status()
                
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                return file_path
                
            except Exception as e:
                if attempt < self.max_retries - 1:
                    print(f"Download attempt {attempt + 1} failed: {e}. Retrying...")
                else:
                    print(f"Failed to download PDF {arxiv_id}: {e}")
                    return None
        
        return None
    
    def extract_text_from_pdf(self, pdf_path: Path) -> Optional[str]:
        try:
            with pdfplumber.open(pdf_path) as pdf:
                text_content = []
                
                for page_num, page in enumerate(pdf.pages):
                    try:
                        text = page.extract_text()
                        if text:
                            text_content.append(text)
                    except Exception as e:
                        print(f"Warning: Failed to extract text from page {page_num + 1}: {e}")
                        continue
                
                if text_content:
                    full_text = '\n'.join(text_content)
                    cleaned_text = self._clean_text(full_text)
                    return cleaned_text
                else:
                    print(f"No text could be extracted from {pdf_path}")
                    return None
                    
        except Exception as e:
            print(f"Failed to extract text from PDF {pdf_path}: {e}")
            return None
    
    def _clean_text(self, text: str) -> str:
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if line and len(line) > 1:
                cleaned_lines.append(line)
        
        cleaned_text = ' '.join(cleaned_lines)
        
        while '  ' in cleaned_text:
            cleaned_text = cleaned_text.replace('  ', ' ')
        
        return cleaned_text
    
    def get_paper_content(self, pdf_url: str, arxiv_id: str, abstract: str, use_full_text: bool = False) -> str:
        if not use_full_text:
            return abstract
        
        pdf_path = self.download_pdf(pdf_url, arxiv_id)
        if pdf_path:
            full_text = self.extract_text_from_pdf(pdf_path)
            if full_text:
                return full_text
            else:
                print(f"Falling back to abstract for paper {arxiv_id}")
                return abstract
        else:
            print(f"Falling back to abstract for paper {arxiv_id}")
            return abstract
    
    def cleanup_downloads(self):
        if self.download_dir.exists():
            for pdf_file in self.download_dir.glob("*.pdf"):
                try:
                    pdf_file.unlink()
                except Exception as e:
                    print(f"Warning: Could not delete {pdf_file}: {e}")
            
            try:
                self.download_dir.rmdir()
            except Exception:
                pass