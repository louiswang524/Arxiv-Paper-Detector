#!/usr/bin/env python3
"""
Test script for semantic search functionality
"""

import sys
sys.path.insert(0, '.')

def test_semantic_expansion():
    print("🧠 Testing Semantic Search Engine...")
    print("=" * 50)
    
    try:
        from apfs.semantic_search import SemanticSearchEngine
        
        engine = SemanticSearchEngine()
        print("✅ Semantic search engine initialized")
        
        # Test query expansions
        test_queries = [
            "machine learning",
            "AI", 
            "neural networks",
            "NLP",
            "quantum computing",
            "deep learning algorithms"
        ]
        
        for query in test_queries:
            print(f"\n🔍 Testing query: '{query}'")
            
            # Test different expansion modes
            for mode in ["conservative", "moderate", "aggressive"]:
                expansion = engine.expand_query(query, mode)
                print(f"  {mode.capitalize()} mode:")
                print(f"    Original terms: {expansion.original_terms}")
                print(f"    Expanded terms: {expansion.expanded_terms[:5]}{'...' if len(expansion.expanded_terms) > 5 else ''}")
                
                if expansion.synonyms:
                    print(f"    Synonyms found: {len(expansion.synonyms)} terms")
                
                semantic_query = engine.build_semantic_query(query, mode)
                print(f"    Query length: {len(semantic_query)} chars")
        
        return True
        
    except Exception as e:
        print(f"❌ Semantic search test failed: {e}")
        return False

def test_arxiv_integration():
    print("\n🔗 Testing ArXiv Integration...")
    print("=" * 40)
    
    try:
        from apfs.arxiv_client import ArxivClient
        
        # Test with semantic search disabled
        client_normal = ArxivClient(enable_semantic_search=False)
        print("✅ Normal ArXiv client created")
        
        # Test with semantic search enabled  
        client_semantic = ArxivClient(enable_semantic_search=True)
        print("✅ Semantic ArXiv client created")
        
        # Test explanation
        explanation = client_semantic.explain_semantic_search("machine learning", "moderate")
        if explanation:
            print("✅ Query explanation generated")
            print(f"   Length: {len(explanation)} chars")
        else:
            print("❌ No explanation generated")
            return False
            
        print("\n📝 Sample explanation:")
        print(explanation[:200] + "..." if len(explanation) > 200 else explanation)
        
        return True
        
    except Exception as e:
        print(f"❌ ArXiv integration test failed: {e}")
        return False

def test_cli_integration():
    print("\n⚡ Testing CLI Integration...")
    print("=" * 35)
    
    try:
        from apfs.main import main
        print("✅ Main CLI module imported")
        
        # Test if new parameters are recognized
        import inspect
        sig = inspect.signature(main)
        params = list(sig.parameters.keys())
        
        required_params = ['semantic_search', 'semantic_mode', 'explain_search']
        for param in required_params:
            if param in params:
                print(f"✅ Parameter '{param}' found in CLI")
            else:
                print(f"❌ Parameter '{param}' missing from CLI")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ CLI integration test failed: {e}")
        return False

def demo_semantic_search():
    print("\n🚀 Semantic Search Demo")
    print("=" * 30)
    
    try:
        from apfs.semantic_search import SemanticSearchEngine
        
        engine = SemanticSearchEngine()
        
        demo_query = "machine learning"
        print(f"Demo query: '{demo_query}'\n")
        
        explanation = engine.explain_expansion(demo_query, "moderate")
        print(explanation)
        
        return True
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Semantic Search Test Suite")
    print("=" * 60)
    
    tests = [
        test_semantic_expansion,
        test_arxiv_integration,
        test_cli_integration,
        demo_semantic_search
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"✅ Tests passed: {passed}/{len(tests)}")
    
    if passed == len(tests):
        print("🎉 All semantic search tests passed!")
        print("\n💡 Try these commands:")
        print("   python -m apfs.main 'AI' --semantic-search --explain-search")
        print("   python -m apfs.main 'neural networks' --semantic-search --semantic-mode aggressive")
        print("   python -m apfs.main 'machine learning' --semantic-search --max-results 5")
    else:
        print("⚠️  Some tests failed. Check the output above.")
    
    sys.exit(0 if passed == len(tests) else 1)