import streamlit as st
from chatbot.backend import chatbot
from langchain_core.messages import HumanMessage

# Use a consistent thread_id for the session (LangGraph MemorySaver uses thread_id, not session_id)
CONFIG = {'configurable': {'thread_id': 'streamlit-session-1'}}

# Initialize display history (for UI only; actual conversation is in MemorySaver)
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

# Display chat history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.markdown(message['content'])  # Use markdown for richer formatting

user_input = st.chat_input('Type here')

if user_input:
    # Add user message to UI display
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.markdown(user_input)
    
    # With Stremming 
    with st.chat_message('assistant') :
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
            {'messages': [HumanMessage(content=user_input)]},
            config=CONFIG,
            stream_mode='messages'
            )
        )
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
