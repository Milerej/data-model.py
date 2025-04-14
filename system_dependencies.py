import streamlit as st
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
import tempfile
import os

def show_system_dependencies():
    st.title("🔄 System Dependencies Visualization")
    
    # Sample data - replace with your actual system dependencies data
    systems = {
        "System A": {
            "color": "#1976D2",
            "size": 30,
            "shape": "dot",
            "title": "Core System A"
        },
        "System B": {
            "color": "#1976D2",
            "size": 30,
            "shape": "dot",
            "title": "Core System B"
        },
        "System C": {
            "color": "#1976D2",
            "size": 30,
            "shape": "dot",
            "title": "Core System C"
        }
    }

    # Sample dependencies
    dependencies = [
        ("System A", "System B", "Depends on", "to"),
        ("System B", "System C", "Provides data to", "to"),
        ("System C", "System A", "Updates", "to")
    ]

    # Create NetworkX graph
    G = nx.DiGraph()
    
    # Add nodes
    for system, attributes in systems.items():
        node_attrs = {
            "color": attributes["color"],
            "size": attributes["size"],
            "shape": attributes["shape"],
            "title": attributes["title"],
            "label": system
        }
        G.add_node(system, **node_attrs)

    # Add edges
    for source, target, label, direction in dependencies:
        G.add_edge(source, target, title=label, label=label, arrows=direction)

    # Create PyVis network
    net = Network(height="900px", width="100%", directed=True, notebook=True)
    net.from_nx(G)

    # Set options
    net.set_options("""
    {
        "physics": {
            "enabled": true,
            "forceAtlas2Based": {
                "gravitationalConstant": -50,
                "centralGravity": 0.01,
                "springLength": 200,
                "springConstant": 0.08
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
                "type": "continuous",
                "forceDirection": "none"
            },
            "color": {
                "inherit": false,
                "color": "#1976D2",
                "opacity": 0.8
            },
            "width": 2,
            "arrows": {
                "to": {
                    "enabled": true,
                    "scaleFactor": 0.5
                }
            },
            "font": {
                "size": 12,
                "align": "middle"
            }
        },
        "nodes": {
            "font": {
                "size": 14,
                "face": "arial"
            },
            "borderWidth": 2,
            "borderWidthSelected": 4,
            "scaling": {
                "min": 20,
                "max": 40
            }
        },
        "interaction": {
            "hover": true,
            "navigationButtons": true,
            "keyboard": {
                "enabled": true
            }
        }
    }
    """)

    # Save and display
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as tmp_file:
            net.save_graph(tmp_file.name)
            with open(tmp_file.name, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Add fullscreen button
            fullscreen_html = """
            <button 
                style="
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    z-index: 10000;
                    padding: 8px 16px;
                    background-color: #1976D2;
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

    # Add controls
    st.sidebar.subheader("Visualization Controls")
    st.sidebar.write("Add your custom controls here")
