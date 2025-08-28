#!/usr/bin/env python3
import sys
import subprocess

def test_installation():
    """Test if all required packages can be imported"""
    
    print("🧪 Testing APFS Installation...")
    print("=" * 50)
    
    # Test core Python modules
    try:
        import sys
        print(f"✅ Python version: {sys.version.split()[0]}")
    except Exception as e:
        print(f"❌ Python import failed: {e}")
        return False
    
    # Test required packages
    packages = [
        ("arxiv", "ArXiv API client"),
        ("pdfplumber", "PDF text extraction"),
        ("requests", "HTTP requests"),
        ("ollama", "Local LLM client"),
        ("rich", "Rich terminal output"),
        ("click", "CLI framework")
    ]
    
    failed_packages = []
    
    for package, description in packages:
        try:
            __import__(package)
            print(f"✅ {package:12} - {description}")
        except ImportError as e:
            print(f"❌ {package:12} - {description} (FAILED: {e})")
            failed_packages.append(package)
    
    if failed_packages:
        print(f"\n⚠️  Failed to import: {', '.join(failed_packages)}")
        print("   Run: pip install -r requirements.txt")
        return False
    
    # Test APFS modules
    print("\n🔧 Testing APFS modules...")
    apfs_modules = [
        ("apfs.arxiv_client", "ArXiv client"),
        ("apfs.pdf_handler", "PDF handler"),
        ("apfs.summarizer", "LLM summarizer"),
        ("apfs.output_formatter", "Output formatter")
    ]
    
    sys.path.insert(0, '.')
    
    for module, description in apfs_modules:
        try:
            __import__(module)
            print(f"✅ {module:20} - {description}")
        except ImportError as e:
            print(f"❌ {module:20} - {description} (FAILED: {e})")
            return False
    
    print("\n🎉 All tests passed! APFS is ready to use.")
    print("\n📖 Quick start:")
    print("   python -m apfs.main 'machine learning' --max-results 3")
    
    return True

if __name__ == "__main__":
    success = test_installation()
    sys.exit(0 if success else 1)