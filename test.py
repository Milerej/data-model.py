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
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("⚠️ Password incorrect")
        return False
    else:
        return True

if check_password():
    st.set_page_config(page_title="Interactive Dependency Graph", layout="wide")
    st.title("🔄 System Dependencies Visualization")

    # Add the view toggle and physics toggle
    col1, col2 = st.columns(2)
    with col1:
        view_type = st.toggle("Enable Hierarchical Layout", False)
    with col2:
        physics_enabled = st.toggle("Enable Physics", False)

    # Define color schemes
    COLOR_SCHEMES = {
        "system": "#1B5E20",
        "dependency": "#2E7D32"
    }

    # Define mock systems and their attributes
    entities = {
        "System A": {
            "color": "#E41A1C",  # Red
            "size": 30,
            "shape": "dot",
            "title": "Critical Payment System",
            "level": 1
        },
        "System B": {
            "color": "#377EB8",  # Blue
            "size": 30,
            "shape": "dot",
            "title": "Authentication System",
            "level": 2
        },
        "System C": {
            "color": "#4DAF4A",  # Green
            "size": 30,
            "shape": "dot",
            "title": "Document Management System",
            "level": 2
        },
        "System D": {
            "color": "#984EA3",  # Purple
            "size": 30,
            "shape": "dot",
            "title": "Email System",
            "level": 3
        },
        "System E": {
            "color": "#FF7F00",  # Orange
            "size": 30,
            "shape": "dot",
            "title": "Database System",
            "level": 3
        },
        "System F": {
            "color": "#FFFF33",  # Yellow
            "size": 30,
            "shape": "dot",
            "title": "Reporting System",
            "level": 2
        },
        "System G": {
            "color": "#A65628",  # Brown
            "size": 30,
            "shape": "dot",
            "title": "API Gateway",
            "level": 2
        },
        "System H": {
            "color": "#F781BF",  # Pink
            "size": 30,
            "shape": "dot",
            "title": "Monitoring System",
            "level": 4
        }
    }

    # Define mock dependencies with clearer parent-child relationships
    edges = [
        # Level 1 (Top Level Systems)
        ("System A", "System B", "Requires authentication", "to"),
        ("System A", "System E", "Stores transaction data", "to"),
        ("System A", "System G", "API access", "to"),
        
        # Level 2 Systems
        ("System B", "System E", "User data storage", "to"),
        ("System B", "System H", "Security monitoring", "to"),
        
        # Level 3 Systems
        ("System C", "System B", "User authentication", "to"),
        ("System C", "System E", "Document storage", "to"),
        ("System C", "System G", "API access", "to"),
        
        # Level 4 Systems
        ("System D", "System B", "User verification", "to"),
        ("System D", "System C", "Document attachment", "to"),
        ("System D", "System H", "Email monitoring", "to"),
        
        # Cross-level dependencies
        ("System E", "System H", "Database monitoring", "to"),
        ("System F", "System A", "Payment data", "to"),
        ("System F", "System E", "Analytics data", "to"),
        ("System G", "System B", "API authentication", "to"),
        ("System G", "System H", "API monitoring", "to"),
        ("System H", "System E", "Logs storage", "to")
    ]

    # Create NetworkX graph
    G = nx.DiGraph()
    for node, attributes in entities.items():
        G.add_node(node, **attributes)

    # Add edges
    for source, target, title, arrow in edges:
        G.add_edge(source, target, title=title, arrows=arrow)

    # Create PyVis network
    net = Network(height="900px", width="100%", directed=True)
    net.from_nx(G)

    if view_type:
        net.set_options("""{
            "layout": {
                "hierarchical": {
                    "enabled": true,
                    "direction": "UD",
                    "sortMethod": "directed",
                    "nodeSpacing": 150,
                    "levelSeparation": 150,
                    "treeSpacing": 200,
                    "blockShifting": true,
                    "edgeMinimization": true,
                    "parentCentralization": true,
                    "shakeTowards": "roots"
                }
            },
            "physics": {
                "enabled": true,
                "hierarchicalRepulsion": {
                    "centralGravity": 0.0,
                    "springLength": 100,
                    "springConstant": 0.01,
                    "nodeDistance": 120,
                    "damping": 0.09
                },
                "solver": "hierarchicalRepulsion",
                "stabilization": {
                    "enabled": true,
                    "iterations": 1000,
                    "updateInterval": 100,
                    "onlyDynamicEdges": false,
                    "fit": true
                }
            },
            "edges": {
                "smooth": {
                    "type": "cubicBezier",
                    "forceDirection": "vertical",
                    "roundness": 0.4
                },
                "arrows": {
                    "to": {
                        "enabled": true,
                        "scaleFactor": 0.5
                    }
                }
            },
            "interaction": {
                "dragNodes": true,
                "dragView": true,
                "zoomView": true
            }
        }""")
    else:
        net.set_options(f"""{{
            "layout": {{
                "randomSeed": 42
            }},
            "physics": {{
                "enabled": {str(physics_enabled).lower()},
                "stabilization": {{
                    "enabled": true,
                    "iterations": 2000,
                    "updateInterval": 50,
                    "fit": true
                }},
                "barnesHut": {{
                    "gravitationalConstant": -2000,
                    "centralGravity": 0.3,
                    "springLength": 200,
                    "springConstant": 0.04,
                    "damping": 0.09,
                    "avoidOverlap": 0.1
                }},
                "minVelocity": 0.75,
                "maxVelocity": 30
            }},
            "edges": {{
                "smooth": {{
                    "type": "continuous",
                    "roundness": 0.5
                }},
                "arrows": {{
                    "to": {{
                        "enabled": true,
                        "scaleFactor": 0.5
                    }}
                }},
                "color": {{
                    "inherit": false,
                    "color": "#666666",
                    "opacity": 0.8
                }}
            }},
            "interaction": {{
                "hover": true,
                "navigationButtons": true,
                "keyboard": {{
                    "enabled": true
                }},
                "dragNodes": true,
                "dragView": true,
                "zoomView": true
            }}
        }}""")

    # Save and display the network
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as tmp_file:
            net.save_graph(tmp_file.name)
            with open(tmp_file.name, 'r', encoding='utf-8') as f:
                html_content = f.read()

            fullscreen_html = """
            <button 
                style="
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    z-index: 10000;
                    padding: 8px 16px;
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    font-family: Arial, sans-serif;
                    font-size: 14px;
                "
                onclick="toggleFullscreen()"
            >
                Full Screen
            </button>
            <script>
                function toggleFullscreen() {
                    let elem = document.documentElement;
                    if (!document.fullscreenElement) {
                        if (elem.requestFullscreen) {
                            elem.requestFullscreen();
                        } else if (elem.webkitRequestFullscreen) {
                            elem.webkitRequestFullscreen();
                        } else if (elem.msRequestFullscreen) {
                            elem.msRequestFullscreen();
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
            </script>
            """

            modified_html = html_content.replace('</body>', f'{fullscreen_html}</body>')
            components.html(modified_html, height=900)
            os.unlink(tmp_file.name)

        # Add legend
        st.sidebar.markdown("## System Legend")
        for node, attrs in entities.items():
            st.sidebar.markdown(
                f'<div style="display: flex; align-items: center;">'
                f'<div style="width: 20px; height: 20px; background-color: {attrs["color"]}; '
                f'border-radius: 50%; margin-right: 10px;"></div>'
                f'<div>{node}: {attrs["title"]}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    except Exception as e:
        st.error(f"An error occurred while generating the graph: {str(e)}")
