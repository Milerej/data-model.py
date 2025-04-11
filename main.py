import streamlit as st
from pyvis.network import Network
import networkx as nx
import streamlit.components.v1 as components

st.set_page_config(page_title="Interactive Interdependency Graph", layout="wide")

st.title("🧠 Interactive System Management Data Model")

# Define entity modules and colors - updated System Overview to green
entities = {
    "System Management": {"color": "green", "size": 30},  # Bigger size for main module
    "System Overview": {"color": "green", "size": 20},    # Same color as System Management
    "Criticality Assessment": {"color": "teal", "size": 20},
    "Security & Sensitivity Classification": {"color": "green", "size": 20},
    "Risk Materiality Level": {"color": "green", "size": 20},
    "System Resiliency": {"color": "green", "size": 20},
    "Hosting and System Dependencies": {"color": "green", "size": 20},
    "Central Programmes": {"color": "green", "size": 20}
}

# Add filter in sidebar
st.sidebar.title("Filter Options")
selected_nodes = st.sidebar.multiselect(
    "Select nodes to highlight:",
    options=list(entities.keys()),
    default=None
)

# Define edges with PK/FK relationships
edges = [
    ("System Management", "System Overview", "FK: System_ID", "both"),
    ("System Management", "Criticality Assessment", "FK: System_ID", "both"),
    ("System Management", "Security & Sensitivity Classification", "FK: System_ID", "both"),
    ("System Management", "Risk Materiality Level", "FK: System_ID", "both"),
    ("System Management", "System Resiliency", "FK: System_ID", "both"),
    ("System Management", "Hosting and System Dependencies", "FK: System_ID", "both"),
    ("System Management", "Central Programmes", "FK: System_ID", "both")
]

# Create NetworkX graph
G = nx.DiGraph()
for node, attributes in entities.items():
    G.add_node(node, title=node, color=attributes["color"], size=attributes["size"])

# Add edges with labels and custom arrow directions
for source, target, label, direction in edges:
    G.add_edge(source, target, title=label, label=label, arrows=direction)

# Create interactive PyVis network
net = Network(height="700px", width="100%", directed=True)
net.from_nx(G)
net.repulsion(node_distance=200, central_gravity=0.3)

# Customize edge labels, arrows, and node sizes
for node in net.nodes:
    node["value"] = entities[node["id"]]["size"]  # Set node size

for edge in net.edges:
    edge["label"] = edge["title"]
    if edge["arrows"] == "both":
        edge["arrows"] = "to,from"
    else:
        edge["arrows"] = edge["arrows"]

# Add JavaScript for highlighting selected nodes and their connections
highlight_js = """
<script>
function highlightNodes(selectedNodes) {
    if (selectedNodes.length === 0) {
        Object.values(network.body.nodes).forEach(node => {
            node.options.opacity = 1.0;
        });
        Object.values(network.body.edges).forEach(edge => {
            edge.options.opacity = 1.0;
        });
        network.redraw();
        return;
    }

    var connectedNodes = new Set(selectedNodes);
    var connectedEdges = new Set();
    
    selectedNodes.forEach(function(nodeId) {
        network.getConnectedNodes(nodeId).forEach(function(connectedNode) {
            connectedNodes.add(connectedNode);
            network.getConnectedEdges(nodeId).forEach(function(edgeId) {
                connectedEdges.add(edgeId);
            });
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
    
    network.redraw();
}

highlightNodes(%s);

network.on("click", function(params) {
    if (params.nodes.length > 0) {
        highlightNodes([params.nodes[0]]);
    } else {
        highlightNodes([]);
    }
});
</script>
""" % str(selected_nodes)

# Save and display in Streamlit
net.save_graph("graph.html")
with open("graph.html", "r", encoding='utf-8') as f:
    html_content = f.read()
    html_content = html_content.replace('</body>', f'{highlight_js}</body>')
components.html(html_content, height=750, scrolling=True)

# Add legend
st.sidebar.markdown("### Color Legend")
for entity_type, color in {
    "System Management & Overview": "green",
    "Criticality Assessment": "teal"
}.items():
    st.sidebar.markdown(
        f'<div style="display: flex; align-items: center;">'
        f'<div style="width: 20px; height: 20px; background-color: {color}; margin-right: 10px;"></div>'
        f'<div>{entity_type}</div></div>',
        unsafe_allow_html=True
    )

# Add instructions
st.sidebar.markdown("""
### Instructions
1. Select nodes from the dropdown above to highlight them and their connections
2. Click on any node in the graph to highlight its connections
3. Click on empty space to reset the view
4. Drag nodes to
