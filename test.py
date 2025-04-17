import streamlit as st
from pyvis.network import Network
import networkx as nx
import streamlit.components.v1 as components
import tempfile
import os

# This MUST be the first Streamlit command
st.set_page_config(page_title="Interactive Interdependency Graph", layout="wide")

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
    st.title("⚙️ Entity Relationship Diagram : System Management and Agency Management Data Model (V2.2)")
    
    # Add the view toggle
    view_type = st.toggle("Enable Hierarchical Layout", False)

    # Define standardised settings
    NODE_SETTINGS = {
        "module": {
            "size": 50,
            "shape": "dot"
        },
        "submodule": {
            "size": 35,
            "shape": "dot"
        },
        "subgroup": {
            "size": 25,
            "shape": "dot"
        },
        "field": {
            "size": 15,
            "shape": "dot"
        }
    }

    COLOR_SCHEMES = {
        "system_management": {
            "module": "#1B5E20",      # Darkest green
            "submodule": "#2E7D32",   # Dark green
            "subgroup": "#388E3C",    # Medium green
            "field": "#43A047"        # Light green
        },
        "agency_management": {
            "module": "#1A237E",      # Darkest blue
            "submodule": "#283593",   # Dark blue
            "subgroup": "#303F9F",    # Medium blue
            "field": "#3949AB"        # Light blue
        }
    }

    # Complete entities dictionary with all nodes
    entities = {
        # Root node
        "DGP 2.0": {
            "color": "#1A237E",  # Dark blue color
            "size": 60,  # Larger than module size
            "shape": NODE_SETTINGS["module"]["shape"],
            "title": "DGP 2.0 Root"
        },
    
        # System Management Module and related nodes
        "System Management": {
            "color": COLOR_SCHEMES["system_management"]["module"],
            "size": NODE_SETTINGS["module"]["size"],
            "shape": NODE_SETTINGS["module"]["shape"],
            "title": "System Management Module"
        },
        "System Identity & Classification": {
            "color": COLOR_SCHEMES["system_management"]["submodule"],
            "size": NODE_SETTINGS["submodule"]["size"],
            "shape": NODE_SETTINGS["submodule"]["shape"],
            "title": "System Identity & Classification Sub-Module"
        },
        "Criticality & Risk": {
            "color": COLOR_SCHEMES["system_management"]["submodule"],
            "size": NODE_SETTINGS["submodule"]["size"],
            "shape": NODE_SETTINGS["submodule"]["shape"],
            "title": "Criticality & Risk Sub-Module"
        },
        "System Resilience": {
            "color": COLOR_SCHEMES["system_management"]["submodule"],
            "size": NODE_SETTINGS["submodule"]["size"],
            "shape": NODE_SETTINGS["submodule"]["shape"],
            "title": "System Resilience Sub-Module"
        },
        "Hosting and System Dependencies": {
            "color": COLOR_SCHEMES["system_management"]["submodule"],
            "size": NODE_SETTINGS["submodule"]["size"],
            "shape": NODE_SETTINGS["submodule"]["shape"],
            "title": "Hosting and System Dependencies Sub-Module"
        },

            # Agency Management Module and related nodes
        "Agency Management": {
            "color": COLOR_SCHEMES["agency_management"]["module"],
            "size": NODE_SETTINGS["module"]["size"],
            "shape": NODE_SETTINGS["module"]["shape"],
            "title": "Agency Management Module"
        },
        "Agency": {
            "color": COLOR_SCHEMES["agency_management"]["submodule"],
            "size": NODE_SETTINGS["submodule"]["size"],
            "shape": NODE_SETTINGS["submodule"]["shape"],
            "title": "Agency Sub-Module"
        },
        "Key Appointment Holder": {
            "color": COLOR_SCHEMES["agency_management"]["submodule"],
            "size": NODE_SETTINGS["submodule"]["size"],
            "shape": NODE_SETTINGS["submodule"]["shape"],
            "title": "Key Appointment Holder Sub-Module"
        },

        # System Management Subgroups
        "Basic Information": {
            "color": COLOR_SCHEMES["system_management"]["subgroup"],
            "size": NODE_SETTINGS["subgroup"]["size"],
            "shape": NODE_SETTINGS["subgroup"]["shape"],
            "title": "Basic Information Sub-Group"
        },
        "Organizational Context": {
            "color": COLOR_SCHEMES["system_management"]["subgroup"],
            "size": NODE_SETTINGS["subgroup"]["size"],
            "shape": NODE_SETTINGS["subgroup"]["shape"],
            "title": "Organizational Context Sub-Group"
        },
        "Classification": {
            "color": COLOR_SCHEMES["system_management"]["subgroup"],
            "size": NODE_SETTINGS["subgroup"]["size"],
            "shape": NODE_SETTINGS["subgroup"]["shape"],
            "title": "Classification Sub-Group"
        },
        "Impact Assessment": {
            "color": COLOR_SCHEMES["system_management"]["subgroup"],
            "size": NODE_SETTINGS["subgroup"]["size"],
            "shape": NODE_SETTINGS["subgroup"]["shape"],
            "title": "Impact Assessment Sub-Group"
        },
        "Risk Profile": {
            "color": COLOR_SCHEMES["system_management"]["subgroup"],
            "size": NODE_SETTINGS["subgroup"]["size"],
            "shape": NODE_SETTINGS["subgroup"]["shape"],
            "title": "Risk Profile Sub-Group"
        },
        "SCA/RML Approval": {
            "color": COLOR_SCHEMES["system_management"]["subgroup"],
            "size": NODE_SETTINGS["subgroup"]["size"],
            "shape": NODE_SETTINGS["subgroup"]["shape"],
            "title": "SCA/RML Approval Sub-Group"
        },
        "Availability & Recovery": {
            "color": COLOR_SCHEMES["system_management"]["subgroup"],
            "size": NODE_SETTINGS["subgroup"]["size"],
            "shape": NODE_SETTINGS["subgroup"]["shape"],
            "title": "Availability & Recovery Sub-Group"
        },
        "Dependencies Management": {
            "color": COLOR_SCHEMES["system_management"]["subgroup"],
            "size": NODE_SETTINGS["subgroup"]["size"],
            "shape": NODE_SETTINGS["subgroup"]["shape"],
            "title": "Dependencies Management Sub-Group"
        },

            # Fields for both modules
        # Agency Management Fields
        "Agency Name": {
            "color": COLOR_SCHEMES["agency_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Agency Name field"
        },
        "Agency Abbreviation (Short Form)": {
            "color": COLOR_SCHEMES["agency_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Agency Abbreviation field"
        },
        "Agency Operational Status": {
            "color": COLOR_SCHEMES["agency_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Agency Operational Status field"
        },
        "Ministry Family": {
            "color": COLOR_SCHEMES["agency_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Ministry Family field"
        },
        "Full Name": {
            "color": COLOR_SCHEMES["agency_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Full Name field"
        },
        "Designation": {
            "color": COLOR_SCHEMES["agency_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Designation field"
        },
        "Email": {
            "color": COLOR_SCHEMES["agency_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Email field"
        },

        # System Management Fields
        "System ID": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "System ID field"
        },
        "System Name": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "System Name field"
        },
        "System Description": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "System Description field"
        },
        "System Status": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "System Status field"
        },
        "System Classification": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "System Classification field"
        },
        "Impact Level": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Impact Level field"
        },
        "Risk Level": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Risk Level field"
        },
        "SCA Status": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "SCA Status field"
        },
        "RML Status": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "RML Status field"
        },
        "System Availability": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "System Availability field"
        },
        "Recovery Time": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Recovery Time field"
        },
        "Dependencies": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Dependencies field"
        }
    }

    # Complete edges list
    edges = [
        # Root node connections
        ("DGP 2.0", "System Management", "", ""),
        ("DGP 2.0", "Agency Management", "", ""),
    
        # System Management Module relationships
        ("System Management", "System Identity & Classification", "", ""),
        ("System Management", "Criticality & Risk", "", ""),
        ("System Management", "System Resilience", "", ""),
        ("System Management", "Hosting and System Dependencies", "", ""),

        # System Identity & Classification relationships
        ("System Identity & Classification", "Basic Information", "", ""),
        ("System Identity & Classification", "Organizational Context", "", ""),
        ("System Identity & Classification", "Classification", "", ""),

        # Criticality & Risk relationships
        ("Criticality & Risk", "Impact Assessment", "", ""),
        ("Criticality & Risk", "Risk Profile", "", ""),
        ("Criticality & Risk", "SCA/RML Approval", "", ""),

        # System Resilience relationships
        ("System Resilience", "Availability & Recovery", "", ""),

        # Hosting and System Dependencies relationships
        ("Hosting and System Dependencies", "Dependencies Management", "", ""),

        # Agency Management Module relationships
        ("Agency Management", "Agency", "", ""),
        ("Agency Management", "Key Appointment Holder", "", ""),

        # Field relationships for Basic Information
        ("Basic Information", "System ID", "", ""),
        ("Basic Information", "System Name", "", ""),
        ("Basic Information", "System Description", "", ""),
        ("Basic Information", "System Status", "", ""),

        # Field relationships for Organizational Context
        ("Organizational Context", "Agency Name", "", ""),

        # Field relationships for Classification
        ("Classification", "System Classification", "", ""),

        # Field relationships for Impact Assessment
        ("Impact Assessment", "Impact Level", "", ""),

        # Field relationships for Risk Profile
        ("Risk Profile", "Risk Level", "", ""),

        # Field relationships for SCA/RML Approval
        ("SCA/RML Approval", "SCA Status", "", ""),
        ("SCA/RML Approval", "RML Status", "", ""),

        # Field relationships for Availability & Recovery
        ("Availability & Recovery", "System Availability", "", ""),
        ("Availability & Recovery", "Recovery Time", "", ""),

        # Field relationships for Dependencies Management
        ("Dependencies Management", "Dependencies", "", ""),

        # Field relationships for Agency
        ("Agency", "Agency Name", "", ""),
        ("Agency", "Agency Abbreviation (Short Form)", "", ""),
        ("Agency", "Agency Operational Status", "", ""),
        ("Agency", "Ministry Family", "", ""),

        # Field relationships for Key Appointment Holder
        ("Key Appointment Holder", "Full Name", "", ""),
        ("Key Appointment Holder", "Designation", "", ""),
        ("Key Appointment Holder", "Email", "", ""),

        # Cross-module relationships
        #("Agency Name", "Agency", "", ""),
        #("Dependencies", "System ID", "", "")
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

    # Add edges
    for source, target, label, direction in edges:
        G.add_edge(source, target, title=label, label=label, arrows=direction)

    # Create PyVis network
    net = Network(height="900px", width="100%", directed=True)
    net.from_nx(G)

    # Set hierarchical layout options based on toggle
    if view_type:
        net.set_options("""{
            "layout": {
                "hierarchical": {
                    "enabled": true,
                    "direction": "UD",
                    "sortMethod": "directed",
                    "nodeSpacing": 200,
                    "levelSeparation": 200,
                    "treeSpacing": 200,
                    "blockShifting": false,
                    "edgeMinimization": false,
                    "parentCentralization": false,
                    "shakeTowards": "roots"
                }
            },
            "physics": {
                "enabled": true,
                "hierarchicalRepulsion": {
                    "centralGravity": 0.5,
                    "springLength": 150,
                    "springConstant": 0.3,
                    "nodeDistance": 200,
                    "damping": 0.09,
                    "avoidOverlap": 1
                },
                "stabilization": {
                    "enabled": true,
                    "iterations": 2000,
                    "updateInterval": 100,
                    "fit": true
                }
            },
            "edges": {
                "smooth": {
                    "type": "cubicBezier",
                    "forceDirection": "vertical",
                    "roundness": 0.5
                },
                "color": {
                    "inherit": false,
                    "color": "#2E7D32",
                    "opacity": 0.8
                }
            },
            "nodes": {
                "fixed": {
                    "x": false,
                    "y": true
                },
                "shape": "dot",
                "size": 25,
                "font": {
                    "size": 14
                }
            },
            "interaction": {
                "dragNodes": true,
                "dragView": true,
                "zoomView": true
            },
            "groups": {
                "useDefaultGroups": false
            }
        }""")
    else:
        net.set_options("""{
            "layout": {
                "hierarchical": {
                    "enabled": false
                }
            },
            "physics": {
                "enabled": true,
                "barnesHut": {
                    "gravitationalConstant": -60000,
                    "centralGravity": 0.1,
                    "springLength": 200,
                    "springConstant": 0.08,
                    "damping": 0.12,
                    "avoidOverlap": 1
                }
            },
            "edges": {
                "smooth": {
                    "type": "curvedCW",
                    "roundness": 0.2
                },
                "color": {
                    "inherit": false,
                    "color": "#2E7D32",
                    "opacity": 0.8
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
    except Exception as e:
        st.error(f"An error occurred while generating the graph: {str(e)}")


import streamlit as st
from pyvis.network import Network
import networkx as nx
import streamlit.components.v1 as components

st.set_page_config(page_title="Interactive Interdependency Graph", layout="wide")

st.title("🧠 Interactive Data Model Interdependency Chart")

# Define entity modules and colors
entities = {
    "Ministry Family": "blue",
    "Agency": "blue",
    "System Overview": "teal",
    "Criticality Assessment": "teal",
    "Policy": "red",
    "Policy Waivers": "red",
    "Supplier Profile": "purple",
    "Supplier Risk Management": "purple",
    "Supplier Contracts": "purple",
    "Actions Against Errant Supplier": "purple",
    "Supplier Performance Feedback": "purple",
    "Bulk Tender ECN Details": "purple",
    "EDH Agency": "purple",
    "Risk Assessments": "orange",
    "Risk Treatments": "orange",
    "Audit Findings": "gray",
    "System Management": "green",
    "Security & Sensitivity Classification": "green",
    "Risk Materiality Level": "green",
    "System Resiliency": "green",
    "Hosting and System Dependencies": "green",
    "Central Programmes": "green"
}

# Define edges with PK/FK relationships - all with bidirectional arrows
edges = [
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
    # System Management relationships
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

# Create NetworkX graph
G = nx.DiGraph()
for node, color in entities.items():
    G.add_node(node, title=node, color=color)

# Add edges with labels and custom arrow directions
for source, target, label, direction in edges:
    G.add_edge(source, target, title=label, label=label, arrows=direction)

# Create interactive PyVis network
net = Network(height="700px", width="100%", directed=True)
net.from_nx(G)
net.repulsion(node_distance=200, central_gravity=0.3)

# Customize edge labels and arrows
for edge in net.edges:
    edge["label"] = edge["title"]
    if edge["arrows"] == "both":
        edge["arrows"] = "to,from"
    else:
        edge["arrows"] = edge["arrows"]

# Save and display in Streamlit
net.save_graph("graph.html")
components.html(open("graph.html", "r", encoding='utf-8').read(), height=750, scrolling=True)



