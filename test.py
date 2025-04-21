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

    # Add the view toggle
    view_type = st.toggle("Enable Hierarchical Layout", False)

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
            "title": "Critical Payment System"
        },
        "System B": {
            "color": "#377EB8",  # Blue
            "size": 30,
            "shape": "dot",
            "title": "Authentication System"
        },
        "System C": {
            "color": "#4DAF4A",  # Green
            "size": 30,
            "shape": "dot",
            "title": "Document Management System"
        },
        "System D": {
            "color": "#984EA3",  # Purple
            "size": 30,
            "shape": "dot",
            "title": "Email System"
        },
        "System E": {
            "color": "#FF7F00",  # Orange
            "size": 30,
            "shape": "dot",
            "title": "Database System"
        },
        # Additional mock systems
        "System F": {
            "color": "#FFFF33",  # Yellow
            "size": 30,
            "shape": "dot",
            "title": "Reporting System"
        },
        "System G": {
            "color": "#A65628",  # Brown
            "size": 30,
            "shape": "dot",
            "title": "API Gateway"
        },
        "System H": {
            "color": "#F781BF",  # Pink
            "size": 30,
            "shape": "dot",
            "title": "Monitoring System"
        }
    }

    # Define mock dependencies
    edges = [
        # System A dependencies
        ("System A", "System B", "Requires authentication", "to"),
        ("System A", "System E", "Stores transaction data", "to"),
        ("System A", "System G", "API access", "to"),
        
        # System B dependencies
        ("System B", "System E", "User data storage", "to"),
        ("System B", "System H", "Security monitoring", "to"),
        
        # System C dependencies
        ("System C", "System B", "User authentication", "to"),
        ("System C", "System E", "Document storage", "to"),
        ("System C", "System G", "API access", "to"),
        
        # System D dependencies
        ("System D", "System B", "User verification", "to"),
        ("System D", "System C", "Document attachment", "to"),
        ("System D", "System H", "Email monitoring", "to"),
        
        # System E dependencies
        ("System E", "System H", "Database monitoring", "to"),
        
        # System F dependencies
        ("System F", "System A", "Payment data", "to"),
        ("System F", "System E", "Analytics data", "to"),
        
        # System G dependencies
        ("System G", "System B", "API authentication", "to"),
        ("System G", "System H", "API monitoring", "to"),
        
        # System H dependencies
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
                    "nodeSpacing": 200,
                    "levelSeparation": 200
                }
            },
            "physics": {
                "hierarchicalRepulsion": {
                    "centralGravity": 0.5,
                    "springLength": 150,
                    "springConstant": 0.3,
                    "nodeDistance": 200,
                    "damping": 0.09
                }
            }
        }""")
    else:
        net.set_options("""{
            "layout": {
                "randomSeed": 42
            },
            "physics": {
                "forceAtlas2Based": {
                    "gravitationalConstant": -50,
                    "centralGravity": 0.01,
                    "springLength": 200,
                    "springConstant": 0.08,
                    "damping": 0.4,
                    "avoidOverlap": 1
                },
                "maxVelocity": 50,
                "minVelocity": 0.1,
                "solver": "forceAtlas2Based",
                "stabilization": {
                    "enabled": true,
                    "iterations": 1000,
                    "updateInterval": 100
                }
            },
            "edges": {
                "smooth": {
                    "type": "curvedCW",
                    "roundness": 0.2
                },
                "arrows": {
                    "to": {
                        "enabled": true,
                        "scaleFactor": 0.5
                    }
                },
                "color": {
                    "inherit": false,
                    "color": "#666666",
                    "opacity": 0.8
                }
            },
            "interaction": {
                "hover": true,
                "navigationButtons": true,
                "keyboard": {
                    "enabled": true
                }
            }
        }""")

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
