import streamlit as st
from pyvis.network import Network
import networkx as nx
import streamlit.components.v1 as components
import tempfile
import os

st.set_page_config(page_title="Interactive Interdependency Graph", layout="wide")

st.title("🧠 Interactive System Management Data Model")

# Create network with specific physics options
net = Network(height="700px", width="100%", directed=True)
net.force_atlas_2based()

# Add nodes directly to network
net.add_node(1, 
    label="\n".join([
        "SYSTEM MANAGEMENT",
        "─────────────",
        "Agency Code",
        "Ministry Code",
        "System ID",
        "System Name",
        "System Description",
        "System Status"
    ]),
    color="white",
    shape="box",
    size=60)

net.add_node(2, 
    label="\n".join([
        "SYSTEM OVERVIEW",
        "─────────────",
        "Agency",
        "Ministry Family",
        "System ID (Primary Key)",
        "System Name",
        "System Description",
        "System Status"
    ]),
    color="white",
    shape="box",
    size=60)

# Add other nodes
node_ids = {
    "Criticality Assessment": 3,
    "Security & Sensitivity Classification": 4,
    "Risk Materiality Level": 5,
    "System Resiliency": 6,
    "Hosting and System Dependencies": 7,
    "Central Programmes": 8
}

for name, id in node_ids.items():
    net.add_node(id, label=name, color="green", size=20)

# Add edges
edges = [
    (1, 2, "PK: System_ID"),
    (1, 3, "PK: System_ID"),
    (1, 4, "PK: System_ID"),
    (1, 5, "PK: System_ID"),
    (1, 6, "PK: System_ID"),
    (1, 7, "PK: System_ID"),
    (1, 8, "PK: System_ID"),
    (3, 5, "PK: System_ID"),
    (7, 5, "PK: System_ID"),
    (4, 5, "PK: System_ID")
]

for source, target, label in edges:
    net.add_edge(source, target, label=label, arrows='to,from')

# Set physics options
net.set_options("""
const options = {
  "physics": {
    "forceAtlas2Based": {
      "gravitationalConstant": -50,
      "centralGravity": 0.01,
      "springLength": 200,
      "springConstant": 0.08
    },
    "maxVelocity": 50,
    "solver": "forceAtlas2Based",
    "timestep": 0.35,
    "stabilization": {"iterations": 150}
  }
}
""")

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
    
    # Add JavaScript
    html_content = html_content.replace('</body>', f'{combined_js}</body>')
    
    components.html(html_content, height=750, scrolling=True)
