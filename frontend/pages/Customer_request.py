import streamlit as st
import pandas as pd

# Initialize session state
if "login" not in st.session_state:
    st.session_state.login = False
if "show_form" not in st.session_state:
    st.session_state.show_form = False
if "form_data" not in st.session_state:
    st.session_state.form_data = []
if "quotation_data" not in st.session_state:
    st.session_state.quotation_data = []
if "current_customer" not in st.session_state:
    st.session_state.current_customer = None
if "show_quotation_form" not in st.session_state:
    st.session_state.show_quotation_form = False

# Sample Parameters and Sub-parameters with Costs
parameters = {
    "Header 1": {"Sub1": 100, "Sub2": 200, "Sub3": 150},
    "Header 2": {"Sub4": 300, "Sub5": 250},
    "Header 3": {"Sub6": 400, "Sub7": 350}
}

# Check login status
if st.session_state.login:

    # Page layout
    st.title("📝 Customer Requests")

    # Button to display the form
    if st.button("➕ Add Request"):
        st.session_state.show_form = True

    # Display the form
    if st.session_state.show_form:
        with st.form("customer_form"):
            st.markdown("### ➕ Add New Request")

            col1, col2 = st.columns(2)
            name = col1.text_input("Customer Name", placeholder="Enter customer name", max_chars=50)
            address = col2.text_area("Address", placeholder="Enter customer address")

            col3, col4 = st.columns(2)
            email = col3.text_input("Email ID", placeholder="Enter customer email")
            contact = col4.text_input("Contact Number", placeholder="Enter contact number")

            col5, col6 = st.columns(2)
            whatsapp = col5.text_input("WhatsApp Number", placeholder="Enter WhatsApp number")
            comment = col6.text_area("Comment (Optional)", placeholder="Add any comments")

            # Submit and Cancel buttons
            col_submit, col_cancel = st.columns([1, 1])
            submit_btn = col_submit.form_submit_button("✅ Submit")
            cancel_btn = col_cancel.form_submit_button("❌ Cancel")

        # Form submission logic
        if submit_btn:
            if name and email and contact:
                st.session_state.form_data.append({
                    "Name": name,
                    "Address": address,
                    "Email": email,
                    "Contact": contact,
                    "WhatsApp": whatsapp,
                    "Comment": comment if comment else "N/A"
                })
                st.success("✅ Request added successfully!")
                st.session_state.show_form = False
                st.rerun()
            else:
                st.error("❌ Please fill in all required fields.")

        if cancel_btn:
            st.session_state.show_form = False
            st.rerun()

    # Display submitted requests with "Add Quotation" buttons
    st.markdown("### 📊 Submitted Requests")

    if st.session_state.form_data:
        # Convert the form data into a DataFrame
        df = pd.DataFrame(st.session_state.form_data)

        # Add "Add Quotation" column with buttons
        for index, row in df.iterrows():
            cols = st.columns(len(df.columns) + 1)  # Extra column for the button

            # Display row data
            for i, value in enumerate(row):
                cols[i].write(value)

            # Add "Add Quotation" button
            if cols[-1].button("➕ Add Quotation", key=f"quote_{index}"):
                st.session_state.current_customer = row['Name']
                st.session_state.current_customer_email = row['Email']
                st.session_state.current_customer_comment = row['Comment']
                st.session_state.show_quotation_form = True

        # Display the quotation form dynamically
        if st.session_state.show_quotation_form:
            st.title("📝 Create Quotation")

            col_left, col_middle, col_right = st.columns([2, 3, 2])

            with st.form("quotation_form_data"):
                # Left Column → Customer Details
                with col_left:
                    st.markdown("### 📄 Customer Details")
                    st.write(f"**Name:** {st.session_state.current_customer}")
                    st.write(f"**Email:** {st.session_state.current_customer_email}")
                    st.write(f"**Comment:** {st.session_state.current_customer_comment}")

                # Middle Column → Parameters with Sub-parameters
                with col_middle:
                    st.markdown("### 🛠️ Parameters & Sub-parameters")
                    selected_params = {}

                    for header, sub_params in parameters.items():
                        st.subheader(header)
                        for sub_param, cost in sub_params.items():
                            key = f"{header}_{sub_param}"
                            if st.checkbox(f"{sub_param} (₹{cost})", key=key):
                                selected_params[sub_param] = cost

                # Right Column → Selected Parameters and Total Cost
                with col_right:
                    st.markdown("### 💰 Selected Parameters & Cost Summary")

                    if selected_params:
                        total_cost = sum(selected_params.values())
                        param_count = len(selected_params)

                        for param, cost in selected_params.items():
                            st.write(f"✅ {param}: ₹{cost}")

                        st.write("---")
                        st.write(f"**Total Parameters:** 🔢 {param_count}")
                        st.write(f"**Total Cost:** 💵 ₹{total_cost}")
                    else:
                        st.write("No parameters selected")

                # Submit and Cancel buttons
                col_submit, col_cancel = st.columns(2)
                submit_btn = col_submit.form_submit_button("✅ Submit Quotation")
                cancel_btn = col_cancel.form_submit_button("❌ Cancel")

                # Store the quotation data
                if submit_btn:
                    quotation = {
                        "Name": st.session_state.current_customer,
                        "Email": st.session_state.current_customer_email,
                        "Parameter List": ", ".join(selected_params.keys()),
                        "Total Cost": total_cost
                    }
                    st.session_state.quotation_data.append(quotation)

                    st.success(f"✅ Quotation added for {st.session_state.current_customer}")
                    st.session_state.show_quotation_form = False
                    st.rerun()

                if cancel_btn:
                    st.session_state.show_quotation_form = False
                    st.rerun()

    else:
        st.warning("⚠️ No data found")

else:
    st.text("⚠️ Please login first.")
    st.switch_page('app.py')
