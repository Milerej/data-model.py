import streamlit as st
from pyvis.network import Network
import networkx as nx
import streamlit.components.v1 as components

st.set_page_config(page_title="Interactive Interdependency Graph", layout="wide")

st.title("🧠🧠🧠 Interactive Data Model Interdependency Chart")

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

# Define edges with labels for relationships
edges = [
    ("Agency", "System Overview", "relates to"),
    ("Agency", "Ministry Family", "manages"),
    ("System Overview", "Criticality Assessment", "supports"),
    ("System Overview", "Policy", "defines"),
    ("Policy", "Policy Waivers", "grants"),
    ("Supplier Profile", "Supplier Risk Management", "informs"),
    ("Supplier Profile", "Supplier Contracts", "oversees"),
    ("Supplier Profile", "Actions Against Errant Supplier", "initiates"),
    ("Supplier Profile", "Supplier Performance Feedback", "monitors"),
    ("Supplier Profile", "Bulk Tender ECN Details", "includes"),
    ("Supplier Profile", "EDH Agency", "collaborates with"),
    ("Risk Assessments", "Risk Treatments", "leads to"),
    ("Audit Findings", "Risk Treatments", "triggers"),
    ("Supplier Risk Management", "Risk Assessments", "feeds into"),
    ("Supplier Performance Feedback", "Supplier Risk Management", "affects"),
    ("Actions Against Errant Supplier", "Supplier Contracts", "cancels"),
    ("System Overview", "Supplier Contracts", "references"),
    ("System Overview", "Audit Findings", "monitors"),
    # New edges for System Management
    ("System Management", "System Overview", "manages"),
    ("System Management", "Criticality Assessment", "supports"),
    ("System Management", "Security & Sensitivity Classification", "evaluates"),
    ("System Management", "Risk Materiality Level", "determines"),
    ("System Management", "System Resiliency", "improves"),
    ("System Management", "Hosting and System Dependencies", "depends on"),
    ("System Management", "Central Programmes", "aligns with"),
    ("System Management", "Supplier Contracts", "depends on"),
    ("Supplier Contracts", "Hosting and System Dependencies", "depends on")
]

# Create NetworkX graph
G = nx.DiGraph()
for node, color in entities.items():
    G.add_node(node, title=node, color=color)

# Add edges with labels
for source, target, label in edges:
    G.add_edge(source, target, title=label, label=label)

# Create interactive PyVis network
net = Network(height="700px", width="100%", directed=True)
net.from_nx(G)
net.repulsion(node_distance=200, central_gravity=0.3)

# Customize edge labels
for edge in net.edges:
    edge["label"] = edge["title"]

# Save and display in Streamlit
net.save_graph("graph.html")
components.html(open("graph.html", "r", encoding='utf-8').read(), height=750, scrolling=True)

import streamlit as st
from pyvis.network import Network
import networkx as nx
import streamlit.components.v1 as components

st.set_page_config(page_title="Interactive Interdependency Graph", layout="wide")

st.title("🧠🧠 Interactive Data Model Interdependency Chart")

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

# Define edges with labels for relationships
edges = [
    ("Agency", "System Overview", "relates to"),
    ("Agency", "Ministry Family", "manages"),
    ("System Overview", "Criticality Assessment", "supports"),
    ("System Overview", "Policy", "defines"),
    ("Policy", "Policy Waivers", "grants"),
    ("Supplier Profile", "Supplier Risk Management", "informs"),
    ("Supplier Profile", "Supplier Contracts", "oversees"),
    ("Supplier Profile", "Actions Against Errant Supplier", "initiates"),
    ("Supplier Profile", "Supplier Performance Feedback", "monitors"),
    ("Supplier Profile", "Bulk Tender ECN Details", "includes"),
    ("Supplier Profile", "EDH Agency", "collaborates with"),
    ("Risk Assessments", "Risk Treatments", "leads to"),
    ("Audit Findings", "Risk Treatments", "triggers"),
    ("Supplier Risk Management", "Risk Assessments", "feeds into"),
    ("Supplier Performance Feedback", "Supplier Risk Management", "affects"),
    ("Actions Against Errant Supplier", "Supplier Contracts", "cancels"),
    ("System Overview", "Supplier Contracts", "references"),
    ("System Overview", "Audit Findings", "monitors"),
    # New edges for System Management
    ("System Management", "System Overview", "manages"),
    ("System Management", "Criticality Assessment", "supports"),
    ("System Management", "Security & Sensitivity Classification", "evaluates"),
    ("System Management", "Risk Materiality Level", "determines"),
    ("System Management", "System Resiliency", "improves"),
    ("System Management", "Hosting and System Dependencies", "depends on"),
    ("System Management", "Central Programmes", "aligns with"),
    ("System Management", "Supplier Contracts", "depends on"),
    ("Supplier Contracts", "Hosting and System Dependencies", "depends on")
]

# Create NetworkX graph
G = nx.DiGraph()
for node, color in entities.items():
    G.add_node(node, title=node, color=color)

# Add edges with labels
for source, target, label in edges:
    G.add_edge(source, target, title=label, label=label)

# Create interactive PyVis network
net = Network(height="700px", width="100%", directed=True)
net.from_nx(G)
net.repulsion(node_distance=200, central_gravity=0.3)

# Customize edge labels
for edge in net.edges:
    edge["label"] = edge["title"]

# Save and display in Streamlit
net.save_graph("graph.html")
components.html(open("graph.html", "r", encoding='utf-8').read(), height=750, scrolling=True)
