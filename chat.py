import asyncio

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import AIMessage

from dotenv import load_dotenv
from colorama import init, Fore, Style

from llms import Llms, ChatContext
from prompts import custom_prompts
from helpers import parser, create_directories


# Initialize colorama
init()

# Load environment variables from .env file
load_dotenv()

# Parse arguments
args = parser.parse_args()
model = args.m
role = args.r


""" Apply the model """

llm = Llms(model)
model = llm.get_model()
selected_model = getattr(llm, 'model')

print(f"\n{Fore.LIGHTBLUE_EX}{Style.NORMAL}Model: {selected_model}")
print(f"{Fore.LIGHTBLUE_EX}{Style.NORMAL}Role: {role}")

system_prompt = f""" You are helpful, creative, clever, and very friendly assistant. 
{custom_prompts[role]} """  # Change this role to whatever you want

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}"),
])

chain = prompt | model | StrOutputParser()

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
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

    print(f"{Style.RESET_ALL}\nI am your assistant. Give me a prompt according to my role!")

    while True:
        
        if prompt := input(f"\n{Fore.YELLOW}{Style.NORMAL}User: "):
            
            # Print the AI response
            print(f"{Fore.GREEN}{Style.NORMAL}AI: ", end='')
            
            # Stream the AI model response after prompting
            config = {"configurable": {"session_id": "chat"}}
            
            # for response in with_message_history.stream(
            #     {"input": prompt},
            #     config=config,
            # ):
            #     print(response, end='', flush=True)
            ##Error in RootListenersTracer.on_chain_end callback: ValueError()
            ##Error in callback coroutine: ValueError()

            response = with_message_history.invoke(
                {"input": prompt},
                config=config,
            )
            
            for char in response:
                print(char, end='', flush=True)
                await asyncio.sleep(0.01)  # Adjust this value to control the speed of output

            # print(response)  # invoke
        
        else: 
            # Generate remarks if the role is 'correct ...'
            if 'correct' in role:
                remarks = ChatContext(store['chat'].messages, 'provide remarks').generate()
                print(f"\nRemarks:\n{remarks}")
            else:
                remarks = None
            
            # Ask a question to save or not to text file
            save = input("Do you want to save the conversation to a text file? (y/n): ")         
            
            if save.lower() == 'y':
                
                # Save the conversation to a text file
                filename = ChatContext(store['chat'].messages, "generate a filename").generate()
                
                # Make directories if not exists
                dir = 'conversations'
                create_directories(dir, role)
                
                with open(f"{dir}/{role}/{filename}.txt", 'w', encoding='UTF-8') as f:
                    f.write(f"Model: {selected_model}\n\n")
                    for message in store['chat'].messages:
                        prefix = "AI" if isinstance(message, AIMessage) else "User"
                        f.write(f"{prefix}: {message.content}\n")
                    if remarks:
                        f.write(f"\nRemarks:\n{remarks}")
                
                print(f"Conversation saved to the file: {filename}.txt")
            
            break  # Exit the loop if the user enters an empty prompt


if __name__ == '__main__':
    # Call the async function to start the chat loop
    asyncio.run(chat_loop())

