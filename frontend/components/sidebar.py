import streamlit as st
from components.chats import load_chats

def display_sidebar():
    print(f"Frontend Logged in user ID: {st.session_state['user_id']}")

    st.sidebar.title("Chat History")

    if st.sidebar.button("New Chat"):
        st.session_state["selected_chat_id"] = "new_chat"
        st.session_state.messages = []
        st.rerun()

    chats = load_chats()
    for i, chat in enumerate(chats):
        if st.sidebar.button(f"Chat {i+1}", key=f"chat_{chat['_id']}"):
            st.session_state["selected_chat_id"] = chat["_id"]
            st.rerun()
