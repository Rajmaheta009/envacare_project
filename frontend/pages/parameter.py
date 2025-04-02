import streamlit as st
import requests
import pandas as pd

BASE_URL = "http://localhost:8000"
PARAMETER_URL = f"{BASE_URL}/parameter"
PARENT_PARAMETER_URL = f"{BASE_URL}/parent_parameter"

if "edit_form" not in st.session_state:
    st.session_state.edit_form = None
if "edit_param" not in st.session_state:
    st.session_state.edit_param = {}

# API functions
def create_parent_parameter(data):
    response = requests.post(f"{PARENT_PARAMETER_URL}/", json=data)
    if response.status_code in [200, 201]:
        st.success("Parent parameter added successfully!")
        return response.json().get("id")
    else:
        st.error(f"Failed to add parent parameter: {response.text}")
        return None

def create_parameter(data):
    response = requests.post(f"{PARAMETER_URL}/", json=data)
    if response.status_code in [200, 201]:
        st.success("Parameter added successfully!")
    else:
        st.error(f"Failed to add parameter: {response.text}")

def fetch_parent_parameters():
    response = requests.get(PARENT_PARAMETER_URL)
    return response.json() if response.status_code == 200 else []

def fetch_parameters():
    response = requests.get(PARAMETER_URL)
    return response.json() if response.status_code == 200 else []

def update_parent_parameter(inx, id):
    name = st.session_state.get(f"input_{inx}", "")
    data = {"name": name}
    response = requests.put(f"{PARENT_PARAMETER_URL}/{id}", json=data)
    if response.status_code == 200:
        st.success("Parent parameter updated successfully!")
        st.session_state.edit_form = None
    else:
        st.error(f"Failed to update parent parameter: {response.text}")

def update_parameter(inx, parameter_id):
    data = {
        "parent_id": st.session_state[f"input_p_id_{inx}"],
        "name": st.session_state[f"input_name_{inx}"],
        "price": st.session_state[f"input_price_{inx}"],
        "min_range": st.session_state[f"input_min_{inx}"],
        "max_range": st.session_state[f"input_max_{inx}"],
        "protocol": st.session_state[f"input_protocol_{inx}"]
    }
    response = requests.put(f"{PARAMETER_URL}/{parameter_id}", json=data)
    if response.status_code == 200:
        st.success("Parameter updated successfully!")
        st.session_state.edit_param[inx] = False
    else:
        st.error(f"Failed to update parameter: {response.text}")

def delete_parent_parameter(p_id):
    response = requests.delete(f"{PARENT_PARAMETER_URL}/{p_id}")
    if response.status_code == 200:
        st.success("Parent parameter deleted successfully!")

def delete_parameter(p_id):
    response = requests.delete(f"{PARAMETER_URL}/{p_id}")
    if response.status_code == 200:
        st.success("Parameter deleted successfully!")

# Fetch data once
display_parent_parameters = fetch_parent_parameters()
display_parameters = fetch_parameters()

# Create Parent Parameter Form
with st.form("parent_parameter_form"):
    st.markdown("### Create Parent Parameter")
    name = st.text_input("Parent Parameter Name:", placeholder="Enter parameter name")
    submit_btn = st.form_submit_button("✅ Submit")
    if submit_btn and name:
        create_parent_parameter({"name": name})

# Add Parameter Form
with st.form("add_parameter_form"):
    st.markdown("### Add Parameter Data")
    p_id = st.number_input("Parent id", min_value=1)
    name = st.text_input("Parameter Name")
    protocol = st.text_input("Protocol Name")
    price = st.number_input("Price", min_value=0.0, step=0.1, format="%.2f")
    min_value = st.number_input("Min Value", min_value=0)
    max_value = st.number_input("Max Value", min_value=0)
    submit_btn = st.form_submit_button("✅ Submit Parameter")
    if submit_btn and name:
        create_parameter({"parent_id": p_id, "name": name, "price": price, "min_range": min_value, "max_range": max_value, "protocol": protocol})
        st.rerun()

# Display Parent Parameters
st.markdown("### Parent Parameters")
for ind, row in enumerate(display_parent_parameters):
    with st.expander(f"Details of {row['name']}"):
        st.markdown(f"**Parent Parameter ID:** {row['id']}")
        st.markdown(f"**Parent Parameter Name:** {row['name']}")
        if st.button("Edit", key=f"edit_parent_{ind}"):
            st.session_state.edit_form = ind
        if st.button("Delete", key=f"delete_parent_{ind}"):
            delete_parent_parameter(row['id'])
        if st.session_state.edit_form == ind:
            edit_name = st.text_input("Edit Parent Parameter Name", value=row['name'], key=f"input_{ind}")
            if st.button("Update Parent"):
                update_parent_parameter(ind, row['id'])
            if st.button("Cancel Edit"):
                st.session_state.edit_form = None

# Display Parameters
st.markdown("### Parameters")
for ind, param in enumerate(display_parameters):
    with st.expander(f"Details of {param['name']}"):
        st.markdown(f"**Id:** {param['id']}")
        st.markdown(f"**Parent Id:** {param['parent_id']}")
        st.markdown(f"**Price:** {param.get('price', 'N/A')}")
        st.markdown(f"**Min Value:** {param.get('min_range', 'N/A')}")
        st.markdown(f"**Max Value:** {param.get('max_range', 'N/A')}")
        st.markdown(f"**Protocol:** {param.get('protocol', 'N/A')}")
        if st.button("Edit", key=f"edit_param_{ind}"):
            st.session_state.edit_param[ind] = True
        if st.button("Delete", key=f"delete_param_{ind}"):
            delete_parameter(param['id'])
        if st.session_state.edit_param.get(ind, False):
            with st.form(f"edit_param_form_{ind}"):
                edit_p_id = st.number_input("Edit Parent Id", value=param['parent_id'], key=f"input_p_id_{ind}")
                edit_name = st.text_input("Edit Parameter Name", value=param['name'], key=f"input_name_{ind}")
                edit_price = st.number_input("Edit Price", value=float(param['price']), key=f"input_price_{ind}")
                edit_min = st.number_input("Edit Min Value", value=float(param['min_range']), key=f"input_min_{ind}")
                edit_max = st.number_input("Edit Max Value", value=float(param['max_range']), key=f"input_max_{ind}")
                edit_protocol = st.text_input("Edit Protocol Name", value=param['protocol'], key=f"input_protocol_{ind}")
                update_btn = st.form_submit_button("Update Parameter", on_click=update_parameter, args=(ind, param['id']))
                cancel_btn = st.form_submit_button("Cancel Edit")
                if cancel_btn:
                    st.session_state.edit_param[ind] = False
