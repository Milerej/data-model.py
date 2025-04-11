import streamlit as st
from pyvis.network import Network
import networkx as nx
import streamlit.components.v1 as components
import tempfile
import os

st.set_page_config(page_title="Interactive Interdependency Graph", layout="wide")

st.title("🧠 Interactive System Management Data Model")

# Define custom CSS for tooltips
custom_css = """
<style>
.tooltip-table {
    border-collapse: collapse;
    width: 100%;
    background-color: white;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.tooltip-table td {
    padding: 8px;
    border: 1px solid #ddd;
}
.tooltip-table .field-name {
    font-weight: bold;
    background-color: #f5f5f5;
}
</style>
"""

# Define tooltip content for each node
tooltip_info = {
    "System Overview": "<table style='width:100%;border-collapse:collapse;background:white'>" + 
                      "<tr><td style='padding:5px;border:1px solid gray;font-weight:bold'>Agency</td><td style='padding:5px;border:1px solid gray'>&nbsp;</td></tr>" + 
                      "<tr><td style='padding:5px;border:1px solid gray;font-weight:bold'>Ministry Family</td><td style='padding:5px;border:1px solid gray'>&nbsp;</td></tr>" + 
                      "<tr><td style='padding:5px;border:1px solid gray;font-weight:bold'>System ID (Primary Key)</td><td style='padding:5px;border:1px solid gray'>&nbsp;</td></tr>" + 
                      "<tr><td style='padding:5px;border:1px solid gray;font-weight:bold'>System Name</td><td style='padding:5px;border:1px solid gray'>&nbsp;</td></tr>" + 
                      "<tr><td style='padding:5px;border:1px solid gray;font-weight:bold'>System Description</td><td style='padding:5px;border:1px solid gray'>&nbsp;</td></tr>" + 
                      "<tr><td style='padding:5px;border:1px solid gray;font-weight:bold'>System Status</td><td style='padding:5px;border:1px solid gray'>&nbsp;</td></tr>" + 
                      "</table>",
    "System Management": "",
    "Criticality Assessment": "",
    "Security & Sensitivity Classification": "",
    "Risk Materiality Level": "",
    "System Resiliency": "",
    "Hosting and System Dependencies": "",
    "Central Programmes": ""
}

tooltip_info = {
    "System Overview": '<table style="border-collapse: collapse; width: 100%; background-color: white;">' + \
        '<tr><td style="border: 1px solid #ddd; padding: 8px; font-weight: bold; background-color: #f5f5f5;">Agency</td><td style="border: 1px solid #ddd; padding: 8px;"></td></tr>' + \
        '<tr><td style="border: 1px solid #ddd; padding: 8px; font-weight: bold; background-color: #f5f5f5;">Ministry Family</td><td style="border: 1px solid #ddd; padding: 8px;"></td></tr>' + \
        '<tr><td style="border: 1px solid #ddd; padding: 8px; font-weight: bold; background-color: #f5f5f5;">System ID (Primary Key)</td><td style="border: 1px solid #ddd; padding: 8px;"></td></tr>' + \
        '<tr><td style="border: 1px solid #ddd; padding: 8px; font-weight: bold; background-color: #f5f5f5;">System Name</td><td style="border: 1px solid #ddd; padding: 8px;"></td></tr>' + \
        '<tr><td style="border: 1px solid #ddd; padding: 8px; font-weight: bold; background-color: #f5f5f5;">System Description</td><td style="border: 1px solid #ddd; padding: 8px;"></td></tr>' + \
        '<tr><td style="border: 1px solid #ddd; padding: 8px; font-weight: bold; background-color: #f5f5f5;">System Status</td><td style="border: 1px solid #ddd; padding: 8px;"></td></tr>' + \
        '</table>',
    "System Management": "",
    "Criticality Assessment": "",
    "Security & Sensitivity Classification": "",
    "Risk Materiality Level": "",
    "System Resiliency": "",
    "Hosting and System Dependencies": "",
    "Central Programmes": ""
}

# Define entity modules and colors
entities = {
    "System Management": {"color": "green", "size": 30},
    "System Overview": {"color": "green", "size": 20},
    "Criticality Assessment": {"color": "green", "size": 20},
    "Security & Sensitivity Classification": {"color": "green", "size": 20},
    "Risk Materiality Level": {"color": "green", "size": 20},
    "System Resiliency": {"color": "green", "size": 20},
    "Hosting and System Dependencies": {"color": "green", "size": 20},
    "Central Programmes": {"color": "green", "size": 20}
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
    G.add_node(node, title=tooltip_info[node], color=attributes["color"], size=attributes["size"])

# Add edges with labels and custom arrow directions
for source, target, label, direction in edges:
    G.add_edge(source, target, title=label, label=label, arrows=direction)

# Create interactive PyVis network
net = Network(height="700px", width="100%", directed=True, notebook=True)
net.from_nx(G)
net.repulsion(node_distance=200, central_gravity=0.3)

# Customize edge labels, arrows, and node sizes
for node in net.nodes:
    node["value"] = entities[node["id"]]["size"]

for edge in net.edges:
    edge["label"] = edge["title"]
    if edge["arrows"] == "both":
        edge["arrows"] = "to,from"
    else:
        edge["arrows"] = edge["arrows"]

# Add JavaScript for tooltips and highlighting
combined_js = """
<script>
// Tooltip handling
network.on("hoverNode", function(params) {
    var node = params.node;
    var x = params.event.center.x;
    var y = params.event.center.y;
    
    var existingTooltip = document.getElementById('tooltip');
    if (existingTooltip) {
        existingTooltip.parentNode.removeChild(existingTooltip);
    }
    
    var tooltip = document.createElement('div');
    tooltip.id = 'tooltip';
    tooltip.style.position = 'absolute';
    tooltip.style.left = (x + 10) + 'px';
    tooltip.style.top = (y + 10) + 'px';
    tooltip.style.backgroundColor = 'white';
    tooltip.style.padding = '10px';
    tooltip.style.borderRadius = '5px';
    tooltip.style.boxShadow = '0 2px 4px rgba(0,0,0,0.2)';
    tooltip.style.zIndex = '1000';
    tooltip.innerHTML = node.title;
    
    document.body.appendChild(tooltip);
});

network.on("blurNode", function(params) {
    var tooltip = document.getElementById('tooltip');
    if (tooltip) {
        tooltip.parentNode.removeChild(tooltip);
    }
});

// Node highlighting
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

// Update tooltip position on canvas drag
network.on("dragging", function(params) {
    var tooltip = document.getElementById('tooltip');
    if (tooltip) {
        tooltip.parentNode.removeChild(tooltip);
    }
});
</script>
"""

# Create a temporary directory and save the graph
with tempfile.TemporaryDirectory() as temp_dir:
    path = os.path.join(temp_dir, "graph.html")
    net.save_graph(path)
    
    with open(path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # Add custom CSS and JavaScript
    html_content = html_content.replace('</head>', f'{custom_css}</head>')
    html_content = html_content.replace('</body>', f'{combined_js}</body>')
    
    components.html(html_content, height=750, scrolling=True)
