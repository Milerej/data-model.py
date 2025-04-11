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

# Enhanced network visualization options
network_options = """
const options = {
    "nodes": {
        "font": {
            "size": 12
        },
        "color": {
            "highlight": {
                "border": "#FFA500",
                "background": "#FFA500"
            }
        }
    },
    "edges": {
        "color": {
            "inherit": false,
            "highlight": "#FFA500"
        },
        "smooth": {
            "enabled": false
        },
        "width": 1.5
    },
    "interaction": {
        "hover": true,
        "hoverConnectedEdges": true,
        "selectConnectedEdges": true,
        "multiselect": true,
        "navigationButtons": true
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
    },
    "layout": {
        "improvedLayout": true,
        "hierarchical": {
            "enabled": false
        }
    }
};

// Add event listeners for node selection
network.on("click", function(params) {
    if (params.nodes.length > 0) {
        var selectedNode = params.nodes[0];
        var connectedNodes = new Set();
        var connectedEdges = new Set();
        
        // First degree connections
        network.getConnectedNodes(selectedNode).forEach(function(nodeId) {
            connectedNodes.add(nodeId);
            network.getConnectedEdges(nodeId).forEach(function(edgeId) {
                connectedEdges.add(edgeId);
            });
        });
        
        // Second degree connections
        connectedNodes.forEach(function(nodeId) {
            network.getConnectedNodes(nodeId).forEach(function(secondDegreeNode) {
                connectedNodes.add(secondDegreeNode);
                network.getConnectedEdges(secondDegreeNode).forEach(function(edgeId) {
                    connectedEdges.add(edgeId);
                });
            });
        });

        // Update visualization
        var allNodes = network.body.nodes;
        var allEdges = network.body.edges;
        
        Object.values(allNodes).forEach(function(node) {
            if (node.id === selectedNode || connectedNodes.has(node.id)) {
                node.options.opacity = 1.0;
            } else {
                node.options.opacity = 0.2;
            }
        });
        
        Object.values(allEdges).forEach(function(edge) {
            if (connectedEdges.has(edge.id)) {
                edge.options.opacity = 1.0;
            } else {
                edge.options.opacity = 0.2;
            }
        });
        
        network.redraw();
    } else {
        // Reset all nodes and edges if clicking on empty space
        Object.values(network.body.nodes).forEach(function(node) {
            node.options.opacity = 1.0;
        });
        Object.values(network.body.edges).forEach(function(edge) {
            edge.options.opacity = 1.0;
        });
        network.redraw();
    }
});
"""

# First visualization edges
edges = [
    ("Agency", "Ministry Family", "FK: Ministry_ID", "to"),
    # Add your first set of edges here
]

def create_network(edges, entities):
    G = nx.DiGraph()
    for node, color in entities.items():
        G.add_node(node, title=node, color=color)
    
    for source, target, label, direction in edges:
        G.add_edge(source, target, title=label, label=label, arrows=direction)
    
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
    
    return net

# Create and display first visualization
net1 = create_network(edges, entities)
net1.save_graph("graph1.html")
components.html(open("graph1.html", "r", encoding='utf-8').read(), height=750, scrolling=True)

# Second visualization
st.title("🧠🧠 Viz - Mock Up Data")

edges_mock = [
    ("Agency", "System Overview", "relates to", "both"),
    # Add your second set of edges here
]

# Create and display second visualization
net2 = create_network(edges_mock, entities)
net2.save_graph("graph2.html")
components.html(open("graph2.html", "r", encoding='utf-8').read(), height=750, scrolling=True)
