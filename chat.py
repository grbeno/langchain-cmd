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
from colorama import init, Fore, Style

from llms import Llms, ChatContext
from prompts import custom_prompts

# Initialize colorama
init()

# Load environment variables from .env file
load_dotenv()

parser = argparse.ArgumentParser(description="Script to process model and provider")

# Add optional 'model' argument
parser.add_argument("--model", default="gpt-4o-mini", help="The model to use (optional)")
parser.add_argument("--mode", default="Short and concise", help="The mode to response to the prompt (optional)")

# Parse arguments
args = parser.parse_args()
model = args.model
response_mode = args.mode

llm = Llms(model)
model = llm.get_model()
selected_model = getattr(llm, 'model')
print(f"{Fore.LIGHTBLUE_EX}{Style.NORMAL}Model: {selected_model}")
print(f"{Fore.LIGHTBLUE_EX}{Style.NORMAL}Response mode: {response_mode}")

system_prompt = f""" You are helpful, creative, clever, and very friendly assistant. 
{custom_prompts[response_mode]} """  # Change this role to whatever you want

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}"),
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
    
    print(f"{Style.RESET_ALL}\nI am your assistant. Ask me anything or chat with me.")
    
    while True:
        
        if prompt := input(f"\n{Fore.YELLOW}{Style.NORMAL}User: "):
            
            # Invoke the AI model with the prompt
            response = with_message_history.invoke(
                {"input": prompt},
                config={"configurable": {"session_id": "chat"}},
            )
            
            # Print the AI response
            print(f"{Fore.GREEN}{Style.NORMAL}AI: ", end='')
            
            # Streaming output
            for char in response:
                print(char, end='', flush=True)
                await asyncio.sleep(0.01)  # Adjust this value to control the speed of output
        
        else:
            # Ask a question to save or not to text file
            save = input("Do you want to save the conversation to a text file? (y/n): ")
            
            if save.lower() == 'y':
                
                # Make directory if not exists
                dir = 'conversations'
                if not os.path.exists(dir):
                    os.makedirs(dir)
                
                # Save the conversation to a text file
                aigenerated_filename =ChatContext(store['chat'].messages).add_filename()
                
                with open(f"{dir}/{aigenerated_filename}.txt", 'w', encoding='UTF-8') as f:
                    f.write(f"Model: {selected_model}\n\n")
                    for message in store['chat'].messages:
                        prefix = "AI" if isinstance(message, AIMessage) else "User"
                        f.write(f"{prefix}: {message.content}\n")
                
                print(f"Conversation saved to the file: {aigenerated_filename}.txt")
            
            break  # Exit the loop if the user enters an empty prompt

# Call the async function to start the chat loop
asyncio.run(chat_loop())
