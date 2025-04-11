import streamlit as st
from pyvis.network import Network
import networkx as nx
import streamlit.components.v1 as components
import json

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

# Define edges for first visualization
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

# Define edges for second visualization (mock data)
edges_mock = [
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

# Network options
network_options = {
    "nodes": {
        "font": {"size": 12},
        "color": {
            "highlight": {
                "border": "#FFA500",
                "background": "#FFA500"
            }
        }
    },
    "edges": {
        "color": {
            "inherit": False,
            "highlight": "#FFA500"
        },
        "smooth": {
            "enabled": False
        },
        "width": 1.5
    },
    "interaction": {
        "hover": True,
        "hoverConnectedEdges": True,
        "selectConnectedEdges": True,
        "multiselect": True,
        "navigationButtons": True
    },
    "physics": {
        "enabled": True,
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
            "enabled": True,
            "iterations": 1000,
            "updateInterval": 25
        }
    },
    "layout": {
        "improvedLayout": True,
        "hierarchical": {
            "enabled": False
        }
    }
}

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
    net.set_options(json.dumps(network_options))
    
    for edge in net.edges:
        edge["label"] = edge["title"]
        if edge["arrows"] == "both":
            edge["arrows"] = "to,from"
        else:
            edge["arrows"] = edge["arrows"]
    
    return net

def add_highlighting_js(html_content):
    highlight_js = """
    <script>
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
    </script>
    """
    return html_content.replace('</body>', f'{highlight_js}</body>')

# Create and display first visualization
net1 = create_network(edges, entities)
net1.save_graph("graph1.html")
with open("graph1.html", "r", encoding='utf-8') as f:
    html_content = f.read()
components.html(add_highlighting_js(html_content), height=750, scrolling=True)

# Second visualization
st.title("🧠🧠 Viz - Mock Up Data")

# Create and display second visualization
net2 = create_network(edges_mock, entities)
net2.save_graph("graph2.html")
with open("graph2.html", "r", encoding='utf-8') as f:
    html_content = f.read()
components.html(add_highlighting_js(html_content), height=750, scrolling=True)
