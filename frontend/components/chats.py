import streamlit as st
import requests

def load_chat_history(chat_id, token):
    headers = {"user_id": token}
    response = requests.get(f"http://localhost:5000/chats/{chat_id}", headers=headers)
    if response.status_code == 200:
        return response.json()["chat_history"]
    else:
        st.error("Unable to load chat history")
        return []

def chat_window(token):
    st.title("ChatBot")

    # Check if a chat is selected
    if "selected_chat_id" in st.session_state:
        chat_id = st.session_state["selected_chat_id"]
        chat_history = load_chat_history(chat_id, token)

        # Display chat history
        for chat in chat_history:
            st.write(f"**{chat['role']}**: {chat['content']}")
    else:
        # Show button to create a new chat
        if st.button("Start New Chat"):
            # Initialize a new chat ID (you may need to create a new chat in the backend)
            # For this example, we'll just set a placeholder for the chat ID
            st.session_state["selected_chat_id"] = "new_chat_id"  # This should be replaced with the actual creation logic
            st.session_state["chat_history"] = []  # Initialize empty chat history
            st.success("New chat started! You can start chatting now.")
    
    # Handle new messages
    prompt = st.chat_input("Ask me anything...")
    
    if prompt:
        new_chat = {"role": "user", "content": prompt}
        if "chat_history" in st.session_state:
            st.session_state["chat_history"].append(new_chat)

        response = requests.post(f"http://localhost:5000/chats/{st.session_state['selected_chat_id']}", json={"prompt": prompt}, headers={"user_id": token})
        if response.status_code == 200:
            assistant_message = response.json()["assistant_message"]
            st.session_state["chat_history"].append({"role": "assistant", "content": assistant_message})
            st.write(f"**Assistant**: {assistant_message}")
        else:
            st.error("Error sending message")
