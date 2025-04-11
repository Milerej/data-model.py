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
    "System Management": "green",
    "Security & Sensitivity Classification": "green",
    "Risk Materiality Level": "green",
    "System Resiliency": "green",
    "Hosting and System Dependencies": "green",
    "Central Programmes": "green"
}

# Network visualization options
network_options = """
const options = {
    "nodes": {
        "font": {
            "size": 12
        }
    },
    "edges": {
        "color": {
            "inherit": true
        },
        "smooth": {
            "enabled": false
        }
    },
    "interaction": {
        "hover": true,
        "hoverConnectedEdges": true,
        "selectConnectedEdges": true
    },
    "physics": {
        "enabled": true,
        "forceAtlas2Based": {
            "gravitationalConstant": -26,
            "centralGravity": 0.005,
            "springLength": 230,
            "springConstant": 0.18
        },
        "maxVelocity": 146,
        "solver": "forceAtlas2Based",
        "timestep": 0.35,
        "stabilization": {
            "enabled": true,
            "iterations": 1000,
            "updateInterval": 25
        }
    }
}
"""

# First visualization
edges = [
    # Ministry and Agency relationships (one-way)
    ("Agency", "Ministry Family", "FK: Ministry_ID", "to"),
    # ... (rest of your first edges list)
]

# Create first NetworkX graph
G = nx.DiGraph()
for node, color in entities.items():
    G.add_node(node, title=node, color=color)

for source, target, label, direction in edges:
    G.add_edge(source, target, title=label, label=label, arrows=direction)

# Create first interactive PyVis network
net = Network(height="700px", width="100%", directed=True)
net.from_nx(G)
net.repulsion(node_distance=200, central_gravity=0.3)
net.toggle_hide_edges_on_drag(True)
net.toggle_physics(False)
net.set_options(network_options)

for edge in net.edges:
    edge["label"] = edge["title"]
    if edge["arrows"] == "both":
        edge["arrows"] = "to,from"
    else:
        edge["arrows"] = edge["arrows"]

net.save_graph("graph1.html")
components.html(open("graph1.html", "r", encoding='utf-8').read(), height=750, scrolling=True)

# Second visualization
st.title("🧠🧠 Viz - Mock Up Data")

edges = [
    ("Agency", "System Overview", "relates to", "both"),
    # ... (rest of your second edges list)
]

# Create second NetworkX graph
G = nx.DiGraph()
for node, color in entities.items():
    G.add_node(node, title=node, color=color)

for source, target, label, direction in edges:
    G.add_edge(source, target, title=label, label=label, arrows=direction)

# Create second interactive PyVis network
net = Network(height="700px", width="100%", directed=True)
net.from_nx(G)
net.repulsion(node_distance=200, central_gravity=0.3)
net.toggle_hide_edges_on_drag(True)
net.toggle_physics(False)
net.set_options(network_options)

for edge in net.edges:
    edge["label"] = edge["title"]
    if edge["arrows"] == "both":
        edge["arrows"] = "to,from"
    else:
        edge["arrows"] = edge["arrows"]

net.save_graph("graph2.html")
components.html(open("graph2.html", "r", encoding='utf-8').read(), height=750, scrolling=True)
