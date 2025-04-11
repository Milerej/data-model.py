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
        "color": "green", 
        "size": 30, 
        "shape": "dot",
        "details": "\n".join([
            "SYSTEM OVERVIEW FIELDS",
            "─────────────",
            "Agency",
            "Ministry Family",
            "System ID (Primary Key)",
            "System Name",
            "System Description",
            "System Status"
        ])
    },
    "Criticality Assessment": {"color": "green", "size": 20, "shape": "dot"},
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
    if node == "System Overview":
        # Add the main node
        G.add_node(
            node,
            color=attributes["color"],
            size=attributes["size"],
            shape=attributes["shape"],
            label=node
        )
        # Add the details node
        G.add_node(
            f"{node}_details",
            color="white",
            size=40,
            shape="box",
            label=attributes["details"]
        )
        # Add invisible edge to keep them close
        G.add_edge(node, f"{node}_details", color="rgba(0,0,0,0)")
    else:
        G.add_node(
            node,
            color=attributes["color"],
            size=attributes["size"],
            shape=attributes["shape"],
            label=node
        )

# Add edges with labels and custom arrow directions
for source, target, label, direction in edges:
    G.add_edge(source, target, title=label, label=label, arrows=direction)

# Create interactive PyVis network
net = Network(height="700px", width="100%", directed=True, notebook=True)
net.from_nx(G)
net.repulsion(node_distance=200, central_gravity=0.3)

# Customize edge labels and arrows
for edge in net.edges:
    if "color" in edge:
        edge["color"] = edge["color"]
    edge["label"] = edge.get("title", "")
    if edge.get("arrows") == "both":
        edge["arrows"] = "to,from"

# Add JavaScript for highlighting
combined_js = """
<script>
network.on("click", function(params) {
    if (params.nodes.length > 0) {
        var selectedNode = params.nodes[0];
        var connectedNodes = new Set([selectedNode]);
        var connectedEdges = new Set();
        
        network.getConnectedNodes(selectedNode).forEach(function(connectedNode) {
            connectedNodes.add(connectedNode);
            network.getConnectedEdges(selectedNode).forEach(function(edgeId) {
                connectedEdges.add(edgeId);
            });
        });

        Object.values(network
