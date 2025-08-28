import arxiv
import time
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
from .semantic_search import SemanticSearchEngine


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
    def __init__(self, max_retries: int = 3, delay_between_retries: float = 1.0, enable_semantic_search: bool = False):
        self.max_retries = max_retries
        self.delay_between_retries = delay_between_retries
        self.semantic_engine = SemanticSearchEngine() if enable_semantic_search else None
    
    def search_papers(
        self, 
        query: str, 
        max_results: int = 10,
        category: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        semantic_mode: Optional[str] = None
    ) -> List[Paper]:
        # Apply semantic expansion if enabled
        if self.semantic_engine and semantic_mode:
            expanded_query = self.semantic_engine.build_semantic_query(query, semantic_mode)
            search_query = expanded_query
            print(f"🔍 Semantic search enabled ({semantic_mode} mode)")
            print(f"📝 Expanded query: {search_query[:100]}...")
        else:
            search_query = query
        
        if category:
            if self.semantic_engine and semantic_mode:
                search_query = f"cat:{category} AND ({search_query})"
            else:
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
                
                # Apply semantic ranking if enabled
                if self.semantic_engine and semantic_mode and papers:
                    papers = self.semantic_engine.rank_results_by_relevance(papers, query)
                    print(f"🎯 Results ranked by semantic relevance")
                
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
    
    def explain_semantic_search(self, query: str, mode: str = "moderate") -> Optional[str]:
        """Explain how semantic search will expand the query"""
        if not self.semantic_engine:
            return None
        
        return self.semantic_engine.explain_expansion(query, mode)