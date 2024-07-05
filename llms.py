import os

from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEndpoint


class Llms():
    
    def __init__(self, model: str, provider: str) -> None:
        self.model = model
        self.provider = provider  # openai, huggingface

    
    def __select_gpt(self) -> callable:
        return ChatOpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
            model=self.model,
            max_tokens=100,
            temperature=0.7,
        )
        
    def __select_hf_opensource(self) -> callable:
        return HuggingFaceEndpoint(
            repo_id=self.model,
            task="text-generation",
            max_new_tokens=100,
            do_sample=False,
            huggingfacehub_api_token=os.environ.get("HUGGINGFACE_API_KEY"),
        )
        
    def get_model(self):
        if self.provider == 'openai':
            return self.__select_gpt()
        elif self.provider == 'huggingface':
            return self.__select_hf_opensource()
        else:
            raise ValueError('Invalid provider')
    
