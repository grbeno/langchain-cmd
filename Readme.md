## 🌱 LLM based AI-chat testing with Langchain on CLI

:point_right: __requirements: python, openai_api_key, huggingface_api_key__
#### Set up a virtual environment in the selected project directory
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
You can select open-source models from Hugging Face, such as `Meta-Llama-3`, but it does not work properly yet.
```
python chat.py --model meta-llama/Meta-Llama-3-8B-Instruct
```
You can select chat mode as well. Default is: `Short and concise`
```
python chat.py --mode "Correct english"
```
---
```
#.env

OPENAI_API_KEY
HUGGINGFACE_API_KEY

# langchain/langsmith

LANGCHAIN_API_KEY
```
:point_right: More in .app_info