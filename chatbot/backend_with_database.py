from json import load
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage 
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite import SqliteSaver # import sqlitesaver
import sqlite3
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
conn = sqlite3.connect(database = 'chatbot.db', check_same_thread=False)

checkpointer = SqliteSaver(conn=conn) # this is SqliteSaver database which is saving all the converstation
graph = StateGraph(ChatState)

# add nodes 
graph.add_node('chat_node', chat_node)

# add edge
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)
#compile
chatbot = graph.compile(checkpointer=checkpointer)

# We can also test it out using invoke and manupilating the thread_id to store in different threads

# Utility function
def retrive_all_threads() :
    all_threads = set()
    for checkpoint in checkpointer.list(None) :
        all_threads.add(checkpoint.config['configurable']['thread_id'])

    return list(all_threads)
#print(retrive_all_threads())