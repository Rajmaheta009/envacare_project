import streamlit as st
import pandas as pd
import requests

# API URLs
API_BASE_URL = "http://localhost:8000"
CUSTOMER_API = f"{API_BASE_URL}/customer_request/"
ORDER_API = f"{API_BASE_URL}/order/"
QUOTATION_API = f"{API_BASE_URL}/quotations/"

# Initialize session state variables
if "login" not in st.session_state:
    st.session_state.login = False
if "show_form" not in st.session_state:
    st.session_state.show_form = False
if "selected_customer_id" not in st.session_state:
    st.session_state.selected_customer_id = None

# Sample Parameters with Costs
parameters = {
    "Header 1": {"Sub1": 100, "Sub2": 200, "Sub3": 150},
    "Header 2": {"Sub4": 300, "Sub5": 250},
    "Header 3": {"Sub6": 400, "Sub7": 350}
}


# ✅ Function to fetch customers with orders
def fetch_customers_with_orders():
    """Fetch customers with associated order data"""
    try:
        customers = requests.get(CUSTOMER_API).json()
        orders = requests.get(ORDER_API).json()

        # Map orders to customers by ID
        order_map = {order['customer_id']: order for order in orders}

        # Merge customer data with order data
        for customer in customers:
            customer_id = customer.get("id")
            order = order_map.get(customer_id, {})

            customer["order_req_comment"] = order.get("order_req_comment", "No comment")
            customer["order_req_doc"] = order.get("order_req_doc", "No document")

        return customers

    except Exception as e:
        st.error(f"⚠️ Error: {e}")
        return []


# ✅ Function to submit customer request
def submit_customer_request(data, comment, docfile):
    """Create customer request and corresponding order"""
    customer_response = requests.post(CUSTOMER_API, json=data)

    if customer_response.status_code == 200:
        customer = customer_response.json()
        customer_id = customer.get("id") or customer.get("customer_id")

        if customer_id:
            # Create order linked to the customer
            order_data = {
                "customer_id": customer_id,
                "order_req_comment": comment,
                "order_req_doc": docfile if docfile else "No document uploaded",
                "status": "Quotation Check"
            }

            order_response = requests.post(ORDER_API, json=order_data)

            if order_response.status_code == 201:
                st.success("✅ Customer and Order created successfully!")
                st.session_state.show_form = False
                st.rerun()
            else:
                st.error(f"❌ Failed to create order. Status: {order_response.status_code}")
        else:
            st.error("❌ Customer ID not found in response!")
    else:
        st.error(f"❌ Failed to submit customer request. Status: {customer_response.status_code}")


# ✅ Function to submit quotation
def submit_quotation(order_id, selected_params, total_cost):
    """Submit quotation linked to customer_id"""
    quotation_data = {
        "order_id": order_id,
        "pdf_url":"that is pandding"
    }

    try:
        response = requests.post(QUOTATION_API, json=quotation_data)
        if response.status_code == 200:
            st.success("✅ Quotation added successfully!")
            st.session_state.selected_customer_id = None  # Reset selection
            st.rerun()
        else:
            st.error(f"❌ Failed to submit quotation: {response.status_code}")
    except Exception as e:
        st.error(f"⚠️ Error: {e}")


# ✅ Main App Logic
if st.session_state.login:
    st.title("📝 Customer Requests")

    # 🚀 Customer Request Form at the Top
    if st.button("➕ Add Request"):
        st.session_state.show_form = True

    if st.session_state.show_form:
        with st.form("customer_form"):
            st.markdown("### 🛠️ Add New Customer Request")

            col1, col2 = st.columns(2)
            name = col1.text_input("Customer Name", placeholder="Enter customer name", max_chars=50)
            email = col2.text_input("Email ID", placeholder="Enter customer email")

            col3, col4 = st.columns(2)
            phone = col3.text_input("Phone Number", placeholder="Enter phone number")
            whatsapp = col4.text_input("WhatsApp Number", placeholder="Enter WhatsApp number")

            address = st.text_area("Address", placeholder="Enter customer address")

            col5, col6 = st.columns(2)
            comment = col5.text_area("Comment", placeholder="Add comments")
            document = col6.file_uploader("Upload Document", type=["pdf", "docx", "txt", "xlsx", "csv"])

            submit_btn = st.form_submit_button("✅ Submit")
            cancel_btn = st.form_submit_button("❌ Cancel")

            if submit_btn:
                if name and email and phone and (comment or document):
                    new_customer = {
                        "name": name,
                        "email": email,
                        "phone_number": phone,
                        "whatsapp_number": whatsapp,
                        "address": address,
                        "is_delete": False
                    }
                    docfile = document.name if document else "No document uploaded"

                    submit_customer_request(new_customer, comment, docfile)
                else:
                    st.error("❌ Please fill all required fields and add a comment or document.")

            if cancel_btn:
                st.session_state.show_form = False
                st.rerun()

    # 🚀 Display Customer List with Quotation Form
    st.markdown("### 📊 Submitted Customer Requests")

    customers = fetch_customers_with_orders()

    if customers:
        for customer in customers:
            customer_id = customer.get("id")

            # Expandable section for each customer
            with st.expander(f"{customer['name']} - {customer['email']}"):
                st.write(f"**Address:** {customer['address']}")
                st.write(f"**Phone:** {customer['phone_number']}")
                st.write(f"**WhatsApp:** {customer['whatsapp_number']}")
                st.write(f"**Comment:** {customer['order_req_comment']}")
                st.write(f"**Document:** {customer['order_req_doc']}")

                # Quotation button
                if st.button(f"➕ Add Quotation for {customer['name']}", key=f"quote_{customer_id}"):
                    st.session_state.selected_customer_id = customer_id

                # ✅ Display quotation form immediately below the customer
                if st.session_state.selected_customer_id == customer_id:
                    st.markdown("### ✏️ Create Quotation")

                    # Compact layout: customer + parameters in the same section
                    with st.container():
                        col1, col2 ,col3 = st.columns([3, 4,3])

                        # Customer details on the left
                        with col1:
                            st.markdown("#### 🛠️ Customer Details")
                            st.write(f"**Name:** {customer['name']}")
                            st.write(f"**Email:** {customer['email']}")
                            st.write(f"**Comments:** {customer['order_req_comment']}")
                            st.write(f"**Doc:** {customer['order_req_doc']}")

                        # Parameters + Cost on the right
                        with col2:
                            st.markdown("#### 🔥 Select Parameters")

                            selected_params = {}
                            for header, items in parameters.items():
                                st.markdown(f"**{header}**")
                                for param, cost in items.items():
                                    if st.checkbox(f"{param} - ₹{cost}", key=f"{customer_id}_{param}"):
                                        selected_params[param] = cost
                        with col3:
                            st.subheader("Total Cost and Parameter Count")  # Heading
                            # Total cost and parameter count
                            total_cost = sum(selected_params.values())
                            param_count = len(selected_params)

                            st.write(f"**Total Parameters:** {param_count}")
                            st.write(f"**Total Cost:** 💵 ₹{total_cost}")

                    # Submit button
                    if st.button("✅ Submit Quotation", key=f"submit_quote_{customer_id}"):
                        submit_quotation(customer_id, selected_params, total_cost)

else:
    st.warning("🚫 Please log in to access this page.")
