import streamlit as st
from pyvis.network import Network
import networkx as nx
import streamlit.components.v1 as components
import html

# This MUST be the first Streamlit command
st.set_page_config(page_title="Interactive Interdependency Graph", layout="wide")

st.title("🧠 Interactive Data Model Interdependency Chart")

# Define entity modules with fields and relationships
entities = {
    "Ministry Family": {
        "color": "blue",
        "fields": [
            {"name": "Ministry_ID", "is_key": True},
            {"name": "Ministry_Name", "is_key": False},
            {"name": "Description", "is_key": False}
        ],
        "type": "Entity"
    },
    "Agency": {
        "color": "blue",
        "fields": [
            {"name": "Agency_ID", "is_key": True},
            {"name": "Agency_Name", "is_key": False},
            {"name": "Ministry_ID", "is_foreign_key": True, "references": "Ministry Family"},
            {"name": "Status", "is_key": False}
        ],
        "type": "Entity"
    },
    "System Overview": {
        "color": "teal",
        "fields": [
            {"name": "System_ID", "is_key": True},
            {"name": "System_Name", "is_key": False},
            {"name": "Agency_ID", "is_foreign_key": True, "references": "Agency"},
            {"name": "Description", "is_key": False}
        ],
        "type": "Entity"
    },
    "Criticality Assessment": {
        "color": "teal",
        "fields": [
            {"name": "Assessment_ID", "is_key": True},
            {"name": "System_ID", "is_foreign_key": True, "references": "System Overview"}
        ],
        "type": "Entity"
    },
    "Policy": {
        "color": "red",
        "fields": [
            {"name": "Policy_ID", "is_key": True}
        ],
        "type": "Entity"
    },
    "Policy Waivers": {
        "color": "red",
        "fields": [
            {"name": "Waiver_ID", "is_key": True},
            {"name": "Policy_ID", "is_foreign_key": True, "references": "Policy"}
        ],
        "type": "Entity"
    },
    "Supplier Profile": {
        "color": "purple",
        "fields": [
            {"name": "Supplier_ID", "is_key": True}
        ],
        "type": "Entity"
    },
    "Supplier Risk Management": {
        "color": "purple",
        "fields": [
            {"name": "Risk_ID", "is_key": True},
            {"name": "Supplier_ID", "is_foreign_key": True, "references": "Supplier Profile"}
        ],
        "type": "Entity"
    },
    "Supplier Contracts": {
        "color": "purple",
        "fields": [
            {"name": "Contract_ID", "is_key": True},
            {"name": "Supplier_ID", "is_foreign_key": True, "references": "Supplier Profile"}
        ],
        "type": "Entity"
    },
    "Actions Against Errant Supplier": {
        "color": "purple",
        "fields": [
            {"name": "Action_ID", "is_key": True},
            {"name": "Supplier_ID", "is_foreign_key": True, "references": "Supplier Profile"}
        ],
        "type": "Entity"
    },
    "Supplier Performance Feedback": {
        "color": "purple",
        "fields": [
            {"name": "Feedback_ID", "is_key": True},
            {"name": "Supplier_ID", "is_foreign_key": True, "references": "Supplier Profile"}
        ],
        "type": "Entity"
    },
    "Bulk Tender ECN Details": {
        "color": "purple",
        "fields": [
            {"name": "ECN_ID", "is_key": True},
            {"name": "Supplier_ID", "is_foreign_key": True, "references": "Supplier Profile"}
        ],
        "type": "Entity"
    },
    "EDH Agency": {
        "color": "purple",
        "fields": [
            {"name": "EDH_ID", "is_key": True}
        ],
        "type": "Entity"
    },
    "Risk Assessments": {
        "color": "orange",
        "fields": [
            {"name": "Assessment_ID", "is_key": True}
        ],
        "type": "Entity"
    },
    "Risk Treatments": {
        "color": "orange",
        "fields": [
            {"name": "Treatment_ID", "is_key": True},
            {"name": "Assessment_ID", "is_foreign_key": True, "references": "Risk Assessments"}
        ],
        "type": "Entity"
    },
    "Audit Findings": {
        "color": "gray",
        "fields": [
            {"name": "Finding_ID", "is_key": True}
        ],
        "type": "Entity"
    },
    "System Management": {
        "color": "green",
        "fields": [
            {"name": "Management_ID", "is_key": True},
            {"name": "System_ID", "is_foreign_key": True, "references": "System Overview"}
        ],
        "type": "Entity"
    },
    "Security & Sensitivity Classification": {
        "color": "green",
        "fields": [
            {"name": "Classification_ID", "is_key": True}
        ],
        "type": "Entity"
    },
    "Risk Materiality Level": {
        "color": "green",
        "fields": [
            {"name": "Materiality_ID", "is_key": True}
        ],
        "type": "Entity"
    },
    "System Resiliency": {
        "color": "green",
        "fields": [
            {"name": "Resiliency_ID", "is_key": True}
        ],
        "type": "Entity"
    },
    "Hosting and System Dependencies": {
        "color": "green",
        "fields": [
            {"name": "Dependency_ID", "is_key": True}
        ],
        "type": "Entity"
    },
    "Central Programmes": {
        "color": "green",
        "fields": [
            {"name": "Programme_ID", "is_key": True}
        ],
        "type": "Entity"
    }
}

# Define edges with labels for relationships - organized by domain
edges = [
    # Ministry and Agency relationships
    ("Agency", "Ministry Family", 
     "FK: Agency.Ministry_ID → Ministry_Family.Ministry_ID"),
    
    # System Overview relationships
    ("System Overview", "Agency", 
     "FK: System_Overview.Agency_ID → Agency.Agency_ID"),
    ("Criticality Assessment", "System Overview", 
     "FK: Criticality_Assessment.System_ID → System_Overview.System_ID"),
    
    # Policy relationships
    ("Policy Waivers", "Policy", 
     "FK: Policy_Waivers.Policy_ID → Policy.Policy_ID"),
    
    # Supplier relationships
    ("Supplier Risk Management", "Supplier Profile", 
     "FK: Supplier_Risk_Management.Supplier_ID → Supplier_Profile.Supplier_ID"),
    ("Supplier Contracts", "Supplier Profile", 
     "FK: Supplier_Contracts.Supplier_ID → Supplier_Profile.Supplier_ID"),
    ("Actions Against Errant Supplier", "Supplier Profile", 
     "FK: Actions_Against_Errant_Supplier.Supplier_ID → Supplier_Profile.Supplier_ID"),
    ("Supplier Performance Feedback", "Supplier Profile", 
     "FK: Supplier_Performance_Feedback.Supplier_ID → Supplier_Profile.Supplier_ID"),
    ("Bulk Tender ECN Details", "Supplier Profile", 
     "FK: Bulk_Tender_ECN_Details.Supplier_ID → Supplier_Profile.Supplier_ID"),
    
    # Risk Management relationships
    ("Risk Treatments", "Risk Assessments", 
     "FK: Risk_Treatments.Assessment_ID → Risk_Assessments.Assessment_ID"),
    
    # System Management relationships
    ("System Management", "System Overview", 
     "FK: System_Management.System_ID → System_Overview.System_ID"),
    ("Security & Sensitivity Classification", "System Overview", 
     "FK: Security_Classification.System_ID → System_Overview.System_ID"),
    ("Risk Materiality Level", "System Overview", 
     "FK: Risk_Materiality.System_ID → System_Overview.System_ID"),
    ("System Resiliency", "System Overview", 
     "FK: System_Resiliency.System_ID → System_
