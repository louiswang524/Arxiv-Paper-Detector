#!/usr/bin/env python3
"""
Example usage of semantic search features in APFS
"""

import sys
sys.path.insert(0, '.')

from apfs.semantic_search import SemanticSearchEngine
from apfs.arxiv_client import ArxivClient

def demo_query_expansion():
    """Demonstrate how different queries get expanded"""
    print("🧠 Semantic Query Expansion Demo")
    print("=" * 50)
    
    engine = SemanticSearchEngine()
    
    # Demo queries showcasing different expansion capabilities
    demo_queries = [
        ("AI", "Shows abbreviation expansion"),
        ("machine learning", "Common ML synonyms"),
        ("NLP", "Natural language processing terms"),
        ("neural networks", "Deep learning related terms"),
        ("quantum computing", "Physics and computing crossover"),
        ("computer vision", "Image processing and AI"),
        ("reinforcement learning", "RL and decision making terms")
    ]
    
    for query, description in demo_queries:
        print(f"\n🔍 Query: '{query}' ({description})")
        print("-" * 60)
        
        for mode in ["conservative", "moderate", "aggressive"]:
            expansion = engine.expand_query(query, mode)
            print(f"\n{mode.upper()} MODE:")
            print(f"  Original terms: {expansion.original_terms}")
            print(f"  Expanded terms: {len(expansion.expanded_terms)} total")
            print(f"  Sample expansions: {expansion.expanded_terms[:5]}")
            
            if expansion.synonyms:
                for term, syns in list(expansion.synonyms.items())[:2]:
                    print(f"  • {term} → {', '.join(syns[:3])}")

def demo_search_comparison():
    """Compare normal vs semantic search results"""
    print("\n🔄 Search Comparison Demo")
    print("=" * 40)
    
    # Note: This would require actual ArXiv API calls
    print("This demo shows how to compare normal vs semantic search:")
    print()
    print("# Normal search:")
    print('python -m apfs.main "AI" --max-results 5 --no-semantic-search')
    print()
    print("# Semantic search:")
    print('python -m apfs.main "AI" --max-results 5 --semantic-search --semantic-mode moderate')
    print()
    print("# With explanation:")
    print('python -m apfs.main "AI" --semantic-search --explain-search')

def demo_domain_specific_expansion():
    """Show domain-specific term expansions"""
    print("\n🎯 Domain-Specific Expansion Demo")
    print("=" * 45)
    
    engine = SemanticSearchEngine()
    
    domain_queries = [
        "deep learning",
        "machine learning", 
        "quantum computing",
        "computer vision",
        "natural language processing"
    ]
    
    for query in domain_queries:
        expansion = engine.expand_query(query, "aggressive")
        print(f"\n📚 {query.upper()}:")
        
        if expansion.related_terms:
            for term, related in expansion.related_terms.items():
                print(f"  🔗 {term}:")
                print(f"     Related: {', '.join(related[:4])}...")
        else:
            print("  No domain-specific expansions found")

def show_practical_examples():
    """Show practical command-line examples"""
    print("\n💡 Practical Examples")
    print("=" * 30)
    
    examples = [
        {
            "scenario": "Broad AI research overview",
            "command": 'python -m apfs.main "artificial intelligence" --semantic-search --max-results 10',
            "explanation": "Finds papers using AI, ML, neural networks, etc."
        },
        {
            "scenario": "Specific technique with variations",
            "command": 'python -m apfs.main "transformer" --semantic-search --semantic-mode conservative',
            "explanation": "Includes attention mechanism, BERT, GPT variants"
        },
        {
            "scenario": "Cross-domain research",
            "command": 'python -m apfs.main "quantum ML" --semantic-search --semantic-mode aggressive',
            "explanation": "Finds quantum machine learning, quantum computing + AI papers"
        },
        {
            "scenario": "Understanding query expansion",
            "command": 'python -m apfs.main "reinforcement learning" --explain-search --semantic-search',
            "explanation": "Shows how RL expands to reward learning, policy optimization, etc."
        },
        {
            "scenario": "Focused but comprehensive search", 
            "command": 'python -m apfs.main "computer vision" --semantic-search --category cs.CV --output-format markdown',
            "explanation": "CV + image processing + pattern recognition papers, exported to file"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. {example['scenario']}:")
        print(f"   Command: {example['command']}")
        print(f"   Result: {example['explanation']}")

def semantic_search_tips():
    """Provide tips for effective semantic search"""
    print("\n💡 Semantic Search Tips")
    print("=" * 35)
    
    tips = [
        "Use abbreviations: 'AI', 'ML', 'NLP' work great and expand automatically",
        "Conservative mode: Best for well-defined, narrow topics",
        "Moderate mode: Good balance for most academic searches", 
        "Aggressive mode: Use when exploring broad or interdisciplinary topics",
        "Use --explain-search to understand how your query expands",
        "Combine with category filters for more precise results",
        "Try different expansion modes if results are too broad/narrow",
        "Semantic ranking puts most relevant papers first"
    ]
    
    for i, tip in enumerate(tips, 1):
        print(f"{i}. {tip}")

if __name__ == "__main__":
    print("🚀 APFS Semantic Search Examples")
    print("=" * 60)
    
    demo_query_expansion()
    demo_search_comparison()
    demo_domain_specific_expansion()
    show_practical_examples()
    semantic_search_tips()
    
    print("\n" + "=" * 60)
    print("🎉 Ready to use semantic search!")
    print("Try: python -m apfs.main 'your query' --semantic-search --explain-search")