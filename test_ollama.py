#!/usr/bin/env python3
"""
Quick test script to diagnose Ollama connectivity issues
"""

import sys
sys.path.insert(0, '.')

def test_ollama_connection():
    print("🔍 Testing Ollama Connection...")
    print("=" * 40)
    
    try:
        import ollama
        print("✅ Ollama library imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import ollama: {e}")
        print("   Install with: pip install ollama")
        return False
    
    try:
        client = ollama.Client()
        print("✅ Ollama client created")
        
        # Test basic connection
        response = client.list()
        print(f"✅ Connected to Ollama server")
        print(f"   Response type: {type(response)}")
        print(f"   Response keys: {list(response.keys()) if isinstance(response, dict) else 'Not a dict'}")
        
        # Parse models safely
        if isinstance(response, dict):
            if 'models' in response:
                models = response['models']
                print(f"   Found {len(models)} models:")
                for i, model in enumerate(models[:3]):  # Show first 3
                    if isinstance(model, dict):
                        name = model.get('name', model.get('model', 'Unknown'))
                        print(f"     {i+1}. {name}")
                    else:
                        print(f"     {i+1}. {model}")
                
                if len(models) > 3:
                    print(f"     ... and {len(models) - 3} more")
            else:
                print("   No 'models' key in response")
        else:
            print("   Response is not a dictionary")
            
        return True
        
    except Exception as e:
        print(f"❌ Failed to connect to Ollama: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. Make sure Ollama is installed:")
        print("      curl -fsSL https://ollama.ai/install.sh | sh")
        print("   2. Start Ollama service:")
        print("      ollama serve")
        print("   3. Pull a model:")
        print("      ollama pull llama3.2:3b")
        return False

def test_apfs_integration():
    print("\n🧪 Testing APFS Integration...")
    print("=" * 40)
    
    try:
        from apfs.summarizer import LLMSummarizer
        print("✅ APFS summarizer imported successfully")
        
        summarizer = LLMSummarizer()
        models = summarizer.get_available_models()
        
        if models:
            print(f"✅ Found {len(models)} available models:")
            for model in models:
                print(f"   • {model}")
        else:
            print("❌ No models found or Ollama not running")
            
        return len(models) > 0
        
    except Exception as e:
        print(f"❌ APFS integration test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Ollama Diagnostic Test")
    print("=" * 50)
    
    success = test_ollama_connection()
    if success:
        test_apfs_integration()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ Ollama is working! You can now use APFS with AI summarization.")
    else:
        print("❌ Ollama setup needed. Follow the troubleshooting steps above.")