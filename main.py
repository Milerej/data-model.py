import streamlit as st
from pyvis.network import Network
import networkx as nx
import streamlit.components.v1 as components
import tempfile
import os

# Set page config
st.set_page_config(page_title="Interactive Interdependency Graph", layout="wide")

# Add title
st.title("⚙️ Data Model : System Management")

# Define entities dictionary
entities = {
    "System Management": {
        "color": "#2E7D32",
        "size": 35,
        "shape": "dot",
        "title": "System Management Module"
    },
    "System Overview": {
        "color": "#4CAF50",
        "size": 25,
        "shape": "dot",
        "title": "System Overview Sub-Module"
    },
    "Criticality Assessment": {
        "color": "#4CAF50",
        "size": 25,
        "shape": "dot",
        "title": "Criticality Assessment Sub-Module"
    },
    "Security & Sensitivity Classification": {
        "color": "#4CAF50",
        "size": 25,
        "shape": "dot",
        "title": "Security & Sensitivity Classification Sub-Module"
    },
    "Risk Materiality Level": {
        "color": "#4CAF50",
        "size": 25,
        "shape": "dot",
        "title": "Risk Materiality Level Sub-Module"
    },
    "System Resiliency": {
        "color": "#4CAF50",
        "size": 25,
        "shape": "dot",
        "title": "System Resiliency Sub-Module"
    },
    "Hosting and System Dependencies": {
        "color": "#4CAF50",
        "size": 25,
        "shape": "dot",
        "title": "Hosting and System Dependencies Sub-Module"
    }
}

# Define edges
edges = [
    ("System Management", "System Overview", "contains", "to"),
    ("System Management", "Criticality Assessment", "contains", "to"),
    ("System Management", "Security & Sensitivity Classification", "contains", "to"),
    ("System Management", "Risk Materiality Level", "contains", "to"),
    ("System Management", "System Resiliency", "contains", "to"),
    ("System Management", "Hosting and System Dependencies", "contains", "to")
]

# Create columns for layout
col1, col2 = st.columns(2)

# Column 1 content
with col1:
    st.header("Interactive Graph")
    
    # Create NetworkX graph
    G = nx.DiGraph()
    for node, attributes in entities.items():
        G.add_node(node, **attributes)

    # Add edges
    for source, target, label, direction in edges:
        G.add_edge(source, target, title=label, arrows=direction)

    # Create PyVis network
    net = Network(height="700px", width="100%", directed=True, notebook=True)
    net.from_nx(G)
    
    # Set options for better visualization
    net.set_options('{' + '''
        "physics": {
            "enabled": true,
            "stabilization": {
                "enabled": true,
                "iterations": 1000
            }
        },
        "edges": {
            "smooth": true,
            "color": {
                "inherit": false,
                "color": "#2E7D32"
            }
        }
    ''' + '}')

    # Save and display the graph
    with tempfile.TemporaryDirectory() as temp_dir:
        path = os.path.join(temp_dir, "graph.html")
        net.save_graph(path)
        with open(path, "r", encoding="utf-8") as f:
            components.html(f.read(), height=750)

# Column 2 content
with col2:
    st.header("Sub-modules and Fields (List View)")
    
    # Create a new NetworkX graph for the list view
    G_list = nx.DiGraph()
    
    # Add main module
    G_list.add_node("System Management", **{
        "color": "#2E7D32",
        "size": 35,
        "shape": "dot",
        "title": "System Management Module",
        "label": "System Management"
    })
    
    # Add sub-modules
    sub_modules = {
        "System Overview": [],
        "Criticality Assessment": [],
        "Security & Sensitivity Classification": [],
        "Risk Materiality Level": [],
        "System Resiliency": [],
        "Hosting and System Dependencies": []
    }
    
    # Add sub-modules to graph and collect fields
    for sub_module in sub_modules.keys():
        G_list.add_node(sub_module, **{
            "color": "#4CAF50",
            "size": 25,
            "shape": "dot",
            "title": entities[sub_module]["title"],
            "label": sub_module
        })
        G_list.add_edge("System Management", sub_module)
        
        # Collect fields for each sub-module
        fields_html = ""
        for source, target, label, _ in edges:
            if source == sub_module and label == "contains":
                fields_html += f"• {target}<br>"
                sub_modules[sub_module].append(target)
        
        if fields_html:
            # Add fields as HTML in the node title
            G_list.nodes[sub_module]["title"] = f"<h3>{sub_module}</h3><p>{fields_html}</p>"

    # Create interactive PyVis network for list view
    net_list = Network(height="700px", width="100%", directed=True, notebook=True)
    net_list.from_nx(G_list)
    
    # Set options for the list view
    net_list.set_options('{' + '''
        "physics": {
            "enabled": true,
            "stabilization": {
                "enabled": true,
                "iterations": 1000,
                "updateInterval": 25
            },
            "hierarchicalRepulsion": {
                "centralGravity": 0.0,
                "springLength": 200,
                "springConstant": 0.01,
                "nodeDistance": 250,
                "damping": 0.09
            }
        },
        "edges": {
            "smooth": {
                "type": "continuous",
                "forceDirection": "none"
            },
            "color": {
                "inherit": false,
                "color": "#2E7D32",
                "opacity": 0.8
            },
            "width": 1.5
        },
        "nodes": {
            "font": {
                "size": 16,
                "strokeWidth": 2,
                "strokeColor": "#ffffff"
            },
            "scaling": {
                "min": 20,
                "max": 35
            }
        },
        "layout": {
            "hierarchical": {
                "enabled": true,
                "direction": "UD",
                "sortMethod": "directed",
                "nodeSpacing": 200,
                "levelSeparation": 200
            }
        },
        "interaction": {
            "hover": true,
            "tooltipDelay": 0
        }
    ''' + '}')

    # Create a temporary directory and save the list view graph
    with tempfile.TemporaryDirectory() as temp_dir:
        path = os.path.join(temp_dir, "graph_list.html")
        net_list.save_graph(path)
        
        with open(path, "r", encoding="utf-8") as f:
            html_content_list = f.read()
        
        components.html(html_content_list, height=750, scrolling=True)
