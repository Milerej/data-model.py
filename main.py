import streamlit as st
from pyvis.network import Network
import networkx as nx
import streamlit.components.v1 as components
import tempfile
import os

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
    st.set_page_config(page_title="Interactive Interdependency Graph", layout="wide")

    st.title("⚙️ Data Model : System Management")

    # [Your existing entities dictionary remains the same]
    entities = {
        # ... [Keep your existing entities dictionary exactly as is]
    }

    # [Your existing edges list remains the same]
    edges = [
        # ... [Keep your existing edges list exactly as is]
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

    # Create interactive PyVis network
    net = Network(height="900px", width="100%", directed=True, notebook=True)
    net.from_nx(G)

    # [Your existing network options remain the same]
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

    # Add fullscreen JavaScript
    fullscreen_js = """
    function toggleFullScreen() {
        const container = document.querySelector('.graph-container');
        if (!document.fullscreenElement) {
            if (container.requestFullscreen) {
                container.requestFullscreen();
            } else if (container.webkitRequestFullscreen) {
                container.webkitRequestFullscreen();
            } else if (container.msRequestFullscreen) {
                container.msRequestFullscreen();
            }
        } else {
            if (document.exitFullscreen) {
                document.exitFullscreen();
            } else if (document.webkitExitFullscreen) {
                document.webkitExitFullscreen();
            } else if (document.msExitFullscreen) {
                document.msExitFullscreen();
            }
        }
    }
    """

    # Add CSS styles
    st.markdown("""
        <style>
            .graph-container {
                position: relative;
                width: 100%;
                height: 900px;
            }
            .fullscreen-button {
                position: absolute;
                top: 10px;
                right: 10px;
                z-index: 1000;
                padding: 8px 16px;
                background: #2E7D32;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 14px;
                transition: background-color 0.3s;
            }
            .fullscreen-button:hover {
                background: #1B5E20;
            }
            .graph-container:fullscreen {
                background: white;
                width: 100vw;
                height: 100vh;
            }
        </style>
    """, unsafe_allow_html=True)

    # Create a temporary directory and save the graph
    with tempfile.TemporaryDirectory() as temp_dir:
        path = os.path.join(temp_dir, "graph.html")
        net.save_graph(path)
        
        with open(path, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        # Wrap the content in a container and add the fullscreen button
        modified_html = f"""
        <div class="graph-container">
            <button class="fullscreen-button" onclick="toggleFullScreen()">
                Toggle Fullscreen
            </button>
            {html_content}
        </div>
        <script>{fullscreen_js}</script>
        <script>{highlight_js}</script>
        """
        
        # Display the modified graph
        components.html(modified_html, height=900, scrolling=True)

else:
    st.stop()  # Don't run the rest of the app
