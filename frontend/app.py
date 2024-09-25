import streamlit as st
from components.auth import login, register
from components.chats import load_chat_history, load_chats, chat_window
from components.sidebar import display_sidebar

# logging.basicConfig(level=print)
BASE_URL = "http://localhost:5000"





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