import streamlit as st
from pages.parameter import fetch_parameters

# Fetch all parameters
parameters = fetch_parameters()

# Split parameters into parents (no price) and children (with price)
parent_parameters = [p for p in parameters if p["price"] is None]
child_parameters = [p for p in parameters if p["price"] is not None]

# Streamlit layout
st.set_page_config(layout="wide")
st.title("🧪 Test Quotation Designer")

col1, col2 = st.columns([2, 1])

# Build a lookup table by parent_id
child_map = {}
for p in parameters:
    parent_id = p.get("parent_id")
    if parent_id is not None:
        child_map.setdefault(parent_id, []).append(p)

selected_parameters = {}

def render_parameters(parent_id):
    children = child_map.get(parent_id, [])
    for child in children:
        if child["price"] is None:
            st.markdown(f"**{child['name']}**")
            render_parameters(child["id"])
        else:
            key = f"{child['id']}_{child['name']}"
            if st.checkbox(f"{child['name']} ₹{child['price']}", key=key):
                selected_parameters[child["name"]] = child["price"]
            else:
                selected_parameters.pop(child["name"], None)


with col1:
    st.subheader("📌 Select Parameters")
    for parent in parent_parameters:
        if parent["parent_id"] is None:
            st.markdown(f"### {parent['name']}")
            render_parameters(parent["id"])

with col2:
    st.subheader("🧾 Selected Parameters")
    total = 0
    for name, price in selected_parameters.items():
        st.write(f"- {name}: ₹{price}")
        total = total + price

    st.markdown("---")
    st.markdown(f"### 💰 Total Cost: ₹{total}")
