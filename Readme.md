## 🌱 LLM based AI-chat testing with Langchain on CLI

:point_right: __Requirements: Python, and any API keys and functions you want; I am currently using openai_api_key, langchain_api_key and huggingface_api_key.__
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
You can select other models: `gpt-4` for example.
```
python chat.py --m gpt-4
```
You can select chat role as well. Default is: `short and concise`
```
python chat.py --r "correct english"
```
Other roles: `correct german` `translate to english` / german / spanish / french / hungarian

End conversation: `add empty row <- push enter`

---
```
#.env

OPENAI_API_KEY
HUGGINGFACE_API_KEY

# langchain/langsmith

LANGCHAIN_API_KEY
```
:point_right: More in .app_info