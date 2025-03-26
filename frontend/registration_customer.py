import streamlit as st
from datetime import datetime

# Predefined Parameters Extracted from the PDF
parameters = [
    "Acenaphthene", "Acenaphthylene", "Acid Mist", "Acidity",
    "Alachlor", "Aldrin", "Alkalinity", "Aluminium",
    "Ammonia", "Ammonical Nitrogen", "Anthracene", "Antimony",
    "Barium", "Benzene", "Beryllium", "BOD", "Boron",
    "Calcium", "Cadmium", "Chloride", "Chromium", "Cobalt",
    "Copper", "Cyanide", "Dissolved Oxygen", "Fluoride",
    "Iron", "Lead", "Magnesium", "Manganese", "Mercury",
    "Nickel", "Nitrate", "Oil & Grease", "pH",
    "Phenolic Compounds", "Phosphorus", "Selenium", "Silver",
    "Sulphate", "Total Dissolved Solids (TDS)", "Zinc"
]

# Page Title
st.title("Customer Registration with Water Parameters")

# Customer Information Form
with st.form("customer_form"):
    # Customer Details
    name = st.text_input("Name")
    address = st.text_area("Address")
    description = st.text_area("Description")
    location = st.text_input("Location")

    # Date of Registration
    date_register = st.date_input("Date of Registration", datetime.today())

    # Sample Quantity (ML only, min 10 ml)
    sample_quantity = st.number_input("Sample Quantity (ml)", min_value=100, step=1)

    sample_condition = st.selectbox(
        "Sample Condition", ["Good", "Average", "Poor", "Contaminated"]
    )

    # Parameters Section
    st.subheader("Select Water Parameters")
    selected_params = st.multiselect("Choose Parameters", options=parameters)

    # Submit Button
    submit = st.form_submit_button("Submit")

# Form Submission Handling
if submit:
    if name and address and location and selected_params:
        st.success("Customer Registered Successfully!")
        st.write("### Details:")
        st.write(f"**Name:** {name}")
        st.write(f"**Address:** {address}")
        st.write(f"**Description:** {description}")
        st.write(f"**Location:** {location}")
        st.write(f"**Date:** {date_register}")
        st.write(f"**Sample Quantity:** {sample_quantity} ml")
        st.write(f"**Sample Condition:** {sample_condition}")
        st.write(f"**Selected Parameters:** {', '.join(selected_params)}")
    else:
        st.error("Please fill in all required fields and select at least one parameter.")
