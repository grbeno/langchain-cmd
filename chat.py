import os
import argparse
import asyncio

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import AIMessage

from dotenv import load_dotenv
from llms import Llms

# Load environment variables from .env file
load_dotenv()

parser = argparse.ArgumentParser(description="Script to process model and provider")

# Add optional 'model' argument
parser.add_argument("--model", default="gpt-4o-mini", help="The model to use (required)")

# Parse arguments
args = parser.parse_args()
model = args.model

llm = Llms(model)
model = llm.get_model()
selected_model = getattr(llm, 'model')
print(f"Model: {selected_model}")

system_prompt = """ You are helpful, creative, clever, and very friendly assistant. 
Your response should be short but concise, no more than 5 sentences. """  # Change this role to whatever you want

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="history"),
    ("user", "{input}"),
])

chain = prompt | model | StrOutputParser()

store = {}
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# Create a runnable that keeps track of the message history
with_message_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

# Chat on the command line
async def chat_loop():
    print("\nI am your assistant. Ask me anything or chat with me.")
    while True:
        if prompt := input("\nUser: "):
            config = {"configurable": {"session_id": "chat"}}
            response = with_message_history.invoke(
                {"input": prompt},
                config=config,
            )
            if 'gpt' in selected_model:
                response = response
            print(f"AI: ", end='')
            async for chunk in chain.astream({"input": prompt, "history": list(response)}):
                print(chunk, end='', flush=True)
        else:
            # Ask a question to save or not to text file, if yes then save the conversation to a text file
            save = input("Do you want to save the conversation to a text file? (y/n): ")
            if save.lower() == 'y':
                # Make directory if not exists
                dir = 'conversations'
                if not os.path.exists(dir):
                    os.makedirs(dir)
                filename = input("Enter a valid filename (without extension): ")
                with open(f"{dir}/{filename}.txt", 'w') as f:
                    f.write(f"Model: {selected_model}\n\n")
                    for message in store['chat'].messages:
                        prefix = "AI" if isinstance(message, AIMessage) else "User"
                        f.write(f"{prefix}: {message.content}\n")
                print("Conversation saved to text file.")
            break  # Exit the loop if the user enters an empty prompt

# Call the async function to start the chat loop
asyncio.run(chat_loop())
