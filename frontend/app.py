import streamlit as st
import requests

# Backend API URL
BASE_URL = "http://127.0.0.1:8000/auth"
LOGIN_URL = f"{BASE_URL}/"

# Initialize session state
if "login" not in st.session_state:
    st.session_state.login = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "email" not in st.session_state:
    st.session_state.email = ""
if "role" not in st.session_state:
    st.session_state.role = ""

# 🚦 Redirect if already logged in
if st.session_state.login:
    st.switch_page("pages/dashboard.py")


# Layout: Title and Logo
col1, col2, col3 = st.columns([1, 3, 1])
col1.title("Login")
col3.image("logo.png", width=150)

# Login Form
with st.form("login_form"):
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    login_btn = st.form_submit_button("🔑 Login")

# 🚀 API call to FastAPI for authentication
if login_btn:
    with st.spinner("Authenticating..."):
        response = requests.post(LOGIN_URL, json={"email": email, "password": password})

        if response.status_code == 200:
            data = response.json()
            st.session_state.username=data["username"]
            st.session_state.user_id = data["id"]
            st.session_state.login = True
            st.rerun()

        else:
            st.error("❌ Invalid credentials. Try again.")
