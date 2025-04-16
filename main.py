import streamlit as st
from pyvis.network import Network
import networkx as nx
import streamlit.components.v1 as components

st.set_page_config(page_title="Interactive Interdependency Graph", layout="wide")

# First Chart Title
st.title("🧠 Interactive Data Model Interdependency Chart - Chart 1")

# [Your existing first chart code remains the same until the divider]

# Add divider
st.markdown("---")

# Second Chart Title
st.title("🧠 Interactive Data Model Interdependency Chart - Chart 2")

# Define entity modules and colors for second chart
entities_2 = {
    "Ministry Family": "blue",
    "Agency": "blue",
    "System Overview": "teal",
    "Criticality Assessment": "teal",
    "Policy": "red",
    "Policy Waivers": "red",
    "Supplier Profile": "purple",
    "Supplier Risk Management": "purple",
    "Supplier Contracts": "purple",
    "Actions Against Errant Supplier": "purple",
    "Supplier Performance Feedback": "purple",
    "Bulk Tender ECN Details": "purple",
    "EDH Agency": "purple",
    "Risk Assessments": "orange",
    "Risk Treatments": "orange",
    "Audit Findings": "gray",
    "System Management": "green",
    "Security & Sensitivity Classification": "green",
    "Risk Materiality Level": "green",
    "System Resiliency": "green",
    "Hosting and System Dependencies": "green",
    "Central Programmes": "green"
}

# Define edges for second chart
edges_2 = [
    ("Agency", "System Overview", "FK: Agency_ID", "both"),
    ("Agency", "Ministry Family", "FK: Ministry_ID", "both"),
    ("System Overview", "Criticality Assessment", "FK: System_ID", "both"),
    ("System Overview", "Policy", "FK: Policy_ID", "both"),
    ("Policy", "Policy Waivers", "FK: Policy_ID", "both"),
    ("Supplier Profile", "Supplier Risk Management", "FK: Supplier_ID", "both"),
    ("Supplier Profile", "Supplier Contracts", "FK: Supplier_ID", "both"),
    ("Supplier Profile", "Actions Against Errant Supplier", "FK: Supplier_ID", "both"),
    ("Supplier Profile", "Supplier Performance Feedback", "FK: Supplier_ID", "both"),
    ("Supplier Profile", "Bulk Tender ECN Details", "FK: Supplier_ID", "both"),
    ("Supplier Profile", "EDH Agency", "FK: Supplier_ID", "both"),
    ("Risk Assessments", "Risk Treatments", "FK: Assessment_ID", "both"),
    ("Audit Findings", "Risk Treatments", "FK: Finding_ID", "both"),
    ("Supplier Risk Management", "Risk Assessments", "FK: Risk_ID", "both"),
    ("Supplier Performance Feedback", "Supplier Risk Management", "FK: Feedback_ID", "both"),
    ("Actions Against Errant Supplier", "Supplier Contracts", "FK: Action_ID", "both"),
    ("System Overview", "Supplier Contracts", "FK: System_ID", "both"),
    ("System Overview", "Audit Findings", "FK: System_ID", "both"),
    ("System Management", "System Overview", "FK: System_ID", "both"),
    ("System Management", "Criticality Assessment", "FK: System_ID", "both"),
    ("System Management", "Security & Sensitivity Classification", "FK: System_ID", "both"),
    ("System Management", "Risk Materiality Level", "FK: System_ID", "both"),
    ("System Management", "System Resiliency", "FK: System_ID", "both"),
    ("System Management", "Hosting and System Dependencies", "FK: System_ID", "both"),
    ("System Management", "Central Programmes", "FK: System_ID", "both"),
    ("System Management", "Supplier Contracts", "FK: System_ID", "both"),
    ("Supplier Contracts", "Hosting and System Dependencies", "FK: Contract_ID", "both")
]

# Create NetworkX graph for second chart
G2 = nx.DiGraph()
for node, color in entities_2.items():
    G2.add_node(node, title=node, color=color)

# Add edges for second chart
for source, target, label, direction in edges_2:
    G2.add_edge(source, target, title=label, label=label, arrows=direction)

# Create interactive PyVis network for second chart
net2 = Network(height="700px", width="100%", directed=True)
net2.from_nx(G2)

# Customize edge labels and arrows for second chart
for edge in net2.edges:
    edge["label"] = edge["title"]
    if edge["arrows"] == "both":
        edge["arrows"] = "to,from"
    else:
        edge["arrows"] = edge["arrows"]

# Save and display second chart
net2.save_graph("graph2.html")
components.html(open("graph2.html", "r", encoding='utf-8').read(), height=750, scrolling=True)
