import streamlit as st
from route import router
from vectordb import faq_chain
from sqlite import sql_chain
st.title("E-Commerce Bot")







# Initialize session state
def init_chat_history():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

# Add message to history
def add_message(role, content):
    st.session_state.chat_history.append({"role": role, "content": content})

# Render chat history
def render_chat_history():
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# Main app logic
init_chat_history()
render_chat_history()

# input
user_input = st.chat_input("Your message")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)
        # response
        # router
        if router(user_input).name == "faq":
            response = faq_chain(user_input)
        elif router(user_input).name == "sql":
            response = sql_chain(user_input)
        else:
            response = "Invalid :   please ask questions about products"

    add_message("user", user_input)
    # Replace with your agent or response logic

    add_message("assistant", response)
    st.rerun()
