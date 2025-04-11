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
.vis-tooltip {
    position: absolute;
    background-color: white;
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 10px;
    font-family: Arial;
    font-size: 14px;
    z-index: 1000;
    max-width: 500px;
    white-space: normal;
}
.vis-tooltip table {
    border-collapse: collapse;
    width: 100%;
    margin-top: 5px;
}
.vis-tooltip th, .vis-tooltip td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
}
.vis-tooltip th {
    background-color: #f2f2f2;
}
</style>
"""

# Define table information for mouseover
table_info = {
    "System Overview": """
<div class='vis-tooltip'>
<table>
<tr><th>Column</th><th>Type</th><th>Description</th></tr>
<tr><td>system_id (PK)</td><td>UUID</td><td>Unique identifier for the system</td></tr>
<tr><td>agency</td><td>VARCHAR(100)</td><td>Agency name</td></tr>
<tr><td>ministry_family</td><td>VARCHAR(100)</td><td>Ministry family name</td></tr>
<tr><td>system_name</td><td>VARCHAR(200)</td><td>Name of the system</td></tr>
<tr><td>system_description</td><td>TEXT</td><td>Detailed description of the system</td></tr>
<tr><td>system_status</td><td>VARCHAR(50)</td><td>Current status of the system</td></tr>
<tr><td>created_at</td><td>TIMESTAMP</td><td>Record creation timestamp</td></tr>
<tr><td>updated_at</td><td>TIMESTAMP</td><td>Last update timestamp</td></tr>
</table>
</div>
""",
    "System Management": """
<div class='vis-tooltip'>
<table>
<tr><th>Column</th><th>Type</th></tr>
<tr><td>system_id (PK)</td><td>UUID</td></tr>
<tr><td>system_name</td><td>VARCHAR(200)</td></tr>
<tr><td>created_at</td><td>TIMESTAMP</td></tr>
<tr><td>updated_at</td><td>TIMESTAMP</td></tr>
</table>
</div>
""",
    "Criticality Assessment": """
<div class='vis-tooltip'>
<table>
<tr><th>Column</th><th>Type</th></tr>
<tr><td>assessment_id (PK)</td><td>UUID</td></tr>
<tr><td>system_id (FK)</td><td>UUID</td></tr>
<tr><td>criticality_level</td><td>VARCHAR(50)</td></tr>
<tr><td>assessment_date</td><td>DATE</td></tr>
</table>
</div>
""",
    "Security & Sensitivity Classification": """
<div class='vis-tooltip'>
<table>
<tr><th>Column</th><th>Type</th></tr>
<tr><td>security_id (PK)</td><td>UUID</td></tr>
<tr><td>system_id (FK)</td><td>UUID</td></tr>
<tr><td>classification_level</td><td>VARCHAR(50)</td></tr>
<tr><td>last_review_date</td><td>DATE</td></tr>
</table>
</div>
""",
    "Risk Materiality Level": """
<div class='vis-tooltip'>
<table>
<tr><th>Column</th><th>Type</th></tr>
<tr><td>risk_id (PK)</td><td>UUID</td></tr>
<tr><td>system_id (FK)</td><td>UUID</td></tr>
<tr><td>materiality_level</td><td>VARCHAR(50)</td></tr>
<tr><td>assessment_date</td><td>DATE</td></tr>
</table>
</div>
""",
    "System Resiliency": """
<div class='vis-tooltip'>
<table>
<tr><th>Column</th><th>Type</th></tr>
<tr><td>resiliency_id (PK)</td><td>UUID</td></tr>
<tr><td>system_id (FK)</td><td>UUID</td></tr>
<tr><td>resiliency_level</td><td>VARCHAR(50)</td></tr>
<tr><td>last_test_date</td><td>DATE</td></tr>
</table>
</div>
""",
    "Hosting and System Dependencies": """
<div class='vis-tooltip'>
<table>
<tr><th>Column</th><th>Type</th></tr>
<tr><td>dependency_id (PK)</td><td>UUID</td></tr>
<tr><td>system_id (FK)</td><td>UUID</td></tr>
<tr><td>dependency_type</td><td>VARCHAR(100)</td></tr>
<tr><td>dependency_details</td><td>TEXT</td></tr>
</table>
</div>
""",
    "Central Programmes": """
<div class='vis-tooltip'>
<table>
<tr><th>Column</th><th>Type</th></tr>
<tr><td>programme_id (PK)</td><td>UUID</td></tr>
<tr><td>system_id (FK)</td><td>UUID</td></tr>
<tr><td>programme_name</td><td>VARCHAR(200)</td></tr>
<tr><td>status</td><td>VARCHAR(50)</td></tr>
</table>
</div>
"""
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
    tooltip = table_info[node].replace('\n', '').replace('"', '\\"')
    G.add_node(node, title=tooltip, color=attributes["color"], size=attributes["size"])

# Add edges with labels and custom arrow directions
for source, target, label, direction in edges:
    G.add_edge(source, target, title=label, label=label, arrows=direction)

# Create interactive PyVis network
net = Network(height="700px", width="100%", directed=True)
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

# Add JavaScript for tooltip handling
tooltip_js = """
<script>
network.on("hoverNode", function(params) {
    var tooltip = document.querySelector('.vis-tooltip');
    if (tooltip) {
        tooltip.innerHTML = params.node.title;
        tooltip.style.display = 'block';
    }
});

network.on("blurNode", function(params) {
    var tooltip = document.querySelector('.vis-tooltip');
    if (tooltip) {
        tooltip.style.display = 'none';
    }
});
</script>
"""

# Add JavaScript for highlighting selected nodes and their connections
highlight_js = """
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
</script>
"""

# Create a temporary directory and save the graph
with tempfile.TemporaryDirectory() as temp_dir:
    path = os.path.join(temp_dir, "graph.html")
    net.save_graph(path)
    
    with open(path, "r", encoding="utf-8") as f:
        html_content = f.read()
        
    # Insert custom CSS and JavaScript
    html_content = html_content.replace('</head>', f'{custom_css}</head>')
    html_content = html_content.replace('</body>', f'{tooltip_js}{highlight_js}</body>')
    
    # Remove HTML escaping in node titles
    html_content = html_content.replace('&lt;', '<').replace('&gt;', '>')
    html_content = html_content.replace('\\n', '')
    html_content = html_content.replace('\\"', '"')
    
    components.html(html_content, height=750, scrolling=True)
