import streamlit as st
from pages.parameter import fetch_parent_parameters

parent_parameters = fetch_parent_parameters()

def data_fatch_edit_form(inx):
    st.write(st.session_state[f"input_{inx}"])
    parent_parameters[inx]['name'] = st.session_state[f"input_{inx}"]

def get_edit_name(name):
    if name:
        st.write(name)



for ind,row in enumerate(parent_parameters):
    with st.expander(f"**Details of {row['name']}**"):
        st.markdown(f"**Parent Parameter id :- {row['id']}**")
        st.markdown(f"**Parent Parameter name :- {row['name']}**")
        col1, col2 = st.columns([2, 1])
        edit_button = st.button("Edit", key=row['id'])
        delete_button = st.button("Delete", key=f"del_{row['id']}")

        # Action handling for Edit or Delete
        if edit_button:
            # st.session_state.edit_form = row['id']  # Set the form for this parameter
            # Edit Form inside st.form
            # with st.form(f"edit_parent_form_{row['id']}"):
            p_edit_name = st.text_input("Edit Parent Parameter New Name",key=f"input_{ind}", value=row['name'],on_change=data_fatch_edit_form,args=(ind,))
            # p_update_btn = st.button("Update Parent",on_click=update_parent_parameter,args=(row['id'], {"name":p_edit_name}))
            p_update_btn = st.button("Update Parent",on_click=get_edit_name,args=(p_edit_name,))
            p_cancel_btn = st.button("Cancel Edit")
