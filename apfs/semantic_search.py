import re
from typing import List, Dict, Set, Tuple
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class SemanticExpansion:
    original_terms: List[str]
    expanded_terms: List[str]
    synonyms: Dict[str, List[str]]
    related_terms: Dict[str, List[str]]


class SemanticSearchEngine:
    """
    Enhanced semantic search engine for academic papers using keyword expansion,
    synonyms, and domain-specific term mapping.
    """
    
    def __init__(self):
        self.academic_synonyms = self._load_academic_synonyms()
        self.domain_terms = self._load_domain_terms()
        self.abbreviation_map = self._load_abbreviations()
        
    def _load_academic_synonyms(self) -> Dict[str, List[str]]:
        """Load academic field synonyms and related terms"""
        return {
            # AI/ML terms
            "artificial intelligence": ["AI", "machine intelligence", "computational intelligence", "intelligent systems"],
            "machine learning": ["ML", "statistical learning", "automated learning", "pattern recognition"],
            "deep learning": ["neural networks", "deep neural networks", "DNN", "artificial neural networks", "ANN"],
            "natural language processing": ["NLP", "computational linguistics", "language processing", "text processing"],
            "computer vision": ["CV", "image processing", "visual computing", "pattern recognition", "image analysis"],
            "reinforcement learning": ["RL", "reward learning", "sequential decision making", "policy learning"],
            "neural network": ["neural net", "connectionist", "artificial neural network", "ANN", "deep network"],
            "transformer": ["attention mechanism", "self-attention", "bert", "gpt", "language model"],
            "large language model": ["LLM", "foundation model", "generative model", "language generation"],
            "generative ai": ["generative model", "text generation", "image generation", "content generation"],
            
            # Computer Science terms  
            "algorithm": ["algorithmic", "computational method", "procedure", "technique"],
            "optimization": ["optimisation", "minimization", "maximization", "objective function"],
            "distributed computing": ["parallel computing", "cluster computing", "grid computing", "cloud computing"],
            "cybersecurity": ["information security", "network security", "computer security", "cyber defense"],
            "blockchain": ["distributed ledger", "cryptocurrency", "bitcoin", "ethereum", "smart contracts"],
            "quantum computing": ["quantum computation", "quantum algorithms", "quantum information", "qubits"],
            
            # Data Science terms
            "data science": ["data analytics", "data mining", "big data", "data analysis", "statistical analysis"],
            "data mining": ["knowledge discovery", "pattern mining", "data exploration", "information extraction"],
            "big data": ["large-scale data", "massive data", "data processing", "scalable analytics"],
            "statistics": ["statistical analysis", "statistical methods", "probability", "inference"],
            
            # Physics terms
            "quantum mechanics": ["quantum physics", "quantum theory", "wave mechanics", "matrix mechanics"],
            "relativity": ["general relativity", "special relativity", "einstein", "spacetime"],
            "particle physics": ["high energy physics", "elementary particles", "quantum field theory"],
            "condensed matter": ["solid state physics", "many-body physics", "materials science"],
            
            # Mathematics terms
            "linear algebra": ["matrix theory", "vector spaces", "eigenvalues", "linear transformations"],
            "calculus": ["differential calculus", "integral calculus", "mathematical analysis"],
            "graph theory": ["network theory", "combinatorial optimization", "discrete mathematics"],
            "topology": ["algebraic topology", "differential topology", "geometric topology"],
            
            # Biology/Medicine terms
            "bioinformatics": ["computational biology", "systems biology", "genomics", "proteomics"],
            "genetics": ["genomics", "molecular genetics", "heredity", "DNA analysis"],
            "neuroscience": ["brain research", "cognitive science", "neural networks", "neuroimaging"],
            "epidemiology": ["disease modeling", "public health", "infectious disease", "population health"],
            
            # Engineering terms
            "robotics": ["autonomous systems", "robot control", "mechatronics", "automation"],
            "control systems": ["feedback control", "system dynamics", "automatic control", "regulation"],
            "signal processing": ["digital signal processing", "DSP", "filtering", "spectral analysis"]
        }
    
    def _load_domain_terms(self) -> Dict[str, List[str]]:
        """Load domain-specific related terms"""
        return {
            "machine_learning": [
                "supervised learning", "unsupervised learning", "semi-supervised", "transfer learning",
                "feature selection", "dimensionality reduction", "cross-validation", "overfitting",
                "regularization", "gradient descent", "backpropagation", "ensemble methods"
            ],
            "deep_learning": [
                "convolutional neural networks", "CNN", "recurrent neural networks", "RNN", "LSTM", "GRU",
                "autoencoder", "generative adversarial networks", "GAN", "attention mechanism",
                "batch normalization", "dropout", "activation function", "loss function"
            ],
            "nlp": [
                "tokenization", "part-of-speech", "named entity recognition", "sentiment analysis",
                "machine translation", "question answering", "text classification", "language model",
                "word embedding", "BERT", "GPT", "transformer", "semantic parsing"
            ],
            "computer_vision": [
                "object detection", "image classification", "semantic segmentation", "face recognition",
                "optical character recognition", "OCR", "image processing", "feature extraction",
                "edge detection", "histogram", "convolution", "pooling"
            ],
            "quantum": [
                "qubit", "superposition", "entanglement", "quantum gate", "quantum circuit",
                "quantum algorithm", "quantum supremacy", "quantum error correction", "decoherence"
            ]
        }
    
    def _load_abbreviations(self) -> Dict[str, str]:
        """Load common academic abbreviations and their expansions"""
        return {
            "AI": "artificial intelligence",
            "ML": "machine learning", 
            "DL": "deep learning",
            "NLP": "natural language processing",
            "CV": "computer vision",
            "RL": "reinforcement learning",
            "CNN": "convolutional neural network",
            "RNN": "recurrent neural network",
            "LSTM": "long short-term memory",
            "GAN": "generative adversarial network",
            "LLM": "large language model",
            "NER": "named entity recognition",
            "OCR": "optical character recognition",
            "API": "application programming interface",
            "GPU": "graphics processing unit",
            "CPU": "central processing unit",
            "IoT": "internet of things",
            "AR": "augmented reality",
            "VR": "virtual reality"
        }
    
    def expand_query(self, query: str, expansion_mode: str = "moderate") -> SemanticExpansion:
        """
        Expand a search query with semantically related terms
        
        Args:
            query: Original search query
            expansion_mode: "conservative", "moderate", or "aggressive"
        """
        original_terms = self._extract_key_terms(query)
        expanded_terms = set(original_terms)
        synonyms = {}
        related_terms = {}
        
        for term in original_terms:
            term_lower = term.lower()
            
            # Add synonyms
            if term_lower in self.academic_synonyms:
                term_synonyms = self.academic_synonyms[term_lower]
                synonyms[term] = term_synonyms
                if expansion_mode in ["moderate", "aggressive"]:
                    expanded_terms.update(term_synonyms)
            
            # Add abbreviation expansions
            if term.upper() in self.abbreviation_map:
                expanded_term = self.abbreviation_map[term.upper()]
                expanded_terms.add(expanded_term)
                synonyms[term] = synonyms.get(term, []) + [expanded_term]
            
            # Add reverse abbreviation lookup
            for abbrev, expansion in self.abbreviation_map.items():
                if term_lower == expansion.lower():
                    expanded_terms.add(abbrev)
                    synonyms[term] = synonyms.get(term, []) + [abbrev]
            
            # Add domain-specific terms
            if expansion_mode == "aggressive":
                domain_key = term_lower.replace(" ", "_")
                if domain_key in self.domain_terms:
                    domain_related = self.domain_terms[domain_key]
                    related_terms[term] = domain_related
                    expanded_terms.update(domain_related[:5])  # Limit to top 5
        
        return SemanticExpansion(
            original_terms=original_terms,
            expanded_terms=list(expanded_terms),
            synonyms=synonyms,
            related_terms=related_terms
        )
    
    def _extract_key_terms(self, query: str) -> List[str]:
        """Extract key terms from a query string"""
        # Remove common stop words and extract meaningful terms
        stop_words = {
            "a", "an", "and", "are", "as", "at", "be", "by", "for", "from",
            "has", "he", "in", "is", "it", "its", "of", "on", "that", "the",
            "to", "was", "will", "with", "using", "based", "approach", "method"
        }
        
        # Split on common delimiters and clean
        terms = re.split(r'[,\s\-_]+', query.lower())
        terms = [term.strip() for term in terms if term.strip()]
        
        # Filter out stop words and short terms (but allow known abbreviations)
        meaningful_terms = []
        for term in terms:
            # Allow known abbreviations even if short
            if (term not in stop_words and 
                (len(term) > 2 or term.upper() in self.abbreviation_map)):
                meaningful_terms.append(term)
        
        # Also extract quoted phrases and multi-word terms
        quoted_phrases = re.findall(r'"([^"]*)"', query)
        meaningful_terms.extend(quoted_phrases)
        
        # Extract potential compound terms (2-3 words)
        words = query.split()
        for i in range(len(words) - 1):
            if len(words[i]) > 2 and len(words[i+1]) > 2:
                compound = f"{words[i]} {words[i+1]}".lower()
                if compound in self.academic_synonyms:
                    meaningful_terms.append(compound)
        
        return list(set(meaningful_terms))
    
    def build_semantic_query(self, original_query: str, expansion_mode: str = "moderate") -> str:
        """
        Build an enhanced ArXiv search query using semantic expansion
        """
        expansion = self.expand_query(original_query, expansion_mode)
        
        # Start with original query
        query_parts = [f'({original_query})']
        
        # Add synonyms with OR logic
        for original_term, term_synonyms in expansion.synonyms.items():
            if term_synonyms:
                synonym_query = " OR ".join([f'"{synonym}"' for synonym in term_synonyms[:3]])
                query_parts.append(f'({synonym_query})')
        
        # Combine with OR to broaden search
        if expansion_mode == "conservative":
            # Only use direct synonyms
            final_query = " OR ".join(query_parts[:2]) if len(query_parts) > 1 else query_parts[0]
        elif expansion_mode == "moderate":
            # Use synonyms and some expansions
            final_query = " OR ".join(query_parts[:4]) if len(query_parts) > 3 else " OR ".join(query_parts)
        else:  # aggressive
            # Use all expansions
            final_query = " OR ".join(query_parts)
        
        return final_query
    
    def rank_results_by_relevance(self, papers: List, original_query: str) -> List:
        """
        Rank search results by semantic relevance to original query
        """
        expansion = self.expand_query(original_query, "moderate")
        original_terms = set([term.lower() for term in expansion.original_terms])
        expanded_terms = set([term.lower() for term in expansion.expanded_terms])
        
        scored_papers = []
        
        for paper in papers:
            # Combine title and abstract for scoring
            text_content = f"{paper.title} {paper.abstract}".lower()
            
            # Score based on term matches
            original_score = sum(2 for term in original_terms if term in text_content)
            synonym_score = sum(1 for term in expanded_terms if term in text_content and term not in original_terms)
            
            # Category bonus for relevant fields
            category_score = 0
            for category in paper.categories:
                if any(term in category.lower() for term in original_terms):
                    category_score += 1
            
            total_score = original_score + (synonym_score * 0.5) + (category_score * 0.3)
            scored_papers.append((paper, total_score))
        
        # Sort by score descending, then by publication date descending
        scored_papers.sort(key=lambda x: (x[1], x[0].published), reverse=True)
        
        return [paper for paper, score in scored_papers]
    
    def explain_expansion(self, query: str, expansion_mode: str = "moderate") -> str:
        """
        Generate a human-readable explanation of query expansion
        """
        expansion = self.expand_query(query, expansion_mode)
        
        explanation = [f"Original query: '{query}'"]
        explanation.append(f"Expansion mode: {expansion_mode}")
        
        if expansion.synonyms:
            explanation.append("\nSynonyms found:")
            for term, synonyms in expansion.synonyms.items():
                explanation.append(f"  • {term}: {', '.join(synonyms[:3])}")
        
        if expansion.related_terms:
            explanation.append("\nRelated terms:")
            for term, related in expansion.related_terms.items():
                explanation.append(f"  • {term}: {', '.join(related[:3])}")
        
        semantic_query = self.build_semantic_query(query, expansion_mode)
        explanation.append(f"\nExpanded search query:\n{semantic_query}")
        
        return "\n".join(explanation)