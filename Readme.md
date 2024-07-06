### LLM based AI-chat testing with Langchain on CLI

1. Use CLI
2. Set virtual environment ( venv, pipenv ... )
3. Install `requirements.txt`
---
Default model `gpt-4o` from OpenAI.
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
.env

OPENAI_API_KEY
HUGGINGFACE_API_KEY

# langchain/langsmith

LANGCHAIN_API_KEY
HUGGINGFACE_API_KEY
```