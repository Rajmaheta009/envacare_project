import requests
import streamlit as st
import pandas as pd

# ✅ Initialize session state variables to prevent AttributeError
if "login" not in st.session_state:
    st.session_state.login = False
if "form_data" not in st.session_state:
    st.session_state.form_data = []
if "quotation_data" not in st.session_state:
    st.session_state.quotation_data = []
if "sample_form_data" not in st.session_state:
    st.session_state.sample_form_data = []

API_BASE_URL = "http://localhost:8000"

# Page layout
col1, col2 = st.columns([5, 1])

# ✅ Dashboard Display
if st.session_state.login:
    col1.subheader(f"👋 Hello!{st.session_state.username}")
    col1.subheader(f" Welcome to the Dashboard")

    # Logout button
    if col2.button("🚪 Logout"):
        with st.spinner("Logging out..."):
            # Clear session state
            st.session_state.login = False
            st.success("✅ Successfully logged out!")
            st.rerun()

    # ✅ Customer Request Section
    st.subheader("📥 Customer Requests")
    try:
        response = requests.get(f"{API_BASE_URL}/customer_request/")

        if response.status_code == 200:
            data = response.json()

            if data:
                df = pd.DataFrame(data)
                df = df.drop("id", axis=1)
                df = df.drop("is_delete", axis=1)
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("⚠️ No customer requests found")
        else:
            st.error("❌ Failed to fetch customer requests")

    except Exception as e:
        st.error(f"⚠️ Error: {e}")

    # ✅ Customer Quotations Section
    st.subheader("💰 Customer Quotations")
    try:
        response = requests.get(f"{API_BASE_URL}/quotations/")
        if response.status_code == 200:
            data = response.json()

            if data:
                df = pd.DataFrame(data)
                df = df.drop("id", axis=1)
                df = df.drop("order_id", axis=1)
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("⚠️ No customer requests found")
        else:
            st.error("❌ Failed to fetch customer requests")

    except Exception as e:
        st.error(f"⚠️ Error: {e}")

    # ✅ Sample Details Section
    st.subheader("🧪 Sample Details")
    if st.session_state.sample_form_data:
        df = pd.DataFrame(st.session_state.sample_form_data)
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("⚠️ No sample details found")

else:
    st.text("⚠️ Please login first")
    st.switch_page("app.py")
