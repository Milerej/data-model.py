import streamlit as st
# Must be the first Streamlit command
st.set_page_config(page_title="System Impact Analysis", layout="wide")

from pyvis.network import Network
import networkx as nx
import streamlit.components.v1 as components
import tempfile
import os
import random
from datetime import datetime, timedelta
import pandas as pd

# Initialize session state for password check
if 'password_correct' not in st.session_state:
    st.session_state.password_correct = False

def generate_random_date(start_year=2015):
    start_date = datetime(start_year, 1, 1)
    end_date = datetime.now()
    days_between_dates = (end_date - start_date).days
    random_number_of_days = random.randrange(days_between_dates)
    return (start_date + timedelta(days=random_number_of_days)).strftime("%Y-%m-%d")

def generate_system_data(system_number):
    agencies = ["Agency 1", "Agency 2", "Agency 3", "Agency 4", "Agency 5", "Agency 6", "Agency 7", "Agency 8"]
    ministry_families = ["MF 1", "MF 2", "MF 3", "MF 4", "MF 5"]
    security_classifications = ["Official", "Restricted", "Confidential", "Secret"]
    sensitivity_classifications = ["Sensitive Normal", "Non-Sensitive", "Sensitive High"]
    system_criticality = ["Others", "SII", "High"]
    rml_levels = ["Low", "Medium", "High"]
    dependency_types = ["Upstream", "Downstream"]
    
    # Logic to ensure consistent criticality and RML relationships
    chosen_criticality = random.choice(system_criticality)
    
    # Determine RML based on criticality
    if chosen_criticality == "High":
        possible_rml = ["Medium", "High"]
        recommended_rml = "High"
    elif chosen_criticality == "SII":
        possible_rml = ["Medium", "High"]
        recommended_rml = "Medium"
    else:  # Others
        possible_rml = ["Low", "Medium"]
        recommended_rml = "Low"
        
    computed_rml = random.choice(possible_rml)
    agency_proposed_rml = random.choice(possible_rml)
    endorsed_rml = recommended_rml  # Using recommended RML as endorsed RML
    
    # Determine RML alignment
    rml_alignment = "Aligned" if computed_rml == endorsed_rml else "Not Aligned"
    
    return {
        "System Identity & Classification": {
            "System ID": f"SYS{random.randint(1000, 9999)}",
            "System Name": f"System {system_number}",
            "System Description": f"Description for System {system_number}",
            "System Status": random.choice(["Active", "Inactive", "Maintenance"]),
            "Operational Date": generate_random_date(),
            "Decommission Date": generate_random_date(2025),
            "Agency Name": random.choice(agencies),
            "Ministry Family Name": random.choice(ministry_families),
            "Security Classification": random.choice(security_classifications),
            "Sensitivity Classification": random.choice(sensitivity_classifications)
        },
        "Criticality & Risk": {
            "System Criticality": chosen_criticality,
            "Computed RML": computed_rml,
            "Computed RML Date": generate_random_date(),
            "Agency Proposed RML": agency_proposed_rml,
            "RML Alignment": rml_alignment,
            "Endorsed RML": endorsed_rml,
            "RML Endorsement Date": generate_random_date()
        },
        "System Resilience": {
            "Service Availability": f"{random.randint(90, 100)}%",
            "RTO": f"{random.randint(1, 24)} hours",
            "RPO": f"{random.randint(1, 12)} hours"
        },
        "Dependencies": {
            "Dependency Type": random.choice(dependency_types),
            "Dependency Status": random.choice(["Active", "Inactive"])
        }
    }

def check_password():
    """Returns `True` if the user had the correct password."""
    if st.session_state.password_correct:
        return True

    password = st.text_input("Password", type="password")
    if password == "Showmethemoney":
        st.session_state.password_correct = True
        return True
    elif password:
        st.error("⚠️ Password incorrect")
        return False
    return False

# Main app
if check_password():
    st.title("🔄 System Impact Analysis")

    # Initialize session state for systems data if not exists
    if 'systems_data' not in st.session_state:
        st.session_state.systems_data = {
            f"System {i}": generate_system_data(i) for i in range(1, 51)
        }

    # Create network graph
    G = nx.DiGraph()
    
    # Add nodes
    for system_name, system_info in st.session_state.systems_data.items():
        G.add_node(system_name, **system_info)
