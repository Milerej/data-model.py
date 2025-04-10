# main.py

import streamlit as st
from pyvis.network import Network
import networkx as nx
import streamlit.components.v1 as components

st.set_page_config(page_title="Interactive Dependency Lineage", layout="wide")
st.title("🧠 Interactive Data Model Lineage Viewer")

# Define nodes with colors
entities = {
    "Ministry": "blue",
    "Family": "blue",
    "Agency": "blue",
    "System Overview": "teal",
    "Criticality Assessment": "teal",
    "Policy": "red",
    "Policy Waivers": "red",
    "Industry Waiver": "red",
    "Supplier Profile": "purple",
    "Supplier Risk Management": "purple",
    "Supplier Contracts": "purple",
    "Actions Against Errant Supplier": "purple",
    "Supplier Performance Feedback": "purple",
    "Bulk Tender ECN Details": "purple",
    "EDH Agency": "purple",
    "Risk Assessments": "orange",
    "Risk Treatments": "orange",
    "Audit Findings": "gray"
}

# Define edges
edges = [
    ("Agency", "System Overview"),
    ("System Overview", "Criticality Assessment"),
    ("Policy", "Policy Waivers"),
    ("Policy", "Industry Waiver"),
    ("Supplier Profile", "Supplier Risk Management"),
    ("Supplier Profile", "Supplier Contracts"),
    ("Supplier Profile", "Actions Against Errant Supplier"),
    ("Supplier Profile", "Supplier Performance Feedback"),
    ("Supplier Profile", "Bulk Tender ECN Details"),
    ("Supplier Profile", "EDH Agency"),
    ("Risk Assessments", "Risk Treatments"),
    ("Audit Findings", "Risk Treatments"),
    ("Supplier Risk Management", "Risk Assessments"),
    ("Supplier Performance Feedback", "Supplier Risk Management"),
    ("Actions Against Errant Supplier", "Supplier Contracts"),
    ("System Overview", "Supplier Contracts")
]

# Full graph
full_graph = nx.DiGraph()
for node, color in entities.items():
    full_graph.add_node(node, title=node, color=color)
full_graph.add_edges_from(edges)

# Node selector
selected_node = st.selectbox("🔍 Select a Node to Show Lineage:", sorted(full_graph.nodes))

# Traverse: Get all reachable descendants from the selected node
descendants = nx.descendants(full_graph, selected_node)
ancestors = nx.ancestors(full_graph, selected_node)

# Include the selected node itself
lineage_nodes = descendants.union(ancestors).union({selected_node})
lineage_subgraph = full_graph.subgraph(lineage_nodes)

# Render with PyVis
net = Network(height="700px", width="100%", directed=True)
net.from_nx(lineage_subgraph)
net.repulsion(node_distance=200, central_gravity=0.3)

net.save_graph("graph.html")
components.html(open("graph.html", "r", encoding='utf-8').read(), height=750, scrolling=True)
