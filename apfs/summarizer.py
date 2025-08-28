import ollama
from typing import Optional, Dict, Any
from enum import Enum


class SummaryType(Enum):
    GENERAL = "general"
    KEY_FINDINGS = "key_findings"
    METHODS = "methods"
    IMPLICATIONS = "implications"


class LLMSummarizer:
    def __init__(self, model_name: str = "llama3.2:3b", max_tokens: int = 300):
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.client = ollama.Client()
        
    def check_model_availability(self) -> bool:
        try:
            response = self.client.list()
            
            # Handle different possible response structures
            if isinstance(response, dict):
                if 'models' in response:
                    models = response['models']
                else:
                    models = response
            else:
                models = response
            
            available_models = []
            for model in models:
                if isinstance(model, dict):
                    if 'name' in model:
                        available_models.append(model['name'])
                    elif 'model' in model:
                        available_models.append(model['model'])
                else:
                    available_models.append(str(model))
            
            return any(self.model_name in model for model in available_models)
            
        except Exception as e:
            print(f"Error checking model availability: {e}")
            print("This usually means Ollama is not running. Please start Ollama first.")
            return False
    
    def pull_model_if_needed(self) -> bool:
        if not self.check_model_availability():
            try:
                print(f"Pulling model {self.model_name}...")
                self.client.pull(self.model_name)
                return True
            except Exception as e:
                print(f"Failed to pull model {self.model_name}: {e}")
                return False
        return True
    
    def get_summary_prompt(self, summary_type: SummaryType) -> str:
        prompts = {
            SummaryType.GENERAL: """Summarize this academic paper in approximately 200-300 words. Focus on:
1. The main research question or problem
2. The approach or methodology used
3. Key findings or results
4. Significance and implications

Text to summarize:""",
            
            SummaryType.KEY_FINDINGS: """Extract and summarize the key findings from this academic paper. Focus only on:
1. Main results and discoveries
2. Important data or evidence presented
3. Conclusions drawn by the authors

Text to summarize:""",
            
            SummaryType.METHODS: """Summarize the methodology and approach used in this academic paper. Focus on:
1. Research methods employed
2. Experimental design or theoretical approach
3. Data sources and analysis techniques
4. Any novel methodological contributions

Text to summarize:""",
            
            SummaryType.IMPLICATIONS: """Analyze the implications and significance of this academic paper. Focus on:
1. Broader impact on the field
2. Practical applications
3. Future research directions suggested
4. How this work advances current knowledge

Text to summarize:"""
        }
        return prompts[summary_type]
    
    def summarize_paper(
        self, 
        paper_content: str, 
        title: str,
        summary_type: SummaryType = SummaryType.GENERAL
    ) -> Optional[str]:
        if not self.pull_model_if_needed():
            return None
        
        prompt = self.get_summary_prompt(summary_type)
        
        truncated_content = paper_content[:8000] if len(paper_content) > 8000 else paper_content
        
        full_prompt = f"{prompt}\n\nTitle: {title}\n\n{truncated_content}"
        
        try:
            response = self.client.chat(
                model=self.model_name,
                messages=[
                    {
                        'role': 'user',
                        'content': full_prompt
                    }
                ],
                options={
                    'temperature': 0.7,
                    'top_p': 0.9,
                    'max_tokens': self.max_tokens,
                }
            )
            
            summary = response['message']['content'].strip()
            return summary
            
        except Exception as e:
            print(f"Failed to generate summary: {e}")
            return None
    
    def summarize_multiple_papers(
        self, 
        papers_data: list, 
        summary_type: SummaryType = SummaryType.GENERAL
    ) -> Dict[str, Optional[str]]:
        summaries = {}
        
        for i, (arxiv_id, title, content) in enumerate(papers_data):
            print(f"Generating summary for paper {i+1}/{len(papers_data)}: {title[:50]}...")
            summary = self.summarize_paper(content, title, summary_type)
            summaries[arxiv_id] = summary
        
        return summaries
    
    def get_available_models(self) -> list:
        try:
            response = self.client.list()
            
            # Handle different possible response structures
            if isinstance(response, dict):
                if 'models' in response:
                    models = response['models']
                else:
                    models = response
            else:
                models = response
            
            available_models = []
            for model in models:
                if isinstance(model, dict):
                    if 'name' in model:
                        available_models.append(model['name'])
                    elif 'model' in model:
                        available_models.append(model['model'])
                else:
                    available_models.append(str(model))
            
            return available_models
            
        except Exception as e:
            print(f"Error listing models: {e}")
            print("This usually means Ollama is not running. Please start Ollama first.")
            return []
    
    def set_model(self, model_name: str):
        self.model_name = model_name