from setuptools import setup, find_packages

setup(
    name="arxiv-paper-finder",
    version="1.0.0",
    description="ArXiv Paper Finder and Summarizer - A local tool for discovering and summarizing academic papers",
    author="APFS Development Team",
    packages=find_packages(),
    install_requires=[
        "arxiv>=2.1.3",
        "pdfplumber>=0.11.4",
        "requests>=2.31.0",
        "ollama>=0.3.2",
        "rich>=13.7.1",
        "click>=8.1.7",
    ],
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "apfs=apfs.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)