import streamlit as st
from chat import ChatBot

# Render the chat UI
def render_chat_ui(bot):
    st.set_page_config(
        page_title="ChatGPT 4o mini",
        page_icon="⚙️",
        layout="centered"
    )

    st.title("ChatGPT 4o mini")

    prompt = st.chat_input("Ask me anything...")

    if "chats" not in st.session_state:
        st.session_state.chats = []

    # Update chat state using the bot's handle_chat method
    st.session_state.chats = bot.handle_chat(prompt, st.session_state.chats)

    # Display chat messages
    for chat in st.session_state.chats:
        st.chat_message(chat['role']).text(chat['content'])

def main():
    bot = ChatBot() 
    render_chat_ui(bot)

if __name__ == "__main__":
    main()
