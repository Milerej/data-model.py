import streamlit as st
from pyvis.network import Network
import networkx as nx
import streamlit.components.v1 as components

st.set_page_config(page_title="Interactive Interdependency Graph", layout="wide")

st.title("🧠 Data Model Interdependency Chart")

# Define entity modules and colors
entities = {
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

# Define edges with labels for relationships and directions
edges = [
    ("Agency", "System Overview", "FK: Agency_ID", "both"),
    ("Agency", "Ministry Family", "FK: Ministry_ID", "to"),
    ("System Overview", "Criticality Assessment", "FK: System_ID", "both"),
    ("System Overview", "Policy", "FK: Policy_ID", "to"),
    ("Policy", "Policy Waivers", "FK: Policy_ID", "to"),
    ("Supplier Profile", "Supplier Risk Management", "FK: Supplier_ID", "both"),
    ("Supplier Profile", "Supplier Contracts", "FK: Supplier_ID", "both"),
    ("Supplier Profile", "Actions Against Errant Supplier", "FK: Supplier_ID", "both"),
    ("Supplier Profile", "Supplier Performance Feedback", "FK: Supplier_ID", "both"),
    ("Supplier Profile", "Bulk Tender ECN Details", "FK: Supplier_ID", "both"),
    ("Supplier Profile", "EDH Agency", "FK: Supplier_ID", "both"),
    ("Risk Assessments", "Risk Treatments", "FK: Assessment_ID", "both"),
    ("Audit Findings", "Risk Treatments", "FK: Assessment_ID", "to"),
    ("Supplier Risk Management", "Risk Assessments", "FK: Risk_ID", "to"),
    ("Supplier Performance Feedback", "Supplier Risk Management", "FK: Risk_ID", "to"),
    ("Actions Against Errant Supplier", "Supplier Contracts", "FK: Contract_ID", "to"),
    ("System Overview", "Supplier Contracts", "FK: System_ID", "both"),
    ("System Overview", "Audit Findings", "FK: System_ID", "both"),
    # System Management relationships
    ("System Management", "System Overview", "FK: System_ID", "both"),
    ("System Management", "Criticality Assessment", "FK: Assessment_ID", "both"),
    ("System Management", "Security & Sensitivity Classification", "FK: System_ID", "both"),
    ("System Management", "Risk Materiality Level", "FK: System_ID", "both"),
    ("System Management", "System Resiliency", "FK: System_ID", "both"),
    ("System Management", "Hosting and System Dependencies", "FK: System_ID", "both"),
    ("System Management", "Central Programmes", "FK: System_ID", "both"),
    ("System Management", "Supplier Contracts", "FK: System_ID", "both"),
    ("Supplier Contracts", "Hosting and System Dependencies", "FK: System_ID", "both")
]

# Create NetworkX graph
G = nx.DiGraph()
for node, color in entities.items():
    G.add_node(node, title=node, color=color)

# Add edges with labels and custom arrow directions
for source, target, label, direction in edges:
    G.add_edge(source, target, title=label, label=label, arrows=direction)

# Create interactive PyVis network
net = Network(height="700px", width="100%", directed=True)
net.from_nx(G)
net.repulsion(node_distance=200, central_gravity=0.3)

# Customize edge labels and arrows
for edge in net.edges:
    edge["label"] = edge["title"]
    if edge["arrows"] == "both":
        edge["arrows"] = "to,from"
    else:
        edge["arrows"] = edge["arrows"]

# Save and display in Streamlit
net.save_graph("graph.html")
components.html(open("graph.html", "r", encoding='utf-8').read(), height=750, scrolling=True)
