# ArXiv Paper Finder and Summarizer (APFS)

A lightweight, privacy-focused tool for discovering and summarizing academic papers from arXiv.org using local Large Language Models (LLMs). Built with cost-effectiveness and offline capability in mind.

## 🚀 Features

- **🔍 Smart Paper Discovery**: Search arXiv by topic, category, date range, and more
- **🤖 Local AI Summarization**: Generate summaries using locally hosted LLMs via Ollama
- **📄 Multiple Output Formats**: Console display, tables, Markdown, and JSON export
- **🔒 Privacy-First**: All processing happens on your device - no cloud APIs
- **💰 Zero Ongoing Costs**: Free to run after initial setup
- **⚡ Efficient**: Handles both abstract-only and full-text summarization
- **🛠️ Customizable**: Support for different summary types and LLM models

## 📋 Requirements

### System Requirements
- **RAM**: Minimum 8 GB (16 GB recommended for larger models)
- **Storage**: ~2-5 GB for LLM models
- **OS**: Windows, macOS, or Linux
- **Python**: 3.10 or higher

### Dependencies
- Ollama (for local LLM inference)
- Python packages (automatically installed)

## ⚡ Quick Start

### 1. Install Ollama

First, install Ollama on your system:

**macOS/Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Windows:**
Download and install from https://ollama.ai/

### 2. Pull a Language Model

```bash
ollama pull llama3.2:3b  # Recommended for most users (lower RAM usage)
# OR
ollama pull llama3.1:8b  # Better quality, higher RAM usage
```

### 3. Install APFS

```bash
git clone <repository-url>
cd arxiv-paper-finder
pip install -r requirements.txt
```

### 4. Run Your First Search

```bash
python -m apfs.main "quantum computing" --max-results 5
```

## 📖 Usage

### Basic Search

```bash
# Simple search
python -m apfs.main "large language models"

# Search with category filter
python -m apfs.main "neural networks" --category cs.AI

# Search with date range
python -m apfs.main "transformer architecture" --date-from 2023-01-01 --date-to 2024-12-31
```

### Advanced Options

```bash
# Use different summary types
python -m apfs.main "machine learning" --summary-type key_findings

# Use full PDF text (slower but more comprehensive)
python -m apfs.main "deep learning" --full-text

# Export results to Markdown
python -m apfs.main "computer vision" --output-format markdown --output-file cv_papers.md

# Use a different model
python -m apfs.main "NLP" --model llama3.1:8b
```

### Complete Example

```bash
python -m apfs.main "attention mechanisms" \
  --max-results 10 \
  --category cs.AI \
  --date-from 2023-01-01 \
  --summary-type general \
  --output-format json \
  --output-file attention_papers.json \
  --full-text
```

## 🛠️ Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `query` | Search terms (required) | - |
| `--max-results, -n` | Maximum papers to retrieve | 10 |
| `--category, -c` | ArXiv category filter | None |
| `--date-from` | Start date (YYYY-MM-DD) | None |
| `--date-to` | End date (YYYY-MM-DD) | None |
| `--summarize/--no-summarize` | Generate AI summaries | True |
| `--summary-type` | Summary type | general |
| `--full-text/--abstract-only` | Use full PDF text | False |
| `--model, -m` | Ollama model name | llama3.2:3b |
| `--output-format` | Output format | console |
| `--output-file, -o` | Output file name | Auto-generated |
| `--download-dir` | PDF download directory | Temp directory |
| `--cleanup/--no-cleanup` | Clean up PDFs after processing | True |

### Summary Types

- **general**: Complete overview with main findings and implications
- **key_findings**: Focus on results and discoveries  
- **methods**: Emphasis on methodology and approach
- **implications**: Analysis of broader impact and significance

### Output Formats

- **console**: Rich formatted display in terminal
- **table**: Compact table view
- **markdown**: Export to Markdown file
- **json**: Machine-readable JSON format

## 🎯 Common ArXiv Categories

| Category | Description |
|----------|-------------|
| `cs.AI` | Artificial Intelligence |
| `cs.LG` | Machine Learning |
| `cs.CL` | Computation and Language |
| `cs.CV` | Computer Vision |
| `physics.gen-ph` | General Physics |
| `math.CO` | Combinatorics |
| `q-bio.QM` | Quantitative Methods |
| `stat.ML` | Machine Learning (Statistics) |

## 🔧 Model Management

### List Available Models
```bash
python -m apfs.main list-models
```

### Pull New Models
```bash
python -m apfs.main pull-model llama3.1:8b
```

### Recommended Models

| Model | RAM Usage | Speed | Quality | Best For |
|-------|-----------|-------|---------|----------|
| `llama3.2:3b` | ~4 GB | Fast | Good | General use, limited resources |
| `llama3.1:8b` | ~8 GB | Medium | Better | Better summaries, more detail |
| `mistral:7b` | ~6 GB | Medium | Good | Alternative to Llama |
| `phi3:mini` | ~2 GB | Very Fast | Basic | Very limited resources |

## 📁 Project Structure

```
arxiv-paper-finder/
├── apfs/
│   ├── __init__.py
│   ├── main.py              # CLI interface
│   ├── arxiv_client.py      # ArXiv API integration  
│   ├── pdf_handler.py       # PDF download and text extraction
│   ├── summarizer.py        # LLM integration
│   └── output_formatter.py  # Output formatting
├── requirements.txt
├── setup.py
└── README.md
```

## 🐛 Troubleshooting

### Common Issues

**"Model not found" error:**
```bash
ollama pull llama3.2:3b
```

**"No papers found" error:**
- Try broader search terms
- Check category spelling
- Verify date range format (YYYY-MM-DD)

**Memory errors:**
- Use smaller models (phi3:mini, llama3.2:3b)
- Use `--abstract-only` flag
- Reduce `--max-results`

**PDF download failures:**
- Check internet connection
- Some papers may have download restrictions
- Tool automatically falls back to abstract-only

### Performance Tips

1. **For faster performance**: Use `--abstract-only` flag
2. **For better summaries**: Use `--full-text` with larger models
3. **For batch processing**: Increase `--max-results` but monitor RAM usage
4. **For storage**: Use `--cleanup` (default) to remove PDFs after processing

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and enhancement requests.

## 📝 License

This project is open source. Please check the license file for details.

## 🙏 Acknowledgments

- [arXiv](https://arxiv.org/) for providing free access to scientific papers
- [Ollama](https://ollama.ai/) for making local LLM deployment easy
- The open source community for the amazing libraries used in this project

---

**Happy Researching! 🎓**