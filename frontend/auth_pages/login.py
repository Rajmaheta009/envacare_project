import requests
import streamlit as st
from component.local_store import set_local_store_value
from component.nav import login_nav

st.session_state.login = False

# --- Backend API URL ---
BASE_URL = "http://127.0.0.1:8000/auth"
LOGIN_URL = f"{BASE_URL}/"

# Layout: Title and Logo
col1, col2, col3 = st.columns([1.3, 1, 1])
col1.image("static/logo.png", width=150)

col4, col5 = st.columns([2, 3])
col4.title("Login")

# ✅ Login Form
with st.form("login_form"):
    email = st.text_input("Email")
    password = st.text_input(label="Password", type="password")
    login_btn = st.form_submit_button("🔑 Login")

# 🚀 API call to FastAPI for authentication
if login_btn:
    response = requests.post(LOGIN_URL, json={"email": email, "password": password})
    if response.status_code == 200:
        data = response.json()

        # ✅ Store user info in session state
        st.session_state.username = data.get("username", "")
        st.session_state.user_id = data.get("id", "")
        st.session_state.login = True

        st.success("✅ Login successful! Redirecting...")
        set_local_store_value()
        main=st.Page("main.py",title="main")
        pg = st.navigation([main], position="hidden")
        pg.run()
    else:
        st.error("❌ Invalid credentials. Try again.")

