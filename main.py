# main.py

import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# Set Streamlit page config
st.set_page_config(page_title="Data Model Interdependency Chart", layout="wide")

st.title("📊 Data Model Interdependency Chart")

# Define entity modules and colors
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

# Define inter-entity relationships
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

# Build the graph
G = nx.DiGraph()
for entity, color in entities.items():
    G.add_node(entity, color=color)

G.add_edges_from(edges)

# Generate colors from node attributes
node_colors = [G.nodes[n]["color"] for n in G.nodes]

# Draw the graph using matplotlib
fig, ax = plt.subplots(figsize=(16, 10))
pos = nx.spring_layout(G, k=0.6, iterations=50, seed=42)
nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=2000,
        font_size=10, edge_color='black', arrows=True, ax=ax)
st.pyplot(fig)
