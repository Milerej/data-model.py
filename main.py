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

# [Previous entities, edges, and table_data definitions remain the same]

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
            "iterations": 1000
        }
    },
    "edges": {
        "smooth": {
            "type": "continuous"
        }
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
