import streamlit as st
from streamlit_javascript import st_javascript

def set_local_store_value():
    st.markdown(
        """
    <script>
        localStorage.setItem("login_status", "true");
        window.location.reload();
    </script>
    """,
        unsafe_allow_html=True
    )
def get_local_store_vlaue():
    # ✅ Retrieve LocalStorage Value
    local_storage_value = st_javascript("localStorage.getItem('login_status')")
    return local_storage_value