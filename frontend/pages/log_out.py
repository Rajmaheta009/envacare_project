import streamlit as st
from component.nav import login_nav, nav_pages


col1 ,col2  = st.columns([1,2])
col2.subheader("You are sure to log out !?")

col1 , col2 , col3 = st.columns([1,1,1])
if col2.button("Yes"):
    st.session_state.login = False
    st.navigation(login_nav,position="hidden")
if col3.button("No"):
    st.navigation(nav_pages)
