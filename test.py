#Part 1 - Imports and Initial Setup:
import streamlit as st
from pyvis.network import Network
import networkx as nx
import streamlit.components.v1 as components
import tempfile
import os
import json
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Interactive Interdependency Graph",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        margin-bottom: 10px;
    }
    .reportview-container {
        background: #f0f2f6
    }
    </style>
    """, unsafe_allow_html=True)
 
#Part 2 - Password Protection and Configuration:
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

# Add session state initialization
if 'graph_data' not in st.session_state:
    st.session_state.graph_data = {}
 
#Part 3 - Add new functionality for graph controls:
def add_graph_controls():
    """Add controls for graph manipulation"""
    with st.sidebar:
        st.header("Graph Controls")
        
        # Layout controls
        st.subheader("Layout Settings")
        view_type = st.toggle("Enable Hierarchical Layout", False)
        
        # Filter controls
        st.subheader("Filter Options")
        filter_module = st.multiselect(
            "Filter by Module",
            ["System Management", "Agency Management"],
            default=["System Management", "Agency Management"]
        )
        
        # Search functionality
        st.subheader("Search")
        search_term = st.text_input("Search nodes", "")
        
        # Export options
        st.subheader("Export Options")
        if st.button("Export Graph Data"):
            export_graph_data()
            
    return view_type, filter_module, search_term

def export_graph_data():
    """Export graph data to JSON"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"graph_data_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(st.session_state.graph_data, f)
    
st.sidebar.success(f"Data exported to {filename}")
 
#Part 4 - Node and Edge Configuration:
def create_node_settings():
    """Create standardized node settings"""
    return {
        "module": {
            "size": 50,
            "shape": "dot",
            "font": {"size": 20, "face": "Arial"}
        },
        "submodule": {
            "size": 35,
            "shape": "dot",
            "font": {"size": 16, "face": "Arial"}
        },
        "subgroup": {
            "size": 25,
            "shape": "dot",
            "font": {"size": 14, "face": "Arial"}
        },
        "field": {
            "size": 15,
            "shape": "dot",
            "font": {"size": 12, "face": "Arial"}
        }
    }

def create_color_schemes():
    """Create color schemes for different modules"""
    return {
        "system_management": {
            "module": "#1B5E20",
            "submodule": "#2E7D32",
            "subgroup": "#388E3C",
            "field": "#43A047",
            "edge": "#2E7D32"
        },
        "agency_management": {
            "module": "#1A237E",
            "submodule": "#283593",
            "subgroup": "#303F9F",
            "field": "#3949AB",
            "edge": "#1A237E"
        }
    }

def apply_node_styling(node_data, node_settings, color_schemes):
    """Apply styling to nodes based on their type"""
    styled_nodes = {}
    for node_name, attributes in node_data.items():
        node_type = attributes.get("type", "field")
        module_type = attributes.get("module", "system_management")
        
        styled_nodes[node_name] = {
            "color": color_schemes[module_type][node_type],
            "size": node_settings[node_type]["size"],
            "shape": node_settings[node_type]["shape"],
            "font": node_settings[node_type]["font"],
            "title": attributes.get("title", node_name)
        }
    return styled_nodes
 
#Part 5 - Graph Creation and Manipulation:
def create_network_graph(entities, edges, view_type, filter_modules, search_term):
    """Create and configure the network graph"""
    # Create NetworkX graph
    G = nx.DiGraph()
    
    # Filter nodes based on modules and search term
    filtered_entities = {
        k: v for k, v in entities.items()
        if any(module in v.get("module", "") for module in filter_modules)
        and search_term.lower() in k.lower()
    }
    
    # Add nodes to graph
    for node, attributes in filtered_entities.items():
        G.add_node(node, **attributes)
    
    # Add filtered edges
    filtered_edges = [
        (source, target, attrs) for source, target, attrs in edges
        if source in filtered_entities and target in filtered_entities
    ]
    
    for source, target, attrs in filtered_edges:
        G.add_edge(source, target, **attrs)
    
    # Create PyVis network
    net = Network(height="900px", width="100%", directed=True)
    net.from_nx(G)
    
    # Configure layout options
    configure_layout(net, view_type)
    
    return net

def configure_layout(net, view_type):
    """Configure the layout settings for the network"""
    if view_type:
        # Hierarchical layout options
        layout_options = {
            "layout": {
                "hierarchical": {
                    "enabled": True,
                    "direction": "UD",
                    "sortMethod": "directed",
                    "nodeSpacing": 200,
                    "levelSeparation": 200
                }
            }
        }
    else:
        # Force-directed layout options
        layout_options = {
            "layout": {
                "hierarchical": {
                    "enabled": False
                }
            },
            "physics": {
                "barnesHut": {
                    "gravitationalConstant": -60000,
                    "centralGravity": 0.1,
                    "springLength": 200
                }
            }
        }
    
    net.set_options(json.dumps(layout_options))
 
#Part 6 - Main Application Logic:
def main():
    """Main application function"""
    if not check_password():
        return
        
    st.title("⚙️ Data Model : System Management and Agency Management V2.3")
    
    # Initialize settings
    node_settings = create_node_settings()
    color_schemes = create_color_schemes()
    
    # Add controls
    view_type, filter_modules, search_term = add_graph_controls()
    
    # Style nodes
    styled_entities = apply_node_styling(entities, node_settings, color_schemes)
    
    try:
        # Create network
        net = create_network_graph(styled_entities, edges, view_type, filter_modules, search_term)
        
        # Display network
        display_network(net)
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

def display_network(net):
    """Display the network graph with fullscreen capability"""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as tmp_file:
        net.save_graph(tmp_file.name)
        with open(tmp_file.name, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Add fullscreen button
        fullscreen_button = create_fullscreen_button()
        modified_html = html_content.replace('</body>', f'{fullscreen_button}</body>')
        
        # Display graph
        components.html(modified_html, height=900)
        os.unlink(tmp_file.name)

def create_fullscreen_button():
    """Create HTML/JS for fullscreen button"""
    return """
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

if __name__ == "__main__":
    main()
