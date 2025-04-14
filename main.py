import streamlit as st
from pyvis.network import Network
import networkx as nx
import streamlit.components.v1 as components
import tempfile
import os

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == "Showmethemoney":
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("⚠️ Password incorrect")
        return False
    else:
        # Password correct.
        return True

if check_password():
    st.set_page_config(page_title="Interactive Interdependency Graph", layout="wide")

    st.title("⚙️ Data Model : System Management")

    # Define entity modules and colors
    entities = {
        "System Management": {
            "color": "#2E7D32", 
            "size": 50, 
            "shape": "dot",
            "title": "System Management Module"
        },
        # Main Modules
        "System Identity & Classification": {
            "color": "#4CAF50", 
            "size": 25, 
            "shape": "dot",
            "title": "System Identity & Classification Sub-Module"
        },
        "Criticality & Risk": {
            "color": "#4CAF50", 
            "size": 25,
            "shape": "dot",
            "title": "Criticality & Risk Sub-Module"
        },
        "System Resilience": {
            "color": "#4CAF50", 
            "size": 25,
            "shape": "dot",
            "title": "System Resilience Sub-Module"
        },
        "Hosting and System Dependencies": {
            "color": "#4CAF50", 
            "size": 25,
            "shape": "dot",
            "title": "Hosting and System Dependencies Sub-Module"
        },

        # Sub-groups
        "Basic Information": {
            "color": "#66BB6A", 
            "size": 20, 
            "shape": "dot",
            "title": "Basic Information Sub-Group"
        },
        "Organizational Context": {
            "color": "#66BB6A", 
            "size": 20, 
            "shape": "dot",
            "title": "Organizational Context Sub-Group"
        },
        "Classification": {
            "color": "#66BB6A", 
            "size": 20, 
            "shape": "dot",
            "title": "Classification Sub-Group"
        },
        "Impact Assessment": {
            "color": "#66BB6A", 
            "size": 20, 
            "shape": "dot",
            "title": "Impact Assessment Sub-Group"
        },
        "Risk Profile": {
            "color": "#66BB6A", 
            "size": 20, 
            "shape": "dot",
            "title": "Risk Profile Sub-Group"
        },
        "SCA/RML Approval": {
            "color": "#66BB6A", 
            "size": 20, 
            "shape": "dot",
            "title": "SCA/RML Approval Sub-Group"
        },
        "Availability & Recovery": {
            "color": "#66BB6A", 
            "size": 20, 
            "shape": "dot",
            "title": "Availability & Recovery Sub-Group"
        },
        "Dependencies Management": {
            "color": "#66BB6A", 
            "size": 20, 
            "shape": "dot",
            "title": "Dependencies Management Sub-Group"
        },

        # Fields
        "Agency": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Agency field"
        },
        "Ministry Family": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Ministry Family field"
        },
        "System ID": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "System ID (Primary Key)"
        },
        "System Name": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "System Name field"
        },
        "System Description": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "System Description field"
        },
        "System Status": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "System Status field"
        },
        "Security Classification": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Security Classification field"
        },
        "Sensitivity Classification": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Sensitivity Classification field"
        },
        "Economy": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Economy impact field"
        },
        "Public Health and Safety": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Public Health and Safety field"
        },
        "National Security": {
