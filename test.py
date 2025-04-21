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
    st.set_page_config(page_title="Interactive Interdependency Graph", layout="wide")
    st.title("⚙️ Data Model : System Management and Agency Management (V2.4)")

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
            "color": "#808080",  # Grey color
            "size": 80,  # Larger than module size
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




            # Agency Management submodules
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
        "Risk Materiality Level": {
            "color": COLOR_SCHEMES["system_management"]["subgroup"],
            "size": NODE_SETTINGS["subgroup"]["size"],
            "shape": NODE_SETTINGS["subgroup"]["shape"],
            "title": "Risk Materiality Level Sub-Group"
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




            # System Management Fields - Basic Information
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
        "Operational Date": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Operational Date field"
        },
        "Decommission Date": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Decommission Date field"
        },

        # System Management Fields - Classification
        "Security Classification": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Security Classification field"
        },
        "Sensitivity Classification": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Sensitivity Classification field"
        },

        # System Management Fields - Impact Assessment
        "Economy": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Economy field"
        },
        "Public Health and Safety": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Public Health and Safety field"
        },
        "National Security": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "National Security field"
        },
        "Social Preparedness": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Social Preparedness field"
        },
        "Public Service": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Public Service field"
        },




            # System Management Fields - Risk Materiality Level
        "System Criticality": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "System Criticality field"
        },
        "Designated CII": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Designated CII field"
        },
        "Computed RML": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Computed RML field"
        },
        "Computed RML Date": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Computed RML Date field"
        },
        "Agency Proposed RML": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Agency Proposed RML field"
        },
        "RML Alignment": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "RML Alignment field"
        },
        "RML Justification": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "RML Justification field"
        },
        "Endorsed RML": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Endorsed RML field"
        },
        "RML Endorsement Date": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "RML Endorsement Date field"
        },
        "Endorsement Comments": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Endorsement Comments field"
        },
        "IDSC Approval Date": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "IDSC Approval Date field"
        },
        "IDSC Approval Attachment": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "IDSC Approval Attachment field"
        },
        "MHA Approval": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "MHA Approval field"
        },
        "CSA Approval": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "CSA Approval field"
        },
        "SNDGO Approval": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "SNDGO Approval field"
        },




            # System Management Fields - Additional Approval Fields
        "MHA Comments": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "MHA Comments field"
        },
        "CSA Comments": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "CSA Comments field"
        },
        "SNDGO Comments": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "SNDGO Comments field"
        },

        # System Management Fields - System Resilience
        "Service Availability": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Service Availability field"
        },
        "RTO": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "RTO field"
        },
        "RPO": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "RPO field"
        },

        # System Management Fields - Dependencies
        "Dependency ID": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Dependency ID field"
        },
        "Dependency Status": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Dependency Status field"
        },
        "Dependency Type": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Dependency Type field"
        },
        "Dependent System": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Dependent System field"
        },

        "Downstream Dependency": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Downstream Dependency field"
        },



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

        # Basic Information field connections
        ("Basic Information", "System ID", "", ""),
        ("Basic Information", "System Name", "", ""),
        ("Basic Information", "System Description", "", ""),
        ("Basic Information", "System Status", "", ""),
        ("Basic Information", "Operational Date", "", ""),
        ("Basic Information", "Decommission Date", "", ""),




            # Organizational Context field connections
        ("Organizational Context", "Agency Name", "", ""),

        # Classification field connections
        ("Classification", "Security Classification", "", ""),
        ("Classification", "Sensitivity Classification", "", ""),

        # Criticality & Risk relationships
        ("Criticality & Risk", "Impact Assessment", "", ""),
        ("Criticality & Risk", "Risk Materiality Level", "", ""),
        ("Criticality & Risk", "SCA/RML Approval", "", ""),

        # Impact Assessment field connections
        ("Impact Assessment", "Economy", "", ""),
        ("Impact Assessment", "Public Health and Safety", "", ""),
        ("Impact Assessment", "National Security", "", ""),
        ("Impact Assessment", "Social Preparedness", "", ""),
        ("Impact Assessment", "Public Service", "", ""),
        ("Impact Assessment", "Designated CII", "", ""),
        ("Economy", "System Criticality", "", ""),
        ("Public Health and Safety", "System Criticality", "", ""),
        ("National Security", "System Criticality", "", ""),
        ("Social Preparedness", "System Criticality", "", ""),
        ("Public Service", "System Criticality", "", ""),
        ("Designated CII", "System Criticality", "", ""),



        # Risk Materiality Level field connections
        ("Risk Materiality Level", "Computed RML", "", ""),
        ("Risk Materiality Level", "Computed RML Date", "", ""),
        ("Risk Materiality Level", "Agency Proposed RML", "", ""),
        ("Risk Materiality Level", "RML Alignment", "", ""),
        ("Risk Materiality Level", "RML Justification", "", ""),


        # SCA/RML Approval field connections
        ("SCA/RML Approval", "Endorsed RML", "", ""),
        ("SCA/RML Approval", "RML Endorsement Date", "", ""),
        ("SCA/RML Approval", "Endorsement Comments", "", ""),
        ("SCA/RML Approval", "IDSC Approval Date", "", ""),
        ("SCA/RML Approval", "IDSC Approval Attachment", "", ""),
        ("SCA/RML Approval", "MHA Approval", "", ""),
        ("SCA/RML Approval", "CSA Approval", "", ""),
        ("SCA/RML Approval", "SNDGO Approval", "", ""),
        ("SCA/RML Approval", "MHA Comments", "", ""),
        ("SCA/RML Approval", "CSA Comments", "", ""),
        ("SCA/RML Approval", "SNDGO Comments", "", ""),

        # System Resilience relationships
        ("System Resilience", "Availability & Recovery", "", ""),

        # Availability & Recovery field connections
        ("Availability & Recovery", "Service Availability", "", ""),
        ("Availability & Recovery", "RTO", "", ""),
        ("Availability & Recovery", "RPO", "", ""),




            # Hosting and System Dependencies relationships
        ("Hosting and System Dependencies", "Dependencies Management", "", ""),

        # Dependencies Management field connections
        ("Dependencies Management", "Dependency ID", "", ""),
        ("Dependencies Management", "Dependency Status", "", ""),
        ("Dependencies Management", "Dependency Type", "", ""),
        ("Dependencies Management", "Dependency System", "", ""),
        ("Downstream Dependency", "Dependent System", "", ""),
        ("Downstream Dependency", "Dependency ID", "", ""),
        ("Downstream Dependency", "Dependency Status", "", ""),
        ("Downstream Dependency", "Dependency Type", "", ""),

        # Agency Management Module relationships
        ("Agency Management", "Agency", "", ""),
        ("Agency Management", "Key Appointment Holder", "", ""),

        # Agency field connections
        ("Agency", "Agency Name", "", ""),
        ("Agency", "Agency Abbreviation (Short Form)", "", ""),
        ("Agency", "Agency Operational Status", "", ""),
        ("Agency", "Ministry Family", "", ""),

        # Key Appointment Holder field connections
        ("Key Appointment Holder", "Full Name", "", ""),
        ("Key Appointment Holder", "Designation", "", ""),
        ("Key Appointment Holder", "Email", "", ""),

        # Cross-module relationships
        ("System Criticality", "Computed RML", "", ""),
        ("Security Classification", "Computed RML", "", ""),
        ("Sensitivity Classification", "Computed RML", "", ""),
        ("Downstream Dependency", "Computed RML", "", ""),

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

