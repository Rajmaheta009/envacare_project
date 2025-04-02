import streamlit as st
import requests
from streamlit import session_state

# API URLs
API_BASE_URL = "http://localhost:8000"
CUSTOMER_API = f"{API_BASE_URL}/customer_request/"
ORDER_API = f"{API_BASE_URL}/order/"
QUOTATION_API = f"{API_BASE_URL}/quotations/"

# Initialize session state variables
if "show_form" not in st.session_state:
    st.session_state.show_form = False
if "selected_customer_id" not in st.session_state:
    st.session_state.selected_customer_id = None
if "customer_to_edit" not in st.session_state:
    st.session_state.customer_to_edit = None

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


# ✅ Function to fetch customer details by ID for editing
def fetch_customer_by_id(customer_id):
    """Fetch customer details for a specific customer ID"""
    try:
        customer = requests.get(f"{CUSTOMER_API}{customer_id}/").json()
        return customer
    except Exception as e:
        st.error(f"⚠️ Error fetching customer details: {e}")
        return None


# ✅ Function to fetch order details by customer ID
def fetch_order_by_customer_id(customer_id):
    """Fetch order details for a specific customer ID"""
    try:
        order = requests.get(f"{ORDER_API}?customer_id={customer_id}").json()
        return order[0]
    except Exception as e:
        st.error(f"⚠️ Error fetching order details: {e}")
        return None


# ✅ Function to create a new customer and order
def create_customer_and_order(data, comment, docfile):
    """Create a new customer and order"""
    try:
        # Create new customer
        response = requests.post(CUSTOMER_API, json=data)
        if response.status_code == 200:
            customer = response.json()
            customer_id = customer.get("id")

            # Create a new order for the customer
            order_data = {
                "customer_id": customer_id,
                "order_req_comment": comment,
                "status": "Quotation Check"
            }
            files = {'docfile': docfile} if docfile else None
            order_response = requests.post(ORDER_API, data=order_data, files=files)

            if order_response.status_code == 200:
                st.success("✅ Customer and Order created successfully!")
                st.session_state.show_form = False
                st.rerun()
            else:
                st.error(f"❌ Failed to create order. Status: {order_response.status_code}")
                st.write(order_data)
                st.write(files)

    except Exception as e:
        st.error(f"⚠️ Error: {e}")


# ✅ Function to update an existing customer and order
def update_customer_and_order(customer_id, order_id, data, comment, docfile):
    """Update an existing customer and order"""
    try:
        # Update customer
        response = requests.put(f'{CUSTOMER_API}{customer_id}', json=data)
        if response.status_code == 200:
            # Update order for the customer
            order_data = {
                "customer_id": customer_id,
                "order_req_comment": comment,
                "status": "Quotation Check"
            }
            if st.session_state.doc_check != docfile:
                files = {'docfile': docfile}
                order_response = requests.put(f"{ORDER_API}{order_id}", data=order_data, files=files)
            else:
                order_response = requests.put(f"{ORDER_API}{order_id}", data=order_data)

            if order_response.status_code == 200:
                st.success("✅ Customer and Order updated successfully!")
                st.session_state.show_form = False
                st.rerun()
            else:
                st.error(f"❌ Failed to update order. Status: {order_response.status_code}")

    except Exception as e:
        st.error(f"⚠️ Error: {e}")

def delete_customer_with_order(c_id,o_id):
    delete_c=requests.delete(f"{CUSTOMER_API}{c_id}")
    if delete_c.status_code == 204:
        delete_o=requests.delete(f"{ORDER_API}{o_id}")
        if delete_o.status_code == 200:
            st.success("Delete Successfully")
        else:
            st.error(f"❌ Failed to Order delete.")
    else:
        st.error(f"❌ Failed to Customer Request delete.")

