import arxiv
import time
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Paper:
    title: str
    authors: List[str]
    abstract: str
    pdf_url: str
    arxiv_id: str
    published: datetime
    categories: List[str]
    

class ArxivClient:
    def __init__(self, max_retries: int = 3, delay_between_retries: float = 1.0):
        self.max_retries = max_retries
        self.delay_between_retries = delay_between_retries
    
    def search_papers(
        self, 
        query: str, 
        max_results: int = 10,
        category: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None
    ) -> List[Paper]:
        search_query = query
        
        if category:
            search_query = f"cat:{category} AND {query}"
        
        for attempt in range(self.max_retries):
            try:
                search = arxiv.Search(
                    query=search_query,
                    max_results=max_results,
                    sort_by=arxiv.SortCriterion.Relevance,
                    sort_order=arxiv.SortOrder.Descending
                )
                
                papers = []
                for result in search.results():
                    if date_from or date_to:
                        paper_date = result.published.strftime("%Y-%m-%d")
                        if date_from and paper_date < date_from:
                            continue
                        if date_to and paper_date > date_to:
                            continue
                    
                    paper = Paper(
                        title=result.title,
                        authors=[str(author) for author in result.authors],
                        abstract=result.summary.replace('\n', ' ').strip(),
                        pdf_url=result.pdf_url,
                        arxiv_id=result.entry_id.split('/')[-1],
                        published=result.published,
                        categories=result.categories
                    )
                    papers.append(paper)
                
                return papers
                
            except Exception as e:
                if attempt < self.max_retries - 1:
                    print(f"Search attempt {attempt + 1} failed: {e}. Retrying in {self.delay_between_retries}s...")
                    time.sleep(self.delay_between_retries)
                else:
                    raise e
        
        return []
    
    def get_paper_by_id(self, arxiv_id: str) -> Optional[Paper]:
        for attempt in range(self.max_retries):
            try:
                search = arxiv.Search(id_list=[arxiv_id])
                result = next(search.results())
                
                return Paper(
                    title=result.title,
                    authors=[str(author) for author in result.authors],
                    abstract=result.summary.replace('\n', ' ').strip(),
                    pdf_url=result.pdf_url,
                    arxiv_id=result.entry_id.split('/')[-1],
                    published=result.published,
                    categories=result.categories
                )
                
            except Exception as e:
                if attempt < self.max_retries - 1:
                    print(f"Fetch attempt {attempt + 1} failed: {e}. Retrying in {self.delay_between_retries}s...")
                    time.sleep(self.delay_between_retries)
                else:
                    print(f"Failed to fetch paper {arxiv_id}: {e}")
                    return None
        
        return None