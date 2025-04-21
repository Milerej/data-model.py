import streamlit as st
from pyvis.network import Network
import networkx as nx
import streamlit.components.v1 as components
import tempfile
import os
import test  # Import your test.py file

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == "Showmethemoney":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("⚠️ Password incorrect")
        return False
    else:
        return True

if check_password():
    st.set_page_config(page_title="Interactive Interdependency Graph", layout="wide")
    
    # Create the sidebar
    with st.sidebar:
        st.title("Navigation")
        page = st.radio(
            "Choose a chart",
            ["System Management Graph", "Second Chart"]
        )
        # Add the view toggle to sidebar
        view_type = st.toggle("Enable Hierarchical Layout", False)

    # Main content area
    if page == "System Management Graph":
        st.title("⚙️ Entity Relationship Diagram : System Management and Agency Management Data Model (V2.2)")
        test.display_system_management_graph(view_type)  # Call function from test.py
        
    elif page == "Second Chart":
        st.title("Second Chart")
        # Add your second chart function here when ready
        st.write("Second chart coming soon...")

if __name__ == "__main__":
    st.set_page_config(layout="wide")