# ✅ Main App Logic
if session_state.login:
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
                create_customer_and_order(new_customer, comment, document)
            else:
                st.error("❌ Please fill all required fields and add a comment or document.")

            if cancel_btn:
                st.session_state.show_form = False
                st.rerun()

    # 🚀 Display Customer List with Quotation Form
    st.markdown("### 📊 Submitted Customer Requests")

    customers = fetch_customers_with_orders()
    if not customers:
        st.warning("⚠️ No customer requests found")

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

                col1 , col2 = st.columns([1,1])
                # Edit button for each customer
                if col1.button(f"Edit => {customer['name']}", key=f"edit_{customer_id}"):
                    # Fetch customer details based on customer_id
                    customer_details = fetch_customer_by_id(customer_id)
                    if customer_details:
                        # Store the selected customer details in session state for editing
                        st.session_state.show_form = True
                        st.session_state.customer_to_edit = customer_details  # Store customer data in session state


                with col2.popover(f"Delete => {customer['name']}"):
                    st.subheader("Are You Sure ?!")
                    col1, col2 = st.columns([1, 2])
                    if col1.button("YES"):
                        order = fetch_order_by_customer_id(customer_id)
                        order_id = order.get("id")
                        delete_customer_with_order(customer_id,order_id)
                    if col2.button("No"):
                        st.write("Ok! Info Is Safe")


                # Quotation button
                if st.button(f"➕ Add Quotation for {customer['name']}", key=f"quote_{customer_id}"):
                    st.session_state.selected_customer_id = customer_id

                # Show the Edit Form below customer details
                if st.session_state.show_form and "customer_to_edit" in st.session_state and st.session_state.customer_to_edit["id"] == customer_id:
                    # When the edit form is shown for the selected customer, pre-fill the form
                    customer_to_edit = st.session_state.customer_to_edit

                    order = fetch_order_by_customer_id(customer_id)
                    order_comment = order.get("order_req_comment", "")
                    order_doc = order.get("order_req_doc", "")

                    with st.form(f"customer_form_{customer_id}"):
                        st.markdown("### 🛠️ Edit Customer Request")

                        col1, col2 = st.columns(2)
                        name = col1.text_input("Customer Name", placeholder="Enter customer name", max_chars=50, value=customer_to_edit["name"])
                        email = col2.text_input("Email ID", placeholder="Enter customer email", value=customer_to_edit["email"])

                        col3, col4 = st.columns(2)
                        phone = col3.text_input("Phone Number", placeholder="Enter phone number", value=customer_to_edit["phone_number"])
                        whatsapp = col4.text_input("WhatsApp Number", placeholder="Enter WhatsApp number", value=customer_to_edit["whatsapp_number"])

                        address = st.text_area("Address", placeholder="Enter customer address", value=customer_to_edit["address"])

                        col5, col6 = st.columns(2)
                        comment = col5.text_area("Comment", placeholder="Add comments", value=order_comment)
                        document = col6.file_uploader("Upload Document", type=["pdf", "docx", "txt", "xlsx", "csv"], key=f"edit_document_{customer_id}")

                        if order_doc:
                            st.write(f"Existing document: {order_doc}")

                        st.session_state.doc_check= order_doc

                        submit_btn = st.form_submit_button("✅ Submit")
                        cancel_btn = st.form_submit_button("❌ Cancel")

                    if submit_btn:
                        if name and email and phone and (comment or document):
                            updated_customer = {
                                "name": name,
                                "email": email,
                                "phone_number": phone,
                                "whatsapp_number": whatsapp,
                                "address": address,
                                "is_delete": False
                            }

                            docfile = document
                            order_id = order.get("id")
                            if docfile:
                                update_customer_and_order(customer_id, order_id, updated_customer, comment, docfile)
                            else:
                                update_customer_and_order(customer_id, order_id, updated_customer, comment,order_doc)
                        else:
                            st.error("❌ Please fill all required fields and add a comment or document.")

                    if cancel_btn:
                        st.session_state.show_form = False
                        st.session_state.customer_to_edit = None  # Clear customer data from session state
                        st.rerun()

else:
    st.warning("🚫 Please log in to access this page.")
    st.switch_page("auth_pages/login.py")
