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
net.set_options('''
{
    "physics": {
        "barnesHut": {
            "gravitationalConstant": -2000,
            "centralGravity": 0.3,
            "springLength": 200,
            "springConstant": 0.04,
            "damping": 0.09,
            "avoidOverlap": 0.1
        },
        "minVelocity": 0.75
    },
    "edges": {
        "smooth": {
            "type": "continuous",
            "forceDirection": "none"
        }
    }
}
''')

# Customize edge labels and arrows
for edge in net.edges:
    edge["label"] = edge.get("title", "")
    if edge.get("arrows") == "both":
        edge["arrows"] = "to,from"

# Add JavaScript for highlighting
highlight_js = """
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

        Object.values(network.body.nodes).forEach(function(node) {
            if (connectedNodes.has(node.id)) {
                node.options.opacity = 1.0;
            } else {
                node.options.opacity = 0.2;
            }
        });
        
        Object.values(network.body.edges).forEach(function(edge) {
            if (connectedEdges.has(edge.id)) {
                edge.options.opacity = 1.0;
            } else {
                edge.options.opacity = 0.2;
            }
        });
    } else {
        Object.values(network.body.nodes).forEach(node => {
            node.options.opacity = 1.0;
        });
        Object.values(network.body.edges).forEach(edge => {
            edge.options.opacity = 1.0;
        });
    }
    network.redraw();
});
"""

# Create a temporary directory and save the graph
with tempfile.TemporaryDirectory() as temp_dir:
    path = os.path.join(temp_dir, "graph.html")
    net.save_graph(path)
    
    with open(path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # Add JavaScript
    html_content = html_content.replace('</body>', f'<script>{highlight_js}</script></body>')
    
    components.html(html_content, height=750, scrolling=True)
