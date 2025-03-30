import streamlit as st

nav_pages=[
    st.Page("pages/dashboard.py", title= "Dashboard"),
    st.Page("pages/Customer_request.py", title= "Customer Request"),
    st.Page("pages/Quotation.py", title= "Quotation List"),
    st.Page("pages/Sample.py", title= "Sample List"),
    st.Page("pages/Result.py", title= "Result Set"),
    st.Page("pages/log_out.py", title= "Log Out")
]

login_nav=[
    st.Page("auth_pages/login.py",title="login")
]

log_out_nav=[
    st.Page("pages/log_out.py",title="log out")
]