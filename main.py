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
        st.error("⚠️ Password incorrect")
        return False
    else:
        # Password correct.
        return True

if check_password():
    st.set_page_config(page_title="Interactive Interdependency Graph", layout="wide")

    # FIRST CHART
    st.title("⚙️ Data Model : System Management")

    # Define entity modules and colors for first chart
    entities = {
        "System Management": {
            "color": "#2E7D32", 
            "size": 50, 
            "shape": "dot",
            "title": "System Management Module"
        },
        # [Your existing entities dictionary content]
        # Main Modules, Sub-groups, and Fields as in your original code
    }

    # Define edges for first chart
    edges = [
        # [Your existing edges list]
        # All the edges from your original code
    ]

    # Create NetworkX graph for first chart
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

    # Add edges with labels and custom arrow directions for first chart
    for source, target, label, direction in edges:
        G.add_edge(source, target, title=label, label=label, arrows=direction)

    # Create interactive PyVis network for first chart
    net = Network(height="900px", width="100%", directed=True, notebook=True)
    net.from_nx(G)

    # Set options for first chart
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

    # Save and display first chart
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
                onclick="toggleFullscreen1()"
            >
                Full Screen
            </button>
            <script>
                function toggleFullscreen1() {
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
        st.error(f"An error occurred while generating the first graph: {str(e)}")

    # Add divider between charts
    st.markdown("---")

    # SECOND CHART
    st.title("🧠 Interactive Data Model Interdependency Chart")

    # Define entity modules and colors for second chart
    entities_2 = {
        "Ministry Family": {"color": "blue", "size": 25, "shape": "dot", "title": "Ministry Family"},
        "Agency": {"color": "blue", "size": 25, "shape": "dot", "title": "Agency"},
        "System Overview": {"color": "teal", "size": 25, "shape": "dot", "title": "System Overview"},
        "Criticality Assessment": {"color": "teal", "size": 25, "shape": "dot", "title": "Criticality Assessment"},
        "Policy": {"color": "red", "size": 25, "shape": "dot", "title": "Policy"},
        "Policy Waivers": {"color": "red", "size": 25, "shape": "dot", "title": "Policy Waivers"},
        "Supplier Profile": {"color": "purple", "size": 25, "shape": "dot", "title": "Supplier Profile"},
        "Supplier Risk Management": {"color": "purple", "size": 25, "shape": "dot", "title": "Supplier Risk Management"},
        "Supplier Contracts": {"color": "purple", "size": 25, "shape": "dot", "title": "Supplier Contracts"},
        "Actions Against Errant Supplier": {"color": "purple", "size": 25, "shape": "dot", "title": "Actions Against Errant Supplier"},
        "Supplier Performance Feedback": {"color": "purple", "size": 25, "shape": "dot", "title": "Supplier Performance Feedback"},
        "Bulk Tender ECN Details": {"color": "purple", "size": 25, "shape": "dot", "title": "Bulk Tender ECN Details"},
        "EDH Agency": {"color": "purple", "size": 25, "shape": "dot", "title": "EDH Agency"},
        "Risk Assessments": {"color": "orange", "size": 25, "shape": "dot", "title": "Risk Assessments"},
        "Risk Treatments": {"color": "orange", "size": 25, "shape": "dot", "title": "Risk Treatments"},
        "Audit Findings": {"color": "gray", "size": 25, "shape": "dot", "title": "Audit Findings"},
        "System Management": {"color": "green", "size": 25, "shape": "dot", "title": "System Management"},
        "Security & Sensitivity Classification": {"color": "green", "size": 25, "shape": "dot", "title": "Security & Sensitivity Classification"},
        "Risk Materiality Level": {"color": "green", "size": 25, "shape": "dot", "title": "Risk Materiality Level"},
        "System Resiliency": {"color": "green", "size": 25, "shape": "dot", "title": "System Resiliency"},
        "Hosting and System Dependencies": {"color": "green", "size": 25, "shape": "dot", "title": "Hosting and System Dependencies"},
        "Central Programmes": {"color": "green", "size": 25, "shape": "dot", "title": "Central Programmes"}
    }

    # Define edges for second chart
    edges_2 = [
        ("Agency", "System Overview", "FK: Agency_ID", "both"),
        ("Agency", "Ministry Family", "FK: Ministry_ID", "both"),
        ("System Overview", "Criticality Assessment", "FK: System_ID", "both"),
        ("System Overview", "Policy", "FK: Policy_ID", "both"),
        ("Policy", "Policy Waivers", "FK: Policy_ID", "both"),
        ("Supplier Profile", "Supplier Risk Management", "FK: Supplier_ID", "both"),
        ("Supplier Profile", "Supplier Contracts", "FK: Supplier_ID", "both"),
        ("Supplier Profile", "Actions Against Errant Supplier", "FK: Supplier_ID", "both"),
        ("Supplier Profile", "Supplier Performance Feedback", "FK: Supplier_ID", "both"),
        ("Supplier Profile", "Bulk Tender ECN Details", "FK: Supplier_ID", "both"),
        ("Supplier Profile", "EDH Agency", "FK: Supplier_ID", "both"),
        ("Risk Assessments", "Risk Treatments", "FK: Assessment_ID", "both"),
        ("Audit Findings", "Risk Treatments", "FK: Finding_ID", "both"),
        ("Supplier Risk Management", "Risk Assessments", "FK: Risk_ID", "both"),
        ("Supplier Performance Feedback", "Supplier Risk Management", "FK: Feedback_ID", "both"),
        ("Actions Against Errant Supplier", "Supplier Contracts", "FK: Action_ID", "both"),
        ("System Overview", "Supplier Contracts", "FK: System_ID", "both"),
        ("System Overview", "Audit Findings", "FK: System_ID", "both"),
        ("System Management", "System Overview", "FK: System_ID", "both"),
        ("System Management", "Criticality Assessment", "FK: System_ID", "both"),
        ("System Management", "Security & Sensitivity Classification", "FK: System_ID", "both"),
        ("System Management", "Risk Materiality Level", "FK: System_ID", "both"),
        ("System Management", "System Resiliency", "FK: System_ID", "both"),
        ("System Management", "Hosting and System Dependencies", "FK: System_ID", "both"),
        ("System Management", "Central Programmes", "FK: System_ID", "both"),
        ("System Management", "Supplier Contracts", "FK: System_ID", "both"),
        ("Supplier Contracts", "Hosting and System Dependencies", "FK: Contract_ID", "both")
    ]

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

    # Save and display second chart
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as tmp_file:
            net2.save_graph(tmp_file.name)
            with open(tmp_file.name, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            fullscreen_html = """
            <button 
                style="
                    position: fixed;
                    bottom: 20px;
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
                onclick="toggleFullscreen2()"
            >
                Full Screen
            </button>
            <script>
                function toggleFullscreen2() {
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
            components.html(modified_html, height=700)
            os.unlink(tmp_file.name)
    except Exception as e:
        st.error(f"An error occurred while generating the second graph: {str(e)}")
