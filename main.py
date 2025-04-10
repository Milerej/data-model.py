import streamlit as st
from pyvis.network import Network
import networkx as nx
import streamlit.components.v1 as components
import html

st.set_page_config(page_title="Interactive Interdependency Graph", layout="wide")

st.title("🧠 Interactive Data Model Interdependency Chart")

# Define entity modules with additional information
entities = {
    "Ministry Family": {
        "color": "blue",
        "fields": ["Ministry ID", "Ministry Name", "Description"],
        "type": "Entity"
    },
    "Agency": {
        "color": "blue",
        "fields": ["Agency ID", "Agency Name", "Ministry", "Status"],
        "type": "Entity"
    },
    "System Overview": {
        "color": "teal",
        "fields": ["System ID", "System Name", "Description", "Status"],
        "type": "Entity"
    },
    # Add similar structure for other entities...
}

# Function to create HTML table for node
def create_node_table(node_name, entity_info):
    table_html = f"""
    <table border="1" style="background-color: {entity_info['color']}; border-collapse: collapse; width: 200px;">
        <tr>
            <th style="text-align: center; padding: 5px; border: 1px solid black;">
                {node_name}
            </th>
        </tr>
        <tr>
            <td style="padding: 5px; border: 1px solid black;">
                <ul style="margin: 0; padding-left: 20px;">
                    {''.join(f'<li>{field}</li>' for field in entity_info['fields'])}
                </ul>
            </td>
        </tr>
    </table>
    """
    return html.escape(table_html)

# Create NetworkX graph
G = nx.DiGraph()
for node, info in entities.items():
    G.add_node(node, 
               title=create_node_table(node, info),
               color=info['color'],
               shape='box')  # Use box shape for tables

# Define and add edges (keep your existing edges code)
edges = [
    ("Agency", "System Overview", "relates to"),
    # ... your existing edges ...
]

for source, target, label in edges:
    G.add_edge(source, target, title=label, label=label)

# Create interactive PyVis network with modified settings
net = Network(height="700px", width="100%", directed=True)
net.from_nx(G)
net.repulsion(node_distance=300, central_gravity=0.2)  # Increased node distance for tables

# Customize nodes and edges
for node in net.nodes:
    node["shape"] = "box"
    node["font"] = {"size": 12}
    node["margin"] = 10
    
for edge in net.edges:
    edge["label"] = edge["title"]
    edge["font"] = {"size": 10}

# Add custom CSS for better table display
custom_css = """
<style>
    .node-table {
        border-collapse: collapse;
        background-color: white;
    }
    .node-table th {
        background-color: #f0f0f0;
        padding: 5px;
    }
    .node-table td {
        padding: 3px;
    }
</style>
"""

# Save and display in Streamlit
net.save_graph("graph.html")
with open("graph.html", "r", encoding='utf-8') as f:
    html_content = custom_css + f.read()
components.html(html_content, height=750, scrolling=True)

# Add legend
st.sidebar.title("Legend")
for entity, info in entities.items():
    st.sidebar.markdown(
        f'<div style="background-color:{info["color"]};width:20px;height:20px;display:inline-block"></div> '
        f'{entity} ({info["type"]})', 
        unsafe_allow_html=True
    )
