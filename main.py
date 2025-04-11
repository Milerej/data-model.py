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

[... previous entities and table_data definitions remain the same ...]

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

[... previous options and JavaScript definitions remain the same ...]

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
            st.info(f"No detailed information available for {node_name}")
    else:
        st.info("Click on a node to view its details")
