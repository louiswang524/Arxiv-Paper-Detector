#!/usr/bin/env python3

import click
import sys
from typing import Optional
from .arxiv_client import ArxivClient
from .pdf_handler import PDFHandler
from .summarizer import LLMSummarizer, SummaryType
from .output_formatter import OutputFormatter


@click.command()
@click.argument('query', required=True)
@click.option('--max-results', '-n', default=10, help='Maximum number of papers to retrieve (default: 10)')
@click.option('--category', '-c', default=None, help='ArXiv category filter (e.g., cs.AI, physics.gen-ph)')
@click.option('--date-from', default=None, help='Start date filter (YYYY-MM-DD format)')
@click.option('--date-to', default=None, help='End date filter (YYYY-MM-DD format)')
@click.option('--summarize/--no-summarize', default=True, help='Generate AI summaries (default: True)')
@click.option('--summary-type', type=click.Choice(['general', 'key_findings', 'methods', 'implications']), 
              default='general', help='Type of summary to generate')
@click.option('--full-text/--abstract-only', default=False, help='Use full PDF text for summarization (default: abstract only)')
@click.option('--model', '-m', default='llama3.2:3b', help='Ollama model to use for summarization')
@click.option('--output-format', type=click.Choice(['console', 'table', 'markdown', 'json']), 
              default='console', help='Output format')
@click.option('--output-file', '-o', default=None, help='Output file name (for markdown/json formats)')
@click.option('--download-dir', default=None, help='Directory to save downloaded PDFs')
@click.option('--cleanup/--no-cleanup', default=True, help='Clean up downloaded PDFs after processing')
def main(query: str, max_results: int, category: Optional[str], date_from: Optional[str], 
         date_to: Optional[str], summarize: bool, summary_type: str, full_text: bool, 
         model: str, output_format: str, output_file: Optional[str], 
         download_dir: Optional[str], cleanup: bool):
    """
    ArXiv Paper Finder and Summarizer (APFS)
    
    Search for academic papers on arXiv.org and generate AI summaries using local LLMs.
    
    QUERY: Search terms for finding papers (e.g., "quantum computing", "large language models")
    """
    
    formatter = OutputFormatter()
    
    try:
        formatter.display_info("🔍 Starting ArXiv Paper Search...")
        
        arxiv_client = ArxivClient()
        papers = arxiv_client.search_papers(
            query=query,
            max_results=max_results,
            category=category,
            date_from=date_from,
            date_to=date_to
        )
        
        if not papers:
            formatter.display_error("No papers found for the given search criteria.")
            sys.exit(1)
        
        formatter.display_success(f"Found {len(papers)} papers")
        
        summaries = {}
        
        if summarize:
            formatter.display_info("🤖 Initializing local LLM for summarization...")
            
            summarizer = LLMSummarizer(model_name=model)
            
            if not summarizer.check_model_availability():
                formatter.display_warning(f"Model {model} not found. Attempting to pull...")
                if not summarizer.pull_model_if_needed():
                    formatter.display_error(f"Failed to pull model {model}. Continuing without summarization.")
                    summarize = False
        
        if summarize:
            pdf_handler = PDFHandler(download_dir=download_dir)
            summary_enum = SummaryType(summary_type)
            
            formatter.display_info("📝 Generating summaries...")
            
            papers_data = []
            for paper in papers:
                content = pdf_handler.get_paper_content(
                    paper.pdf_url, 
                    paper.arxiv_id, 
                    paper.abstract, 
                    use_full_text=full_text
                )
                papers_data.append((paper.arxiv_id, paper.title, content))
            
            summaries = summarizer.summarize_multiple_papers(papers_data, summary_enum)
            
            if cleanup:
                pdf_handler.cleanup_downloads()
        
        if output_format == 'console':
            formatter.display_papers_console(papers, summaries)
        elif output_format == 'table':
            formatter.display_papers_table(papers)
            if summaries:
                formatter.display_info("Note: Summaries are not shown in table format. Use 'console' format to see summaries.")
        elif output_format == 'markdown':
            filename = output_file or f"arxiv_results_{query.replace(' ', '_')}.md"
            formatter.save_to_markdown(papers, summaries, filename)
        elif output_format == 'json':
            filename = output_file or f"arxiv_results_{query.replace(' ', '_')}.json"
            formatter.save_to_json(papers, summaries, filename)
        
        formatter.display_success("✨ Search and summarization completed!")
        
    except KeyboardInterrupt:
        formatter.display_warning("Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        formatter.display_error(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)


@click.group()
def cli():
    """ArXiv Paper Finder and Summarizer (APFS) - CLI Tools"""
    pass


@cli.command()
def list_models():
    """List available Ollama models"""
    formatter = OutputFormatter()
    try:
        summarizer = LLMSummarizer()
        models = summarizer.get_available_models()
        
        if models:
            formatter.display_info("Available Ollama models:")
            for model in models:
                formatter.console.print(f"  • {model}")
        else:
            formatter.display_warning("No Ollama models found. Install Ollama and pull some models first.")
            
    except Exception as e:
        formatter.display_error(f"Error listing models: {e}")


@cli.command()
@click.argument('model_name')
def pull_model(model_name: str):
    """Pull a specific Ollama model"""
    formatter = OutputFormatter()
    try:
        formatter.display_info(f"Pulling model: {model_name}")
        summarizer = LLMSummarizer(model_name=model_name)
        
        if summarizer.pull_model_if_needed():
            formatter.display_success(f"Model {model_name} is ready!")
        else:
            formatter.display_error(f"Failed to pull model {model_name}")
            
    except Exception as e:
        formatter.display_error(f"Error pulling model: {e}")


if __name__ == '__main__':
    main()