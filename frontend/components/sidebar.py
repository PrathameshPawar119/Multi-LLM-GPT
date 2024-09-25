import streamlit as st
import requests

def load_chats(token):
    headers = {"user_id": token}
    response = requests.get("http://localhost:5000/chats", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Unable to fetch chats")
        return []

def display_sidebar(token):
    st.sidebar.title("Chat History")

    chats = load_chats(token)
    selected_chat = st.sidebar.radio("Select a chat", options=[chat["_id"] for chat in chats])

    if selected_chat:
        st.session_state["selected_chat_id"] = selected_chat
