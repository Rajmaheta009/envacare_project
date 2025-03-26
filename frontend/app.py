import streamlit as st

# Initialize session state for login
if "login" not in st.session_state:
    st.session_state.login = False

# Redirect if already logged in
if st.session_state.login:
    st.success("✅ You are already logged in!")
    st.switch_page("pages/Dashboard.py")  # Redirect to the dashboard

# Title in the left column
col1, col2, col3 = st.columns([1, 3, 1])
col1.title("Login")

# Logo in the right column
col3.image("logo.png", width=150)

# Login Form
with st.form("login_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_btn = st.form_submit_button("🔑 Login")

# Check credentials
if login_btn:
    if username == "admin" and password == "admin":
        st.session_state.login = True
        st.success("✅ Login successful! Redirecting...")
        st.rerun()  # Proper rerun after login
    else:
        st.error("❌ Invalid username or password. Try again.")