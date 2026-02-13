from json import load
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage 
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv
load_dotenv()

CONFIG = {'configurable': {'thread_id': 'streamlit-session-1'}}

from langgraph.graph.message import add_messages

class ChatState(TypedDict) :
    messages : Annotated[list[BaseMessage], add_messages]

llm = ChatOpenAI()

def chat_node(state: ChatState) :
    # take user query from state
    messages = state['messages']
    
    # send to llm 
    response = llm.invoke(messages)
    
    # response store state
    return {"messages" : [response]}

checkpointer = MemorySaver() # this is persistance which is saving all the converstation
graph = StateGraph(ChatState)

# add nodes 
graph.add_node('chat_node', chat_node)

# add edge
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)
#compile
chatbot = graph.compile(checkpointer=checkpointer)

'''# ChatBot
if __name__ == "__main__" :
    thread_id = '1'
    while True :
        user_message = input("User: ")
        if user_message.strip().lower() in ['exit', 'quit', 'bye'] :
            break

        config = {'configurable': {'thread_id': thread_id}}
        
        response = chatbot.invoke({'messages' : [HumanMessage(content= user_message)]}, config=config)

        print("AI:" , response['messages'][-1].content)'''

# chatbot.get_state(config=config) this will show all the conversation