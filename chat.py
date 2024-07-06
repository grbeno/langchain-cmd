import argparse

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from dotenv import load_dotenv
from llms import Llms

# Load environment variables from .env file
load_dotenv()

parser = argparse.ArgumentParser(description="Script to process model and provider")

##  model
## 'gpt-4o'
## 'gpt-4'
## 'gpt-4-turbo'
## 'gpt-3.5-turbo'
## 'claude-3-5-sonnet-20240620'  # not yet available
## 'meta-llama/Meta-Llama-3-8B-Instruct'

# Add optional 'model' argument
parser.add_argument("--model", default="gpt-4o", help="The model to use (required)")

## provider
## 'openai'
## 'huggingface'

# Add optional 'provider' argument
# parser.add_argument("--provider", default="openai", help="The provider to use (optional)")

# Parse arguments
args = parser.parse_args()
model = args.model

llm = Llms(model)
model = llm.get_model()
selected_model = getattr(llm, 'model')
print(f"Model: {selected_model}")

system_prompt = "You are helpful, creative, clever, and very friendly assistant."  # Change this role to whatever you want

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="history"),
    ("user", "{input}"),
])

chain = prompt | model

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


with_message_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

# Chat on the command line
while True:
    if prompt := input("Prompt: "):
        config = {"configurable": {"session_id": "any"}}
        response = with_message_history.invoke(
            {"input": prompt},
            config=config,
        )
        if 'gpt' in selected_model:
            response = response.content
        print(response)
    else:
        break  # Exit the loop if the user enters an empty prompt
