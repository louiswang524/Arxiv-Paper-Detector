#!/usr/bin/env python3
"""
Example usage of ArXiv Paper Finder and Summarizer (APFS)
This script demonstrates how to use APFS programmatically
"""

import sys
import os
sys.path.insert(0, '.')

from apfs.arxiv_client import ArxivClient
from apfs.pdf_handler import PDFHandler  
from apfs.summarizer import LLMSummarizer, SummaryType
from apfs.output_formatter import OutputFormatter

def example_search_only():
    """Example: Search for papers without summarization"""
    print("🔍 Example 1: Basic paper search")
    print("=" * 40)
    
    client = ArxivClient()
    formatter = OutputFormatter()
    
    try:
        papers = client.search_papers(
            query="machine learning", 
            max_results=3,
            category="cs.AI"
        )
        
        if papers:
            formatter.display_papers_console(papers)
            print(f"\n✅ Found {len(papers)} papers")
        else:
            print("❌ No papers found")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def example_with_summarization():
    """Example: Search and summarize papers (requires Ollama)"""
    print("\n🤖 Example 2: Search with AI summarization")
    print("=" * 45)
    
    client = ArxivClient()
    formatter = OutputFormatter()
    
    try:
        # Check if Ollama is available
        summarizer = LLMSummarizer(model_name="llama3.2:3b")
        
        if not summarizer.check_model_availability():
            print("⚠️  Ollama model not available. Install Ollama and run:")
            print("   ollama pull llama3.2:3b")
            return
            
        papers = client.search_papers(
            query="natural language processing", 
            max_results=2
        )
        
        if papers:
            pdf_handler = PDFHandler()
            summaries = {}
            
            print("📝 Generating summaries...")
            for paper in papers:
                # Use abstract only for this example (faster)
                summary = summarizer.summarize_paper(
                    paper_content=paper.abstract,
                    title=paper.title,
                    summary_type=SummaryType.GENERAL
                )
                summaries[paper.arxiv_id] = summary
                
            formatter.display_papers_console(papers, summaries)
            print(f"\n✅ Generated summaries for {len(papers)} papers")
        else:
            print("❌ No papers found")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def example_export_results():
    """Example: Export results to different formats"""
    print("\n📄 Example 3: Export results")
    print("=" * 35)
    
    client = ArxivClient()
    formatter = OutputFormatter()
    
    try:
        papers = client.search_papers(
            query="computer vision", 
            max_results=2
        )
        
        if papers:
            # Export to Markdown
            formatter.save_to_markdown(papers, filename="cv_papers_example.md")
            
            # Export to JSON  
            formatter.save_to_json(papers, filename="cv_papers_example.json")
            
            print("✅ Results exported to:")
            print("   - cv_papers_example.md")
            print("   - cv_papers_example.json")
        else:
            print("❌ No papers found")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Run all examples"""
    print("🚀 APFS Usage Examples")
    print("=" * 50)
    
    # Example 1: Basic search
    example_search_only()
    
    # Example 2: With summarization (requires Ollama)
    example_with_summarization() 
    
    # Example 3: Export results
    example_export_results()
    
    print("\n🎯 For CLI usage, try:")
    print("   python -m apfs.main 'quantum computing' --max-results 5")
    print("   python -m apfs.main 'deep learning' --output-format markdown")

if __name__ == "__main__":
    main()