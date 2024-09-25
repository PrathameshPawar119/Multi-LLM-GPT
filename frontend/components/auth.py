import streamlit as st
import requests
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