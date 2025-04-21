import streamlit as st
from pyvis.network import Network
import networkx as nx
import streamlit.components.v1 as components
import tempfile
import os
import random

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

    # Define color palette for systems
    colors = [
        "#E41A1C", "#377EB8", "#4DAF4A", "#984EA3", "#FF7F00",
        "#FFFF33", "#A65628", "#F781BF", "#1F77B4", "#FF7F0E",
        "#2CA02C", "#D62728", "#9467BD", "#8C564B", "#E377C2"
    ]

    # Generate 200 systems with random levels (1-4)
    entities = {}
    for i in range(1, 201):
        entities[f"System {i}"] = {
            "color": random.choice(colors),
            "size": 20,
            "shape": "dot",
            "title": f"System {i}",
            "level": random.randint(1, 4)
        }

    # Generate edges (each system connects to 2-4 other systems)
    edges = []
    systems = list(entities.keys())
    for system in systems:
        current_level = entities[system]["level"]
        # Connect to 2-4 random systems in higher levels
        num_connections = random.randint(2, 4)
        possible_targets = [s for s in systems if entities[s]["level"] > current_level]
        if possible_targets:
            targets = random.sample(possible_targets, min(num_connections, len(possible_targets)))
            for target in targets:
                edges.append((system, target, f"Connects to {target}", "to"))

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

    net.set_options("""{
        "layout": {
            "randomSeed": 42,
            "improvedLayout": true
        },
        "physics": {
            "enabled": true,
            "forceAtlas2Based": {
                "gravitationalConstant": -50,
                "centralGravity": 0.01,
                "springLength": 100,
                "springConstant": 0.08,
                "damping": 0.4,
                "avoidOverlap": 1
            },
            "solver": "forceAtlas2Based",
            "stabilization": {
                "enabled": true,
                "iterations": 1000,
                "updateInterval": 100,
                "fit": true
            }
        },
        "edges": {
            "smooth": {
                "type": "continuous",
                "roundness": 0.5
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
            },
            "dragNodes": true,
            "dragView": true,
            "zoomView": true,
            "multiselect": true
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

    except Exception as e:
        st.error(f"An error occurred while generating the graph: {str(e)}")
