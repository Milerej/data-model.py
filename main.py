import streamlit as st
from pyvis.network import Network
import networkx as nx
import streamlit.components.v1 as components
import tempfile
import os

st.set_page_config(page_title="Interactive Interdependency Graph", layout="wide")

st.title("⚙️ Data Model : System Management")

# Define entity modules and colors
entities = {
    "System Management": {
        "color": "green", 
        "size": 30, 
        "shape": "dot",
        "title": "System Management Module"
    },
    "System Overview": {
        "color": "green", 
        "size": 15, 
        "shape": "dot",
        "title": "\n".join([
            "Fields:",
            "• Agency",
            "• Ministry Family",
            "• System ID (Primary Key)",
            "• System Name",
            "• System Description",
            "• System Status"
        ])
    },
    "Criticality Assessment": {
        "color": "green", 
        "size": 15,
        "shape": "dot",
        "title": "\n".join([
            "Fields:",
            "• Economy",
            "• Public Health and Safety",
            "• National Security",
            "• Social Preparedness",
            "• Public Service",
            "• Designated CII under the Cybersecurity Act",
            "• System Criticality (System Auto-generated) ",
            "• IDSC's Approval Date (CA) ",
            "• IDSC's Approval Attachment (CA) ",
            "• Approved by MHA? ",
            "• Approved by CSA? ",
            "• Approved by SNDGO? ",
            "• MHA Comments",
            "• CSA Comments",
            "• SNDGO Comments"
        ])
    },
    "Security & Sensitivity Classification": {
        "color": "green", 
        "size": 15, 
        "shape": "dot",
       "title": "\n".join([
            "Fields:",
                "• Security Classification",
                "• Sensitivity Classification",
        ])
    },
    "Risk Materiality Level": {
        "color": "green", 
        "size": 15, 
        "shape": "dot",
        "title": "\n".join([
            "Fields:",
                "• Computed Risk Materiality level (System Auto-generated)",
                "• Computed RML",
                "• Computed RML Date",
                "• Agency Proposed Risk Materiality level",
                "• In line with Computed Risk Materiality Level? (System Auto-generated)",
                "• Justification (if not in line with computed",
                "• Endorsed Risk Materiality level:",
                "• Endorsed Risk Materiality level:",
                "• Date Endorsed:",
                "• Endorsed Comments"
        ])
    },
    "System Resiliency": {
        "color": "green", 
        "size": 15, 
        "shape": "dot",
          "title": "\n".join([
            "Fields:",
                "• Service Availability"
        ])
    },
    "Hosting and System Dependencies": {
        "color": "green", 
        "size": 15, 
        "shape": "dot",
        "title": "Hosting environment and system dependency information"
    },
    "Central Programmes": {
        "color": "green", 
        "size": 15, 
        "shape": "dot",
        "title": "Central programmes information"
    }
}

# Define edges with PK/FK relationships
edges = [
    ("System Management", "System Overview", "PK: System_ID", "both"),
    ("System Management", "Criticality Assessment", "PK: System_ID", "both"),
    ("System Management", "Security & Sensitivity Classification", "PK: System_ID", "both"),
    #("System Management", "Risk Materiality Level", "PK: System_ID", "boh"),
    ("System Management", "System Resiliency", "PK: System_ID", "both"),
    ("System Management", "Hosting and System Dependencies", "PK: System_ID", "both"),
    ("System Management", "Central Programmes", "PK: System_ID", "both"),
    ("Risk Materiality Level", "Security & Sensitivity Classification", "PK: System_ID", "both"),
    ("Risk Materiality Level", "Hosting and System Dependencies", "PK: System_ID", "both"),
    ("Risk Materiality Level", "Criticality Assessment", "PK: System_ID", "both")
]

# Create NetworkX graph
G = nx.DiGraph()
for node, attributes in entities.items():
    node_attrs = {
        "color": attributes["color"],
        "size": attributes["size"],
        "shape": attributes["shape"],
        "title": attributes["title"],
        "label": node
    }
    G.add_node(node, **node_attrs)

# Add edges with labels and custom arrow directions
for source, target, label, direction in edges:
    G.add_edge(source, target, title=label, label=label, arrows=direction)

# Create interactive PyVis network
net = Network(height="700px", width="100%", directed=True, notebook=True)
net.from_nx(G)

# Set options as a string
net.set_options('{' + '''
    "physics": {
        "enabled": true,
        "stabilization": {
            "enabled": true,
            "iterations": 1000,
            "updateInterval": 50,
            "onlyDynamicEdges": false,
            "fit": true
        },
        "barnesHut": {
            "gravitationalConstant": -5000,
            "centralGravity": 0.2,
            "springLength": 350,
            "springConstant": 0.02,
            "damping": 0.2,
            "avoidOverlap": 1
        },
        "minVelocity": 0.5,
        "maxVelocity": 40
    },
    "edges": {
        "smooth": {
            "type": "continuous",
            "forceDirection": "none"
        },
        "length": 350,
        "font": {
            "size": 14,
            "strokeWidth": 2,
            "strokeColor": "#ffffff"
        }
    },
    "nodes": {
        "font": {
            "size": 16,
            "strokeWidth": 3,
            "strokeColor": "#ffffff"
        },
        "margin": 20,
        "fixed": {
            "x": false,
            "y": false
        }
    },
    "interaction": {
        "dragNodes": true,
        "dragView": true,
        "zoomView": true,
        "hover": true
    },
    "layout": {
        "improvedLayout": true,
        "randomSeed": 42,
        "hierarchical": {
            "enabled": false,
            "nodeSpacing": 250,
            "levelSeparation": 250
        }
    }
''' + '}')

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
