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
        "title": "\n".join([
            "Fields:",
            "• Classification Level",
            "• Data Sensitivity",
            "• Security Controls",
            "• Access Requirements",
            "• Data Protection Measures"
        ])
    },
    "Risk Materiality Level": {
        "color": "#4CAF50", 
        "size": 25, 
        "shape": "dot",
        "title": "\n".join([
            "Fields:",
            "• Risk Level",
            "• Impact Score",
            "• Probability Rating",
            "• Mitigation Status",
            "• Risk Assessment Date"
        ])
    }
}

# Define edges with PK/FK relationships
edges = [
    ("System Management", "System Overview", "PK: System_ID", "both"),
    ("System Management", "Criticality Assessment", "PK: System_ID", "both"),
    ("System Management", "Security & Sensitivity Classification", "PK: System_ID", "both"),
    ("System Management", "Risk Materiality Level", "PK: System_ID", "both")
]

# Define table data
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
            ["Security Controls", "Implemented security measures"],
            ["Access Requirements", "Access control requirements"],
            ["Data Protection", "Data protection measures"]
        ]
    },
    "Risk Materiality Level": {
        "headers": ["Field", "Description"],
        "rows": [
            ["Risk Level", "Overall risk assessment"],
            ["Impact Score", "Potential impact measurement"],
            ["Probability Rating", "Likelihood of risk occurrence"],
            ["Mitigation Status", "Status of risk mitigation measures"],
            ["Assessment Date", "Date of last risk assessment"]
        ]
    }
}

# Initialize session state
if 'selected_node' not in st.session_state:
    st.session_state.selected_node = None

# Initialize PyVis network
net = Network(notebook=True, cdn_resources='remote')
net.width = "100%"
net.height = "700px"
net.bgcolor = "#ffffff"
net.font_color = True

# Add nodes to network
for node, attributes in entities.items():
    net.add_node(node,
                 color=attributes["color"],
                 size=attributes["size"],
                 shape=attributes["shape"],
                 title=attributes["title"],
                 label=node)

# Add edges to network
for source, target, label, direction in edges:
    net.add_edge(source, target, title=label, label=label, arrows=direction)

# Set network options
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
        }
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
        }
    },
    "interaction": {
        "hover": true,
        "tooltipDelay": 100
    }
}
''')

# Generate HTML file
try:
    with tempfile.NamedTemporaryFile(delete=False, suffix='.html', mode='w', encoding='utf-8') as f:
        net.save_graph(f.name)
        with open(f.name, 'r', encoding='utf-8') as saved_file:
            html_content = saved_file.read()
        
        # Add custom JavaScript
        html_content = html_content.replace('</head>', '''
            <script>
            window.addEventListener('message', function(event) {
                if (event.data.type === 'node_clicked') {
                    window.parent.Streamlit.setComponentValue(event.data.node);
                }
            });
            </script>
            </head>
        ''')
        
        html_content = html_content.replace('</body>', '''
            <script>
            network.on("click", function(params) {
                if (params.nodes.length > 0) {
                    var selectedNode = params.nodes[0];
                    window.parent.postMessage({
                        type: 'node_clicked',
                        node: selectedNode
                    }, '*');
                }
            });
            </script>
            </body>
        ''')

    # Display network in first column
    with col1:
        st.components.v1.html(html_content, height=750)

    # Display table in second column
    with col2:
        if st.session_state.get('selected_node'):
            node_name = st.session_state.selected_node
            if node_name in table_data:
                st.subheader(f"{node_name} Details")
                table = table_data[node_name]
                st.table(pd.DataFrame(table["rows"], columns=table["headers"]))
            else:
                st.info(f"No detailed information available for {node_name}")
        else:
            st.info("Click on a node to view its details")

finally:
    try:
        os.unlink(f.name)
    except:
        pass
