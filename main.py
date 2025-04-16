import time
import streamlit as st
from pyvis.network import Network
import networkx as nx
import streamlit.components.v1 as components
import tempfile
import os

# Clear cache at start
st.cache_data.clear()
st.cache_resource.clear()

# Add timestamp to session state
if 'last_update' not in st.session_state:
    st.session_state['last_update'] = time.time()

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
        st.error("⚠️ Password incorrect")
        return False
    else:
        # Password correct.
        return True

@st.cache_data(ttl=1)  # Cache expires after 1 second
def create_network_data():
    # Your first chart entities and edges
    entities = {
        "System Management": {
            "color": "#2E7D32", 
            "size": 50, 
            "shape": "dot",
            "title": "System Management Module"
        },
        # ... [rest of your entities dictionary]
    }
    
    edges = [
        # ... [your edges list]
    ]
    
    return entities, edges, time.time()

@st.cache_data(ttl=1)
def create_network_data_2():
    # Your second chart entities and edges
    entities_2 = {
        "Ministry Family": {"color": "blue", "size": 25, "shape": "dot", "title": "Ministry Family"},
        # ... [rest of your entities_2 dictionary]
    }
    
    edges_2 = [
        # ... [your edges_2 list]
    ]
    
    return entities_2, edges_2, time.time()

def display_network(net, height=900, position="top"):
    """Function to display the network with fullscreen capability"""
    timestamp = str(time.time()).replace('.', '')
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=f'_{timestamp}.html', encoding='utf-8') as tmp_file:
        net.save_graph(tmp_file.name)
        with open(tmp_file.name, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        button_position = "top: 20px;" if position == "top" else "bottom: 20px;"
        
        fullscreen_html = f"""
        <button 
            style="
                position: fixed;
                {button_position}
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
            onclick="toggleFullscreen_{timestamp}()"
        >
            Full Screen
        </button>
        <script>
            function toggleFullscreen_{timestamp}() {{
                let elem = document.documentElement;
                if (!document.fullscreenElement) {{
                    if (elem.requestFullscreen) {{
                        elem.requestFullscreen();
                    }} else if (elem.webkitRequestFullscreen) {{
                        elem.webkitRequestFullscreen();
                    }} else if (elem.msRequestFullscreen) {{
                        elem.msRequestFullscreen();
                    }}
                }} else {{
                    if (document.exitFullscreen) {{
                        document.exitFullscreen();
                    }} else if (document.webkitExitFullscreen) {{
                        document.webkitExitFullscreen();
                    }} else if (document.msExitFullscreen) {{
                        document.msExitFullscreen();
                    }}
                }}
            }}
        </script>
        """
        
        modified_html = html_content.replace('</body>', f'{fullscreen_html}</body>')
        
        components.html(modified_html, height=height, key=f"graph_{timestamp}")
        
    try:
        os.unlink(tmp_file.name)
    except:
        pass

# Main code
if check_password():
    st.set_page_config(page_title="Interactive Interdependency Graph", layout="wide")
    
    # Add refresh button in the same row as title
    col1, col2 = st.columns([6, 1])
    with col1:
        st.title("⚙️ Data Model : System Management")
    with col2:
        if st.button('Refresh Graphs', key=f"refresh_{time.time()}"):
            st.session_state['last_update'] = time.time()
            st.experimental_rerun()

    # FIRST CHART
    try:
        # Get data from cached function
        entities, edges, timestamp = create_network_data()
        
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

        # Set options for better spacing and reduced overlapping
        net.set_options("""
        {
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
                    "springLength": 1000,
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
        }
        """)

        # Display the first network
        display_network(net, height=900, position="top")

    except Exception as e:
        st.error(f"An error occurred while generating the first graph: {str(e)}")

    # Add divider between charts
    st.markdown("---")

    # SECOND CHART
    st.title("🧠 Interactive Data Model Interdependency Chart")

    try:
        # Get data from cached function
        entities_2, edges_2, timestamp_2 = create_network_data_2()

        # Create NetworkX graph for second chart
        G2 = nx.DiGraph()
        for node, attributes in entities_2.items():
            G2.add_node(node, **attributes)

        # Add edges for second chart
        for source, target, label, direction in edges_2:
            G2.add_edge(source, target, title=label, label=label, arrows=direction)

        # Create interactive PyVis network for second chart
        net2 = Network(height="700px", width="100%", directed=True, notebook=True)
        net2.from_nx(G2)

        # Set options for second chart
        net2.set_options("""
        {
            "physics": {
                "enabled": true,
                "stabilization": {
                    "enabled": true,
                    "iterations": 2000,
                    "updateInterval": 25
                },
                "barnesHut": {
                    "gravitationalConstant": -2000,
                    "centralGravity": 0.3,
                    "springLength": 200,
                    "springConstant": 0.04,
                    "damping": 0.09,
                    "avoidOverlap": 1
                }
            },
            "edges": {
                "smooth": {
                    "type": "continuous",
                    "forceDirection": "none"
                },
                "color": {
                    "inherit": "both"
                },
                "width": 1.5
            }
        }
        """)

        # Display the second network
        display_network(net2, height=700, position="bottom")

    except Exception as e:
        st.error(f"An error occurred while generating the second graph: {str(e)}")

    # Add auto-refresh using JavaScript
    auto_refresh_script = """
    <script>
        function autoRefresh() {
            window.location.reload();
        }
        setTimeout(autoRefresh, 60000); // Refresh every 60 seconds
    </script>
    """
    components.html(auto_refresh_script, height=0)
