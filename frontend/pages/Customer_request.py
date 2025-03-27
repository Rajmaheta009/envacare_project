import streamlit as st
import pandas as pd
import requests

# API URLs
API_BASE_URL = "http://127.0.0.1:8000"
CUSTOMER_API = f"{API_BASE_URL}/customer_request/"
ORDER_API = f"{API_BASE_URL}/order/customer_id/"
QUOTATION_API = f"{API_BASE_URL}/quotations/"

# Initialize session state variables
if "login" not in st.session_state:
    st.session_state.login = False
if "show_form" not in st.session_state:
    st.session_state.show_form = False
if "show_quotation_form" not in st.session_state:
    st.session_state.show_quotation_form = False
if "customer_id" not in st.session_state:
    st.session_state.customer_id = None
if "order_id" not in st.session_state:
    st.session_state.order_id = None  # ✅ Store the latest order ID
if "current_customer" not in st.session_state:
    st.session_state.current_customer = None
if "current_customer_email" not in st.session_state:
    st.session_state.current_customer_email = None
if "c_comment" not in st.session_state:
    st.session_state.c_comment = None
if "c_doc" not in st.session_state:
    st.session_state.c_doc = None

# Sample Parameters with Costs
parameters = {
    "Header 1": {"Sub1": 100, "Sub2": 200, "Sub3": 150},
    "Header 2": {"Sub4": 300, "Sub5": 250},
    "Header 3": {"Sub6": 400, "Sub7": 350}
}

# Helper function to fetch customers
def fetch_customers():
    """Fetch customers from the API"""
    try:
        response = requests.get(CUSTOMER_API)
        if response.status_code == 200:
            return response.json()
        else:
            st.error("❌ Failed to fetch customer data.")
            return []
    except Exception as e:
        st.error(f"⚠️ Error: {e}")
        return []

# Fetch the latest order by customer ID
def fetch_latest_order(customer_id):
    """Fetch the latest order for the customer"""
    try:
        response = requests.get(f"{ORDER_API}{customer_id}")
        if response.status_code == 200:
            order = response.json()
            return order
        else:
            return None
    except Exception as e:
        st.error(f"⚠️ Error: {e}")
        return None

# Function to submit quotation
def submit_quotation(data):
    """Submit quotation linked to order_id"""
    try:
        response = requests.post(QUOTATION_API, json=data)
        if response.status_code == 201:
            st.success("✅ Quotation added successfully!")
            st.session_state.show_quotation_form = False
            st.rerun()
        else:
            st.error(f"❌ Failed to submit quotation: {response.status_code}")
            st.error(response.text)
    except Exception as e:
        st.error(f"⚠️ Error: {e}")

# Main app logic
if st.session_state.login:
    st.title("📝 Customer Requests")

    # Fetch and display customers
    customers = fetch_customers()

    if st.button("➕ Add Request"):
        st.session_state.show_form = True

    # Display customer requests with "Add Quotation" buttons
    st.markdown("### 📊 Submitted Customer Requests")

    if customers:
        df = pd.DataFrame(customers)

        for index, row in df.iterrows():
            customer_id = row.get("id")

            # Display customer data without 'id'
            row_display = row.drop("id")
            cols = st.columns(len(row_display) + 1)

            for i, value in enumerate(row_display):
                cols[i].write(value)

            # Add Quotation button
            if cols[-1].button("➕ Add Quotation", key=f"quote_{index}"):
                if customer_id:
                    st.session_state.customer_id = customer_id
                    st.session_state.current_customer = row['name']
                    st.session_state.current_customer_email = row['email']

                    # ✅ Fetch the latest order and store the `order_id`
                    latest_order = fetch_latest_order(customer_id)

                    if latest_order:
                        st.session_state.order_id = latest_order.get("id")  # Store `order_id`
                        st.session_state.c_comment = latest_order.get("order_req_comment", "No comment available")
                        st.session_state.c_doc = latest_order.get("order_req_doc", "No document uploaded")
                    else:
                        st.session_state.order_id = None
                        st.session_state.c_comment = "No comment available"
                        st.session_state.c_doc = "No document uploaded"

                    st.session_state.show_quotation_form = True

    # Display quotation form dynamically
    if st.session_state.show_quotation_form:
        st.title("📝 Create Quotation")

        col_left, col_middle, col_right = st.columns([2, 3, 2])

        with st.form("quotation_form"):
            # Left → Customer details
            with col_left:
                st.markdown("### 📄 Customer Details")
                st.write(f"**Name:** {st.session_state.current_customer}")
                st.write(f"**Email:** {st.session_state.current_customer_email}")
                st.write(f"**Comments:** {st.session_state.c_comment}")
                st.write(f"**Doc:** {st.session_state.c_doc}")

            # Middle → Parameter selection
            with col_middle:
                st.markdown("### 🛠️ Parameters")
                selected_params = {}
                for header, sub_params in parameters.items():
                    st.subheader(header)
                    for sub_param, cost in sub_params.items():
                        if st.checkbox(f"{sub_param} (₹{cost})"):
                            selected_params[sub_param] = cost

            # Right → Cost summary
            with col_right:
                total_cost = sum(selected_params.values())
                st.write(f"**Total Cost:** 💵 ₹{total_cost}")

            # ✅ Use `order_id` instead of `customer_id` in quotation submission
            if st.form_submit_button("✅ Submit Quotation"):
                if st.session_state.order_id:
                    quotation_data = {
                        "order_id": st.session_state.order_id,  # ✅ Use `order_id`
                        "pdf_url": "that time is pandding"
                    }
                    submit_quotation(quotation_data)
                else:
                    st.error("❌ No valid order ID found!")
else:
    st.switch_page("app.py")
