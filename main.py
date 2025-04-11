import streamlit as st
from pyvis.network import Network
import networkx as nx
import streamlit.components.v1 as components
import tempfile
import os

st.set_page_config(page_title="Interactive Interdependency Graph", layout="wide")

st.title("🧠 Interactive System Management Data Model")

# Define entity modules and colors
entities = {
    "System Management": {"color": "green", "size": 30, "shape": "dot"},
    "System Overview": {
        "color": "white",
        "size": 40, 
        "shape": "box",
        "margin": 20,
        "widthConstraint": {
            "minimum": 200,
            "maximum": 200
        },
        "label": "\n".join([
            "SYSTEM OVERVIEW",
            "─────────────",
            "Agency",
            "Ministry Family",
            "System ID (Primary Key)",
            "System Name",
            "System Description",
            "System Status"
        ])
    },
    "Criticality Assessment": {
        "color": "white",
        "size": 40, 
        "shape": "box",
        "margin": 20,
        "widthConstraint": {
            "minimum": 200,
            "maximum": 200
        },
        "label": "\n".join([
            "CRITICALITY ASSESSMENT",
            "─────────────",
            "Economy",
            "Public Health and Safety",
            "National Security",
            "Social Preparedness",
            "Public Service",
            "Designated CII under the Cybersecurity Act",
            "System Criticality (System Auto-generated)"
        ])
    },
    "Security & Sensitivity Classification": {"color": "green", "size": 20, "shape": "dot"},
    "Risk Materiality Level": {"color": "green", "size": 20, "shape": "dot"},
    "System Resiliency": {"color": "green", "size": 20, "shape": "dot"},
    "Hosting and System Dependencies": {"color": "green", "size": 20, "shape": "dot"},
    "Central Programmes": {"color": "green", "size": 20, "shape": "dot"}
}

# Define edges with PK/FK relationships
edges = [
    ("System Management", "System Overview", "PK: System_ID", "both"),
    ("System Management", "Criticality Assessment", "PK: System_ID", "both"),
    ("System Management", "Security & Sensitivity Classification", "PK: System_ID", "both"),
    ("System Management", "Risk Materiality Level", "PK: System_ID", "both"),
    ("System Management", "System Resiliency", "PK: System_ID", "both"),
    ("System Management", "Hosting and System Dependencies", "PK: System_ID", "both"),
    ("System Management", "Central Programmes", "PK: System_ID", "both"),
    ("Criticality Assessment", "Risk Materiality Level", "PK: System_ID", "both"),
    ("Hosting and System Dependencies", "Risk Materiality Level", "PK: System_ID", "both"),
    ("Security & Sensitivity Classification", "Risk Materiality Level", "PK: System_ID", "both")
]

# Create NetworkX graph
G = nx.DiGraph()
for node, attributes in entities.items():
    node_attrs = {
        "color": attributes["color"],
        "size": attributes["size"],
        "shape": attributes["shape"],
        "label": attributes.get("label", node)
    }
    
    # Add additional attributes for boxes
    if "margin" in attributes:
        node_attrs["margin"] = attributes["margin"]
    if "widthConstraint" in attributes:
        node_attrs["widthConstraint"] = attributes["widthConstraint"]
    
    G.add_node(node, **node_attrs)

# Add edges with labels and custom arrow directions
for source, target, label, direction in edges:
    G.add_edge(source, target, title=label, label=label, arrows=direction)

# Create interactive PyVis network
net = Network(height="700px", width="100%", directed=True, notebook=True)
net.from_nx(G)

# Set options as a string
net.set_options('''{
    "physics": {
        "enabled": true,
        "stabilization": {
            "enabled": true,
            "iterations": 1000,
            "updateInterval": 100,
            "onlyDynamicEdges": false,
            "fit": true
        },
        "barnesHut": {
            "gravitationalConstant": -2000,
            "centralGravity": 0.3,
            "springLength": 200,
            "springConstant": 0.04,
            "damping": 0.09,
            
