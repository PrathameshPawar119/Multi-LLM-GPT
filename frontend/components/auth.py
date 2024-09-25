import streamlit as st
import requests

def login():
    st.title("Login")

    email = st.text_input("Email", key="email_input_login")
    password = st.text_input("Password", type="password", key="password_input_login")

    if st.button("Login", key="login_button"):
        response = requests.post(
            "http://localhost:5000/login",
            json={"email": email, "password": password},
        )
        if response.status_code == 200:
            token = response.json()["token"]
            st.session_state["token"] = token
            st.session_state["logged_in"] = True
            st.success("Logged in successfully!")
        else:
            st.error("Invalid credentials")

    # Button to switch to signup page
    if st.button("Sign Up instead"):
        st.session_state["show_signup"] = True

# Register Function
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
                "http://localhost:5000/register",
                json={"email": email, "password": password},
            )
            if response.status_code == 201:
                st.success("User registered successfully!")
                st.session_state["is_registering"] = False  # Switch to login after successful registration
            elif response.status_code == 400:
                st.error(response.json()["message"])
            else:
                st.error("Registration failed!")
    
    # Button to switch to Login page
    if st.button("Login"):
        st.session_state["is_registering"] = False
