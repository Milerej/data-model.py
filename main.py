import streamlit as st
from pyvis.network import Network
import networkx as nx
import streamlit.components.v1 as components
import tempfile
import os

st.set_page_config(page_title="Interactive Interdependency Graph", layout="wide")

st.title("🧠 Interactive System Management Data Model")

# Create two columns
col1, col2 = st.columns([2, 1])

# Define the table data for each node
table_data = {
    "System Overview": {
        "headers": ["Field", "Description"],
        "rows": [
            ["Agency", "Agency name"],
            ["Ministry Family", "Parent ministry"],
            ["System ID", "Primary Key"],
            ["System Name", "Name of the system"],
            ["System Description", "Detailed description"],
            ["System Status", "Current status"]
        ]
    },
    "Criticality Assessment": {
        "headers": ["Field", "Description"],
        "rows": [
            ["Economy", "Economic impact"],
            ["Public Health and Safety", "Health & safety impact"],
            ["National Security", "Security impact"],
            ["Social Preparedness", "Social impact"],
            ["Public Service", "Service impact"],
            ["Designated CII", "Critical Infrastructure status"],
            ["System Criticality", "Auto-generated assessment"]
        ]
    },
    # Add other tables as needed
}

# Store the selected node in session state
if 'selected_node' not in st.session_state:
    st.session_state.selected_node = None

# [Previous entities and edges definitions remain the same]

# Modify the JavaScript to communicate with Streamlit
highlight_js = """
network.on("click", function(params) {
    if (params.nodes.length > 0) {
        var selectedNode = params.nodes[0];
        // Send the selected node to Streamlit
        window.parent.postMessage({
            type: 'node_clicked',
            node: selectedNode
        }, '*');
        
        // Highlighting logic remains the same
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

# Add JavaScript for handling messages
handle_message_js = """
<script>
window.addEventListener('message', function(event) {
    if (event.data.type === 'node_clicked') {
        // Send the node data to Streamlit
        const node = event.data.node;
        window.parent.Streamlit.setComponentValue(node);
    }
});
</script>
"""

# Display the graph in the first column
with col1:
    # Create a temporary directory and save the graph
    with tempfile.TemporaryDirectory() as temp_dir:
        path = os.path.join(temp_dir, "graph.html")
        net.save_graph(path)
        
        with open(path, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        # Add JavaScript
        html_content = html_content.replace('</body>', f'{handle_message_js}<script>{highlight_js}</script></body>')
        
        # Create a unique key for the component
        component_value = components.html(html_content, height=750, scrolling=True, key="network_graph")
        
        if component_value is not None:
            st.session_state.selected_node = component_value

# Display the table in the second column
with col2:
    if st.session_state.selected_node:
        node_name = st.session_state.selected_node
        if node_name in table_data:
            st.subheader(f"{node_name} Details")
            table = table_data[node_name]
            st.table(pd.DataFrame(table["rows"], columns=table["headers"]))
        else:
            st.info(f"Click on a node to view its details")
    else:
        st.info("Click on a node to view its details")
