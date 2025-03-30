import streamlit as st
# from component.local_store import get_local_store_
from component.nav import nav_pages,login_nav

# ✅ Initialize session state
if "login" not in st.session_state:
    st.session_state.login = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "user_id" not in st.session_state:
    st.session_state.user_id = ""
if "role" not in st.session_state:
    st.session_state.role = ""

# ✅ Sync LocalStorage with session state
# st.session_state.login = True
# ✅ Navigation Logic
if not st.session_state.login:
    # login_page = st.Page("auth_pages/login.py", title="Login")
    pg = st.navigation(login_nav, position="hidden")
    pg.run()
else:
    pg = st.navigation(nav_pages)
    # st.switch_page("Dashboard.py")
    pg.run()
