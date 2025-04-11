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
.custom-tooltip {
    position: absolute;
    background-color: white;
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    z-index: 1000;
    max-width: 300px;
}

.custom-tooltip table {
    border-collapse: collapse;
    width: 100%;
}

.custom-tooltip td {
    border: 1px solid #ddd;
    padding: 8px;
}

.custom-tooltip td:first-child {
    font-weight: bold;
    background-color: #f5f5f5;
}
</style>
"""

# Define tooltip content
tooltip_data = {
    "System Overview": {
        "Agency": "",
        "Ministry Family": "",
        "System ID (Primary Key)": "",
        "System Name": "",
        "System Description": "",
        "System Status": ""
    }
}

# Convert tooltip data to a format that can be passed to JavaScript
tooltip_info = {
    "System Overview": "TOOLTIP_DATA:" + str(list(tooltip_data["System Overview"].items())),
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

# Add JavaScript for custom tooltips and highlighting
combined_js = """
<script>
// Custom tooltip handling
function createTooltipContent(data) {
    if (!data.startsWith('TOOLTIP_DATA:')) return data;
    
    try {
        const tooltipData = eval(data.replace('TOOLTIP_DATA:', ''));
        let table = '<table>';
        tooltipData.forEach(([key, value]) => {
            table += `<tr><td>${key}</td><td>${value || '&nbsp;'}</td></tr>`;
        });
        table += '</table>';
        return table;
    } catch (e) {
        console.error('Error parsing tooltip data:', e);
        return '';
    }
}

// Tooltip handling
network.on("hoverNode", function(params) {
    var node = params.node;
    var x = params.event.center.x;
    var y = params.event.center.y;
    
    var existingTooltip = document.getElementById('custom-tooltip');
    if (existingTooltip) {
        existingTooltip.parentNode.removeChild(existingTooltip);
    }
    
    if (!node.title) return;
    
    var tooltip = document.createElement('div');
    tooltip.id = 'custom-tooltip';
    tooltip.className = 'custom-tooltip';
    tooltip.style.left = (x + 10) + 'px';
    tooltip.style.top = (y + 10) + 'px';
    tooltip.innerHTML = createTooltipContent(node.title);
    
    document.body.appendChild(tooltip);
});

network.on("blurNode", function(params) {
    var tooltip = document.getElementById('custom-tooltip');
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
    var tooltip = document.getElementById('custom-tooltip');
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
