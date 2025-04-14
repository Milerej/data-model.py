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
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True

if check_password():
    st.set_page_config(
        page_title="Interactive Interdependency Graph",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Add maximized layout CSS
    st.markdown("""
        <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            .stApp > header {display: none;}
            .main > .block-container {
                padding-top: 0;
                padding-bottom: 0;
                max-width: 100%;
            }
            .element-container iframe {
                width: 100vw !important;
                height: 100vh !important;
                position: fixed !important;
                top: 0 !important;
                left: 0 !important;
                z-index: 99 !important;
            }
            .fullscreen-button {
                position: fixed;
                top: 10px;
                right: 10px;
                z-index: 1000;
                padding: 10px;
                background: #2E7D32;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            .fullscreen-button:hover {
                background: #1B5E20;
            }
        </style>
    """, unsafe_allow_html=True)

    st.title("⚙️ Data Model : System Management")

    # Define entity modules and colors
    entities = {
        "System Management": {
            "color": "#2E7D32", 
            "size": 35, 
            "shape": "dot",
            "title": "System Management Module"
        },
        # Main Modules
        "System Overview": {
            "color": "#4CAF50", 
            "size": 25, 
            "shape": "dot",
            "title": "System Overview Sub-Module"
        },
        "Criticality Assessment": {
            "color": "#4CAF50", 
            "size": 25,
            "shape": "dot",
            "title": "Criticality Assessment Sub-Module"
        },
        "Security & Sensitivity Classification": {
            "color": "#4CAF50", 
            "size": 25, 
            "shape": "dot",
            "title": "Security & Sensitivity Classification Sub-Module"
        },
        "Risk Materiality Level": {
            "color": "#4CAF50", 
            "size": 25, 
            "shape": "dot",
            "title": "Risk Materiality Level Sub-Module"
        },
        "System Resiliency": {
            "color": "#4CAF50", 
            "size": 25, 
            "shape": "dot",
            "title": "System Resiliency Sub-Module"
        },
        "Hosting and System Dependencies": {
            "color": "#4CAF50", 
            "size": 25, 
            "shape": "dot",
            "title": "Hosting and System Dependencies Sub-Module"
        },

            # System Overview Fields
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

        # Criticality Assessment Fields
        "Economy": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Economy impact field"
        },
        "Public Health and Safety": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Public Health and Safety field"
        },
        "National Security": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "National Security field"
        },
        "Social Preparedness": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Social Preparedness field"
        },
        "Public Service": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Public Service field"
        },
        "Designated CII": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Designated CII under Cybersecurity Act"
        },
        "System Criticality": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "System Criticality (Auto-generated)"
        },
        "IDSC Approval Date": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "IDSC's Approval Date (CA)"
        },
        "IDSC Approval Attachment": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "IDSC's Approval Attachment (CA)"
        },
        "MHA Approval": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Approved by MHA?"
        },
        "CSA Approval": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Approved by CSA?"
        },
        "SNDGO Approval": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Approved by SNDGO?"
        },
        "MHA Comments": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "MHA Comments"
        },
        "CSA Comments": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "CSA Comments"
        },
        "SNDGO Comments": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "SNDGO Comments"
        },

        # Security & Sensitivity Classification Fields
        "Security Classification": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Security Classification field"
        },
        "Sensitivity Classification": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Sensitivity Classification field"
        },

        # Risk Materiality Level Fields
        "Computed RML": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Computed Risk Materiality Level"
        },
        "Computed RML Date": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Computed RML Date"
        },
        "Agency Proposed RML": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Agency Proposed Risk Materiality Level"
        },
        "RML Alignment": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "In line with Computed RML?"
        },
        "RML Justification": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Justification if not in line"
        },
        "Endorsed RML": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Endorsed Risk Materiality Level"
        },
        "RML Endorsement Date": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Date Endorsed"
        },
        "Endorsement Comments": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Endorsed Comments"
        },

        # System Resiliency Fields
        "Service Availability": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Service Availability"
        },
        "RTO": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Recovery Time Objective"
        },
        "RPO": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Recovery Point Objective"
        },

        # Hosting and System Dependencies Fields
        "Total Dependencies": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Total Downstream Dependencies"
        },
        "Downstream Impact": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Sub-System Downstream Impact"
        },
        "Direct Dependencies Count": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Count of Direct Dependencies"
        },
        "Dependency ID": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Dependency ID"
        },
        "Dependency Status": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Dependency Status"
        },
        "Dependency Type": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Type of Dependency"
        },
        "Upstream System": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Dependent Sub-System Upstream"
        },
        "Dependent System": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Dependent System/Service Name"
        },
        "Data Exchange Frequency": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Frequency of Data Exchange"
        },
        "Inferred Dependencies": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Count of Inferred Dependencies"
        }
    }
