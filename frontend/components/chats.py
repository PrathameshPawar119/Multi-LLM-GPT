import streamlit as st
import requests

BASE_URL = "http://localhost:5000"


def load_chat_history(chat_id):
    print(f"load_chat_history Logged in user ID: {st.session_state['user_id']}")
    payload = {"user_id": st.session_state["user_id"]}
    response = requests.get(f"{BASE_URL}/chats/{chat_id}", json=payload)
    if response.status_code == 200:
        return response.json()["chat_history"]
    else:
        st.error("Unable to load chat history")
        return []

def load_chats():
    print(f"load_chats Logged in user ID: {st.session_state['user_id']}")
    payload = {"user_id": st.session_state["user_id"]}
    response = requests.post(f"{BASE_URL}/chats", json=payload)
    if response.status_code == 200:
        chats = response.json()
        print(f"Received {len(chats)} chats")
        # Sort chats by createdAt in descending order
        chats.sort(key=lambda x: x.get('createdAt', ''), reverse=True)
        return chats
    else:
        st.error(f"Unable to fetch chats. Status code: {response.status_code}")
        print(f"Failed to fetch chats. Status code: {response.status_code}")
        return []

def chat_window():
    st.title("ChatBot")
    print(f"chat_window Logged in user ID: {st.session_state['user_id']}")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "selected_chat_id" in st.session_state and st.session_state["selected_chat_id"] != "new_chat":
        chat_id = st.session_state["selected_chat_id"]
        st.session_state.messages = load_chat_history(chat_id)

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is your question?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        print(f"Sending message for user_id: {st.session_state['user_id']}")
        if "selected_chat_id" in st.session_state and st.session_state["selected_chat_id"] != "new_chat":
            response = requests.post(
                f"{BASE_URL}/chats/{st.session_state['selected_chat_id']}/messages",
                json={"prompt": prompt, "user_id": st.session_state["user_id"]}
            )
        else:
            response = requests.post(
                f"{BASE_URL}/createchat",
                json={"prompt": prompt, "user_id": st.session_state["user_id"]},
            )
        
        if response.status_code in [200, 201]:
            data = response.json()
            if "chat_id" in data:
                st.session_state["selected_chat_id"] = data["chat_id"]
            with st.chat_message("assistant"):
                st.markdown(data['assistant_message'])
            st.session_state.messages.append({"role": "assistant", "content": data['assistant_message']})
            print(f"Received response for chat_id: {st.session_state['selected_chat_id']}")
        else:
            st.error(f"Error sending message. Status code: {response.status_code}")
            print(f"Failed to send message. Status code: {response.status_code}")


