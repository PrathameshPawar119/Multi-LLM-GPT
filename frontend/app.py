import streamlit as st
import requests
import logging

# logging.basicConfig(level=print)
BASE_URL = "http://localhost:5000"

def login():
    st.title("Login")

    email = st.text_input("Email", key="email_input_login")
    password = st.text_input("Password", type="password", key="password_input_login")

    if st.button("Login", key="login_button"):
        response = requests.post(
            f"{BASE_URL}/login",
            json={"email": email, "password": password},
        )
        print("Login Response ", response)
        if response.status_code == 200:
            data = response.json()
            st.session_state["token"] = data["token"]
            st.session_state["user_id"] = data["user_id"]
            st.session_state["logged_in"] = True
            st.success("Logged in successfully!")
            print(f"Logged in user ID: {st.session_state['user_id']}")
            st.rerun()
        else:
            st.error("Invalid credentials")

    if st.button("Sign Up instead"):
        st.session_state["show_signup"] = True

def register():
    st.title("Sign Up")
    
    email = st.text_input("Email", key="email_input_register")
    password = st.text_input("Password", type="password", key="password_input_register")
    confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password_input_register")

    if st.button("Sign Up", key="signup_button"):
        if password != confirm_password:
            st.error("Passwords do not match!")
        else:
            response = requests.post(
                f"{BASE_URL}/register",
                json={"email": email, "password": password},
            )
            if response.status_code == 201:
                st.success("User registered successfully!")
                st.session_state["show_signup"] = False
            elif response.status_code == 400:
                st.error(response.json()["message"])
            else:
                st.error("Registration failed!")
    
    if st.button("Login"):
        st.session_state["show_signup"] = False

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
        logging.error(f"Failed to fetch chats. Status code: {response.status_code}")
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
            logging.error(f"Failed to send message. Status code: {response.status_code}")



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

def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if "show_signup" not in st.session_state:
        st.session_state["show_signup"] = False

    if not st.session_state["logged_in"]:
        if st.session_state["show_signup"]:
            register()
        else:
            login()
    else:
        print(f"Frontend Logged in user ID: {st.session_state['user_id']}")
        display_sidebar()
        chat_window()

if __name__ == "__main__":
    main()