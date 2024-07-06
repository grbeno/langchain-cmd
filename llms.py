import os

from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEndpoint


class Llms():
    """Selects the model from OpenAI or Hugging Face."""
    
    def __init__(self, model: str) -> None:
        self.model = model

    def __select_gpt(self) -> callable:
        """Selects the model from OpenAI."""
        return ChatOpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
            model=self.model,
            max_tokens=100,
            temperature=0.7,
        )
        
    def __select_hf_opensource(self) -> callable:
        """Selects the model from the Hugging Face model hub."""
        return HuggingFaceEndpoint(
            repo_id=self.model,
            task="text-generation",
            max_new_tokens=100,
            do_sample=False,
            huggingfacehub_api_token=os.environ.get("HUGGINGFACE_API_KEY"),
        )
        
    def get_model(self):
        """Selects the model."""
        if 'gpt' in self.model:
            return self.__select_gpt()
        else:
            return self.__select_hf_opensource()
    
