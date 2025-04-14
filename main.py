import streamlit as st
from pyvis.network import Network
import networkx as nx
import streamlit.components.v1 as components
import tempfile
import os

# Page config and Streamlit element hiding
st.set_page_config(
    page_title="Interactive Interdependency Graph",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit elements
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .stApp > header {display: none;}
        .main > .block-container {
            padding-top: 0;
            padding-bottom: 0;
            max-width: 100%;
        }
    </style>
""", unsafe_allow_html=True)

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == "Showmethemoney":
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True

if check_password():
    st.title("⚙️ Data Model : System Management")

    # Define entity modules and colors
    entities = {
        "System Management": {
            "color": "#2E7D32", 
            "size": 35, 
            "shape": "dot",
            "title": "System Management Module"
        },
        # Main Modules
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
        },

            # System Overview Fields
        "Agency": {"color": "#81C784", "size": 15, "shape": "dot", "title": "Agency field"},
        "Ministry Family": {"color": "#81C784", "size": 15, "shape": "dot", "title": "Ministry Family field"},
        "System ID": {"color": "#81C784", "size": 15, "shape": "dot", "title": "System ID (Primary Key)"},
        "System Name": {"color": "#81C784", "size": 15, "shape": "dot", "title": "System Name field"},
        "System Description": {"color": "#81C784", "size": 15, "shape": "dot", "title": "System Description field"},
        "System Status": {"color": "#81C784", "size": 15, "shape": "dot", "title": "System Status field"},

        # Add all other entity definitions as in the original code...
        # [Previous entity definitions remain the same]
    }

    # Define edges with PK/FK relationships
    edges = [
        # [Previous edge definitions remain the same]
    ]

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

    # Create interactive PyVis network with full viewport height
    net = Network(height="100vh", width="100%", directed=True, notebook=True)
    net.from_nx(G)

    # Set options for better spacing and reduced overlapping
    net.set_options('{' + '''
        "physics": {
            "enabled": true,
            "stabilization": {
                "enabled": true,
                "iterations": 2000,
                "updateInterval": 25,
                "onlyDynamicEdges": false,
                "fit": true
            },
            "barnesHut": {
                "gravitationalConstant": -60000,
                "centralGravity": 0.1,
                "springLength": 2000,
                "springConstant": 0.08,
                "damping": 0.12,
                "avoidOverlap": 20
            },
            "minVelocity": 0.75,
            "maxVelocity": 30
        },
        "edges": {
            "smooth": {
                "type": "curvedCW",
                "roundness": 0.2,
                "forceDirection": "horizontal"
            },
            "length": 300,
            "font": {
                "size": 11,
                "strokeWidth": 2,
                "strokeColor": "#ffffff"
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
                "size": 12,
                "strokeWidth": 2,
                "strokeColor": "#ffffff"
            },
            "margin": 12,
            "scaling": {
                "min": 10,
                "max": 30
            },
            "fixed": {
                "x": false,
                "y": false
            }
        },
        "layout": {
            "improvedLayout": true,
            "randomSeed": 42,
            "hierarchical": {
                "enabled": false,
                "nodeSpacing": 300,
                "levelSeparation": 300,
                "treeSpacing": 300
            }
        }
    ''' + '}')

    # Customize edge labels and arrows
    for edge in net.edges:
        edge["label"] = edge.get("title", "")
        if edge.get("arrows") == "both":
            edge["arrows"] = "to,from"

    # Add JavaScript for highlighting
    highlight_js = """
    network.on("click", function(params) {
        if (params.nodes.length > 0) {
            var selectedNode = params.nodes[0];
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

    # Add enhanced CSS for fullscreen and layout
    st.markdown("""
        <style>
            .fullscreen-button {
                position: absolute;
                top: 10px;
                right: 10px;
                z-index: 1000;
                padding: 10px;
                background: #2E7D32;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            .fullscreen-button:hover {
                background: #1B5E20;
            }
            .element-container iframe {
                height: 100vh !important;
                width: 100vw !important;
                position: fixed !important;
                top: 0 !important;
                left: 0 !important;
                z-index: 99 !important;
            }
            .main > .block-container {
                padding-top: 0;
                padding-bottom: 0;
                max-width: 100%;
            }
        </style>
    """, unsafe_allow_html=True)

    # Create a temporary directory and save the graph
    with tempfile.TemporaryDirectory() as temp_dir:
        path = os.path.join(temp_dir, "graph.html")
        net.save_graph(path)
        
        with open(path, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        # Add fullscreen button and JavaScript
        html_content = html_content.replace('</body>', '''
            <button class="fullscreen-button" onclick="toggleFullScreen()">Toggle Fullscreen</button>
            <script>
                function toggleFullScreen() {
                    const iframe = document.querySelector('iframe');
                    if (!document.fullscreenElement) {
                        iframe.requestFullscreen().catch(err => {
                            alert(`Error attempting to enable fullscreen: ${err.message}`);
                        });
                    } else {
                        document.exitFullscreen();
                    }
                }
            </script>
            ''' + f'<script>{highlight_js}</script></body>')
        
        # Display the graph with maximum dimensions
        components.html(html_content, height=1000, width=1000, scrolling=False)

else:
    st.stop()  # Don't run the rest of the app
