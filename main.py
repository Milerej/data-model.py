import streamlit as st
from pyvis.network import Network
import networkx as nx
import streamlit.components.v1 as components

st.set_page_config(page_title="Interactive Interdependency Graph", layout="wide")

st.title("🧠 Interactive Data Model Interdependency Chart")

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
    # New nodes
    "System Management": "green",
    "Security & Sensitivity Classification": "green",
    "Risk Materiality Level": "green",
    "System Resiliency": "green",
    "Hosting and System Dependencies": "green",
    "Central Programmes": "green"
}

# Define edges with labels for relationships - organized by domain
edges = [
    # Ministry and Agency relationships (one-way)
    ("Agency", "Ministry Family", "FK: Ministry_ID", "to"),
    
    # System Overview relationships (one-way)
    ("System Overview", "Agency", "FK: Agency_ID", "to"),
    ("Criticality Assessment", "System Overview", "FK: System_ID", "to"),
    
    # Policy relationships (one-way)
    ("Policy Waivers", "Policy", "FK: Policy_ID", "to"),
    
    # Supplier relationships (bidirectional)
    ("Supplier Risk Management", "Supplier Profile", "FK: Supplier_ID", "both"),
    ("Supplier Contracts", "Supplier Profile", "FK: Supplier_ID", "both"),
    ("Actions Against Errant Supplier", "Supplier Profile", "FK: Supplier_ID", "both"),
    ("Supplier Performance Feedback", "Supplier Profile", "FK: Supplier_ID", "both"),
    ("Bulk Tender ECN Details", "Supplier Profile", "FK: Supplier_ID", "both"),
    
    # Risk Management relationships (bidirectional)
    ("Risk Treatments", "Risk Assessments", "FK: Assessment_ID", "both"),
    
    # System Management relationships (bidirectional)
    ("System Management", "System Overview", "FK: System_ID", "both"),
    ("Security & Sensitivity Classification", "System Overview", "FK: System_ID", "both"),
    ("Risk Materiality Level", "System Overview", "FK: System_ID", "both"),
    ("System Resiliency", "System Overview", "FK: System_ID", "both"),
    ("Hosting and System Dependencies", "System Overview", "FK: System_ID", "both"),
    ("Central Programmes", "System Overview", "FK: System_ID", "both"),
    
    # Cross-domain relationships (one-way)
    ("Supplier Contracts", "System Overview", "FK: System_ID", "to"),
    ("Audit Findings", "System Overview", "FK: System_ID", "to")
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


st.title("🧠🧠 Viz - Mock Up Data")  # Fixed the missing parenthesis

# Define edges with labels for relationships and directions
edges = [
    ("Agency", "System Overview", "relates to", "both"),
    ("Agency", "Ministry Family", "manages", "to"),
    ("System Overview", "Criticality Assessment", "supports", "both"),
    ("System Overview", "Policy", "defines", "to"),
    ("Policy", "Policy Waivers", "grants", "to"),
    ("Supplier Profile", "Supplier Risk Management", "informs", "both"),
    ("Supplier Profile", "Supplier Contracts", "oversees", "both"),
    ("Supplier Profile", "Actions Against Errant Supplier", "initiates", "both"),
    ("Supplier Profile", "Supplier Performance Feedback", "monitors", "both"),
    ("Supplier Profile", "Bulk Tender ECN Details", "includes", "both"),
    ("Supplier Profile", "EDH Agency", "collaborates with", "both"),
    ("Risk Assessments", "Risk Treatments", "leads to", "both"),
    ("Audit Findings", "Risk Treatments", "triggers", "to"),
    ("Supplier Risk Management", "Risk Assessments", "feeds into", "to"),
    ("Supplier Performance Feedback", "Supplier Risk Management", "affects", "to"),
    ("Actions Against Errant Supplier", "Supplier Contracts", "cancels", "to"),
    ("System Overview", "Supplier Contracts", "references", "both"),
    ("System Overview", "Audit Findings", "monitors", "both"),
    # New edges for System Management
    ("System Management", "System Overview", "manages", "both"),
    ("System Management", "Criticality Assessment", "supports", "both"),
    ("System Management", "Security & Sensitivity Classification", "evaluates", "both"),
    ("System Management", "Risk Materiality Level", "determines", "both"),
    ("System Management", "System Resiliency", "improves", "both"),
    ("System Management", "Hosting and System Dependencies", "depends on", "both"),
    ("System Management", "Central Programmes", "aligns with", "both"),
    ("System Management", "Supplier Contracts", "depends on", "both"),
    ("Supplier Contracts", "Hosting and System Dependencies", "depends on", "both")
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
