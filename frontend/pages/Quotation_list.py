import streamlit as st
import pandas as pd

# Initialize session state variables
if "login" not in st.session_state:
    st.session_state.login = False
# Check for login
if st.session_state.login:
    # Page Layout
    col1, col2, col3 = st.columns([3, 1, 2])
    col1.subheader("Welcome to Quotation List")

    # Display Submitted Quotations
    st.markdown("### 📄 Submitted Quotations")

    if st.session_state.quotation_data:
        # Display table
        df = pd.DataFrame(st.session_state.quotation_data)
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("⚠️ No data found")

else:
    st.text("⚠️ Please login first.")
    st.switch_page('app.py')
