import streamlit as st


with st.popover("Delete"):
    st.subheader("Are You Sure ?!")
    col1 , col2 = st.columns([1,2])
    if col1.button("YES"):
        st.write("Delete")
    if col2.button("No"):
        st.write("Nope")
# st.write("Your name:", name)