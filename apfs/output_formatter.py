import json
from typing import List, Dict, Optional, Any
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown
from .arxiv_client import Paper


class OutputFormatter:
    def __init__(self):
        self.console = Console()
    
    def display_papers_console(self, papers: List[Paper], summaries: Dict[str, Optional[str]] = None):
        self.console.print("\n[bold blue]📄 ArXiv Paper Search Results[/bold blue]\n")
        
        for i, paper in enumerate(papers, 1):
            title_text = Text(f"{i}. {paper.title}", style="bold cyan")
            self.console.print(title_text)
            
            authors_text = Text(f"Authors: {', '.join(paper.authors[:3])}", style="dim")
            if len(paper.authors) > 3:
                authors_text.append(f" and {len(paper.authors) - 3} more", style="dim italic")
            self.console.print(authors_text)
            
            self.console.print(f"[dim]ArXiv ID:[/dim] {paper.arxiv_id}")
            self.console.print(f"[dim]Published:[/dim] {paper.published.strftime('%Y-%m-%d')}")
            self.console.print(f"[dim]Categories:[/dim] {', '.join(paper.categories)}")
            self.console.print(f"[dim]PDF URL:[/dim] {paper.pdf_url}")
            
            self.console.print("\n[bold]Abstract:[/bold]")
            abstract_panel = Panel(paper.abstract, border_style="dim")
            self.console.print(abstract_panel)
            
            if summaries and paper.arxiv_id in summaries and summaries[paper.arxiv_id]:
                self.console.print("\n[bold green]AI Summary:[/bold green]")
                summary_panel = Panel(summaries[paper.arxiv_id], border_style="green")
                self.console.print(summary_panel)
            
            if i < len(papers):
                self.console.print("\n" + "─" * 80 + "\n")
    
    def display_papers_table(self, papers: List[Paper]):
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Title", style="cyan", width=40)
        table.add_column("Authors", style="green", width=25)
        table.add_column("Published", style="yellow", width=12)
        table.add_column("ArXiv ID", style="dim", width=15)
        
        for paper in papers:
            authors_str = ", ".join(paper.authors[:2])
            if len(paper.authors) > 2:
                authors_str += f" +{len(paper.authors) - 2}"
            
            table.add_row(
                paper.title[:37] + "..." if len(paper.title) > 40 else paper.title,
                authors_str,
                paper.published.strftime('%Y-%m-%d'),
                paper.arxiv_id
            )
        
        self.console.print(table)
    
    def save_to_markdown(self, papers: List[Paper], summaries: Dict[str, Optional[str]] = None, filename: str = "arxiv_results.md"):
        content = ["# ArXiv Paper Search Results\n"]
        
        for i, paper in enumerate(papers, 1):
            content.append(f"## {i}. {paper.title}\n")
            content.append(f"**Authors:** {', '.join(paper.authors)}\n")
            content.append(f"**ArXiv ID:** {paper.arxiv_id}\n")
            content.append(f"**Published:** {paper.published.strftime('%Y-%m-%d')}\n")
            content.append(f"**Categories:** {', '.join(paper.categories)}\n")
            content.append(f"**PDF URL:** {paper.pdf_url}\n")
            
            content.append("### Abstract\n")
            content.append(f"{paper.abstract}\n")
            
            if summaries and paper.arxiv_id in summaries and summaries[paper.arxiv_id]:
                content.append("### AI Summary\n")
                content.append(f"{summaries[paper.arxiv_id]}\n")
            
            content.append("---\n")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))
        
        self.console.print(f"[green]✅ Results saved to {filename}[/green]")
    
    def save_to_json(self, papers: List[Paper], summaries: Dict[str, Optional[str]] = None, filename: str = "arxiv_results.json"):
        data = {
            "search_results": [],
            "timestamp": str(papers[0].published) if papers else "",
            "total_papers": len(papers)
        }
        
        for paper in papers:
            paper_data = {
                "title": paper.title,
                "authors": paper.authors,
                "abstract": paper.abstract,
                "pdf_url": paper.pdf_url,
                "arxiv_id": paper.arxiv_id,
                "published": paper.published.isoformat(),
                "categories": paper.categories
            }
            
            if summaries and paper.arxiv_id in summaries:
                paper_data["ai_summary"] = summaries[paper.arxiv_id]
            
            data["search_results"].append(paper_data)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        self.console.print(f"[green]✅ Results saved to {filename}[/green]")
    
    def display_error(self, message: str):
        error_panel = Panel(f"[red]Error: {message}[/red]", border_style="red")
        self.console.print(error_panel)
    
    def display_warning(self, message: str):
        warning_panel = Panel(f"[yellow]Warning: {message}[/yellow]", border_style="yellow")
        self.console.print(warning_panel)
    
    def display_success(self, message: str):
        success_panel = Panel(f"[green]✅ {message}[/green]", border_style="green")
        self.console.print(success_panel)
    
    def display_info(self, message: str):
        info_panel = Panel(f"[blue]ℹ️  {message}[/blue]", border_style="blue")
        self.console.print(info_panel)