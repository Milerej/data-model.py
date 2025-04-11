import streamlit as st
from pyvis.network import Network
import networkx as nx
import streamlit.components.v1 as components
import tempfile
import os
import pandas as pd

st.set_page_config(page_title="Interactive Interdependency Graph", layout="wide")

st.title("🧠 Interactive System Management Data Model")

# Create two columns
col1, col2 = st.columns([2, 1])

# Define entity modules and colors
entities = {
    "System Management": {
        "color": "#2E7D32", 
        "size": 30, 
        "shape": "dot",
        "title": "Central node managing system relationships"
    },
    "System Overview": {
        "color": "#4CAF50", 
        "size": 25, 
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
        "color": "#4CAF50", 
        "size": 25, 
        "shape": "dot",
        "title": "\n".join([
            "Fields:",
            "• Economy",
            "• Public Health and Safety",
            "• National Security",
            "• Social Preparedness",
            "• Public Service",
            "• Designated CII under the Cybersecurity Act",
            "• System Criticality (System Auto-generated)"
        ])
    },
    "Security & Sensitivity Classification": {
        "color": "#4CAF50", 
        "size": 25, 
        "shape": "dot",
        "title": "Security and sensitivity classification details"
    },
    "Risk Materiality Level": {
        "color": "#4CAF50", 
        "size": 25, 
        "shape": "dot",
        "title": "Risk materiality assessment details"
    },
    "System Resiliency": {
        "color": "#4CAF50", 
        "size": 25, 
        "shape": "dot",
        "title": "System resiliency metrics and details"
    },
    "Hosting and System Dependencies": {
        "color": "#4CAF50", 
        "size": 25, 
        "shape": "dot",
        "title": "Hosting environment and system dependency information"
    },
    "Central Programmes": {
        "color": "#4CAF50", 
        "size": 25, 
        "shape": "dot",
        "title": "Central programmes information"
    }
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
    ("Risk Materiality Level", "Security & Sensitivity Classification", "PK: System_ID", "both"),
    ("Risk Materiality Level", "Hosting and System Dependencies", "PK: System_ID", "both"),
    ("Risk Materiality Level", "Criticality Assessment", "PK: System_ID", "both")
]

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
    "Security & Sensitivity Classification": {
        "headers": ["Field", "Description"],
        "rows": [
            ["Classification Level", "System classification level"],
            ["Data Sensitivity", "Sensitivity of data handled"],
            ["Security Controls", "Implemented security measures"]
        ]
    },
    "Risk Materiality Level": {
        "headers": ["Field", "Description"],
        "rows": [
            ["Risk Level", "Overall risk assessment"],
            ["Impact Score", "Potential impact measurement"],
            ["Mitigation Status", "Status of risk mitigation measures"]
        ]
    },
    "System Resiliency": {
        "headers": ["Field", "Description"],
        "rows": [
            ["Availability Target", "System uptime target"],
            ["Recovery Time", "Expected recovery time"],
            ["Redundancy Level", "System redundancy measures"]
        ]
    },
    "Hosting and System Dependencies": {
        "headers": ["Field", "Description"],
        "rows": [
            ["Hosting Environment", "System hosting location"],
            ["Dependencies", "External system dependencies"],
            ["Integration Points", "System integration details"]
        ]
    },
    "Central Programmes": {
        "headers": ["Field", "Description"],
        "rows": [
            ["Programme Name", "Name of central programme"],
            ["Programme Status", "Current programme status"],
            ["Integration Status", "System integration status"]
        ]
    }
}

# Store the selected node in session state
if 'selected_node' not in st.session_state:
    st.session_state.selected_node = None

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

# Initialize PyVis network
net = Network(height="700px", width="100%", directed=True, notebook=True)

# Add nodes to PyVis network
for node, attrs in G.nodes(data=True):
    net.add_node(node, 
                 color=attrs['color'],
                 size=attrs['size'],
                 shape=attrs['shape'],
                 title=attrs['title'],
                 label=attrs['label'])

# Add edges to PyVis network
for source, target, edge_attrs in G.edges(data=True):
    net.add_edge(source, target, 
                 title=edge_attrs['title'],
                 label=edge_attrs['label'],
                 arrows=edge_attrs['arrows'])

# Set options
net.set_options('''
{
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
}
''')

# JavaScript for node highlighting and communication
highlight_js = """
network.on("click", function(params) {
    if (params.nodes.length > 0) {
        var selectedNode = params.nodes[0];
        window.parent.postMessage({
            type: 'node_clicked',
            node: selectedNode
        }, '*');
        
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

handle_message_js = """
<script>
window.addEventListener('message', function(event) {
    if (event.data.type === 'node_clicked') {
        const node = event.data.node;
        window.parent.Streamlit.setComponentValue(node);
    }
});
</script>
"""

# Display the graph in the first column
with col1:
    with tempfile.TemporaryDirectory() as temp_dir:
        path = os.path.join(temp_dir, "graph.html")
        net.save_graph(path)
        
        with open(path, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        html_content = html_content.replace('</body>', f'{handle_message_js}<script>{highlight_js}</script></body>')
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
            st.info(f"No detailed information available for {node_name}")
    else:
        st.info("Click on a node to view its details")
