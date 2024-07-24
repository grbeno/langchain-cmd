### LLM based AI-chat testing with Langchain on CLI

__requirement: python__\
Set virtual environment in the selected project directory
```
python -m venv .venv
```
```
.venv/Scripts/activate  # windows
```
```
source venv/bin/activate  # linux or mac
``` 
```
pip install -r requirements.txt
```
---
Default model `gpt-4o-mini` from OpenAI.
```
python chat.py
```
You can select other models: `gpt-3.5-turbo` for example.
```
python chat.py --model gpt-3.5-turbo
```
You can select open source models from HuggingFace: `Meta-Llama-3` for example.
```
python chat.py --model meta-llama/Meta-Llama-3-8B-Instruct
```
```
#.env

OPENAI_API_KEY
HUGGINGFACE_API_KEY

# langchain/langsmith

LANGCHAIN_API_KEY
HUGGINGFACE_API_KEY
```