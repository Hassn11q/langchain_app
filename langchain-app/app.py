# Depndencies
import streamlit as st
from chain import chain
from langchain_core.messages import HumanMessage , AIMessage


# Initialize or retrieve chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []



st.set_page_config(page_title='منير')
# Define the title
st.title("منير خبير السيارات")

# Conversation 
for message in st.session_state.chat_history:
    if isinstance(message , HumanMessage):
        with st.chat_message('Human'):
             st.markdown(message.content)
    else:
        with st.chat_message('AI'):
             st.markdown(message.content)

# User input and processing
user_input = st.chat_input("...اكتب سؤالك هنا")
if user_input is not None and user_input != "":
    # Add the user message to the session state
    st.session_state.chat_history.append(HumanMessage(user_input))

    with st.chat_message("Human"):
         st.markdown(user_input)

    with st.chat_message('AI'):
         ai_response = st.write_stream(chain.stream(user_input))    
    st.session_state.chat_history.append(AIMessage(ai_response))
