import os
import json

from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.messages import AIMessage, HumanMessage
from langchain_ollama.llms import OllamaLLM

from prompts import custom_prompts


class Llms():
    """Selects the model from OpenAI or Hugging Face."""
    
    def __init__(self, model: str) -> None:
        self.model = model

    def openai(self) -> callable:
        """Selects the model from OpenAI."""
        return ChatOpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
            model=self.model,
            max_tokens=200,
            temperature=0.7,
        )
        
    def hugging_face(self) -> callable:
        """Selects the model from the Hugging Face model hub."""
        return HuggingFaceEndpoint(
            repo_id=self.model,
            task="text-generation",
            max_new_tokens=200,
            do_sample=False,
            huggingfacehub_api_token=os.environ.get("HUGGINGFACE_API_KEY"),
        )
    
    def ollama(self) -> callable:
        """Selects the model from OpenAI."""
        return OllamaLLM(model=self.model)
        
    def get_model(self):
        """Selects the model."""
        if 'gpt' in self.model:
            return self.openai()
        else:
            #return self.hugging_face()
            return self.ollama()


class ChatContext(Llms):

    def __init__(self, conversation: dict, prompt_keyword: str) -> None:
        super().__init__('gpt-4o-mini')
        self.conversation = conversation
        self.prompt_keyword = prompt_keyword

    def get_content(self) -> json:
        res = []
        for message in self.conversation:
            if self.prompt_keyword == "provide remarks" and isinstance(message, HumanMessage):
                res.append(message.content)
            else:
                res.append(f"{'AI' if isinstance(message, AIMessage) else 'User'}: {message.content}")
        return json.dumps(res)
    
    def generate(self) -> str:    
        create_title = [
            (
                "system",
                custom_prompts[self.prompt_keyword],
            ),
            ("human", self.get_content()),  # should not be list!
        ]
        return self.openai().invoke(create_title).content
    
