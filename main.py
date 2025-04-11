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

# Add filter in sidebar
st.sidebar.title("Filter Options")
selected_nodes = st.sidebar.multiselect(
    "Select nodes to highlight:",
    options=list(entities.keys()),
    default=None
)

# Define edges with PK/FK relationships
edges = [
    ("Agency", "System Overview", "FK: Agency_ID", "both"),
    ("Agency", "Ministry Family", "FK: Ministry_ID", "both"),
    ("System Overview", "Criticality Assessment", "FK: System_ID", "both"),
    ("System Overview", "Policy", "FK: Policy_ID", "both"),
    ("Policy", "Policy Waivers", "FK: Policy_ID", "both"),
    ("Supplier Profile", "Supplier Risk Management", "FK: Supplier_ID", "both"),
    ("Supplier Profile", "Supplier Contracts", "FK: Supplier_ID", "both"),
    ("Supplier Profile", "Actions Against Errant Supplier", "FK: Supplier_ID", "both"),
    ("Supplier Profile", "Supplier Performance Feedback", "FK: Supplier_ID", "both"),
    ("Supplier Profile", "Bulk Tender ECN Details", "FK: Supplier_ID", "both"),
    ("Supplier Profile", "EDH Agency", "FK: Supplier_ID", "both"),
    ("Risk Assessments", "Risk Treatments", "FK: Assessment_ID", "both"),
    ("Audit Findings", "Risk Treatments", "FK: Finding_ID", "both"),
    ("Supplier Risk Management", "Risk Assessments", "FK: Risk_ID", "both"),
    ("Supplier Performance Feedback", "Supplier Risk Management", "FK: Feedback_ID", "both"),
    ("Actions Against Errant Supplier", "Supplier Contracts", "FK: Action_ID", "both"),
    ("System Overview", "Supplier Contracts", "FK: System_ID", "both"),
    ("System Overview", "Audit Findings", "FK: System_ID", "both"),
    ("System Management", "System Overview", "FK: System_ID", "both"),
    ("System Management", "Criticality Assessment", "FK: System_ID", "both"),
    ("System Management", "Security & Sensitivity Classification", "FK: System_ID", "both"),
    ("System Management", "Risk Materiality Level", "FK: System_ID", "both"),
    ("System Management", "System Resiliency", "FK: System_ID", "both"),
    ("System Management", "Hosting and System Dependencies", "FK: System_ID", "both"),
    ("System Management", "Central Programmes", "FK: System_ID", "both"),
    ("System Management", "Supplier Contracts", "FK: System_ID", "both"),
    ("Supplier Contracts", "Hosting and System Dependencies", "FK: Contract_ID", "both")
]

# Create NetworkX graph
G = nx.DiGraph()
for node, color in entities.items():
    G.add_node(node, title=node, color=color)

# Add edges with labels and custom arrow directions
for source, target, label, direction in edges:
    G.add_edge(source, target, title=label, label=label, arrows=direction)

# Create interactive PyVis network
net = Network(height="700px", width="100%", directed=True)
net.from_nx(G)
net.repulsion(node_distance=200, central_gravity=0.3)

# Customize edge labels and arrows
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
    // If no nodes are selected, show all nodes and edges normally
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
    
    // Find directly connected nodes and edges
    selectedNodes.forEach(function(nodeId) {
        network.getConnectedNodes(nodeId).forEach(function(connectedNode) {
            connectedNodes.add(connectedNode);
            network.getConnectedEdges(nodeId).forEach(function(edgeId) {
                connectedEdges.add(edgeId);
            });
        });
    });

    // Update visualization
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

// Initial highlight based on selected nodes
highlightNodes(%s);

// Add event listener for node clicks
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
    "Ministry & Agency": "blue",
    "System & Criticality": "teal",
    "Policy": "red",
    "Supplier": "purple",
    "Risk": "orange",
    "Audit": "gray",
    "System Management": "green"
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
4. Drag nodes to rearrange the layout
""")
