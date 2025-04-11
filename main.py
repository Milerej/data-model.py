import streamlit as st
from pyvis.network import Network
import networkx as nx
import streamlit.components.v1 as components

# Basic page setup
st.set_page_config(page_title="Interactive Interdependency Graph", layout="wide")
st.title("🧠 Interactive Data Model Interdependency Chart")

# Simplified entities with just a few examples
entities = {
    "Ministry Family": {
        "color": "blue",
        "fields": [
            {"name": "Ministry_ID", "is_key": True},
            {"name": "Ministry_Name", "is_key": False}
        ]
    },
    "Agency": {
        "color": "blue",
        "fields": [
            {"name": "Agency_ID", "is_key": True},
            {"name": "Ministry_ID", "is_foreign_key": True, "references": "Ministry Family"}
        ]
    }
}

# Create basic network
G = nx.DiGraph()

# Add nodes
for node, info in entities.items():
    G.add_node(node, color=info['color'])

# Add basic edges
G.add_edge("Agency", "Ministry Family", title="References")

# Create and configure network
net = Network(height="500px", width="100%", directed=True)
net.from_nx(G)
net.repulsion(node_distance=200, central_gravity=0.2)

# Save and display
try:
    net.save_graph("graph.html")
    with open("graph.html", "r", encoding='utf-8') as f:
        components.html(f.read(), height=500)
except Exception as e:
    st.error(f"Error: {str(e)}")

# Simple legend
st.sidebar.title("Legend")
for entity, info in entities.items():
    st.sidebar.markdown(f"- {entity}")
