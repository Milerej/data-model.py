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
        "field": {
            "size": 25,
            "shape": "dot"
        }
    }

    COLOR_SCHEMES = {
        "system_management": {
            "module": "#1B5E20",      # Darkest green
            "submodule": "#2E7D32",   # Dark green
            "field": "#388E3C"        # Medium green
        },
        "agency_management": {
            "module": "#1A237E",      # Darkest blue
            "submodule": "#283593",   # Dark blue
            "field": "#303F9F"        # Medium blue
        }
    }


    # Complete entities dictionary with all nodes
    entities = {
        # Root node
        "DGP 2.0": {
            "color": "#1A237E",
            "size": 60,
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

        # System Identity & Classification Fields
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
        "Agency Name": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Agency Name field"
        },
        "Ministry Family Name": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Ministry Family Name field"
        },
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

        # Criticality & Risk Fields
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

        # System Resilience Fields
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

        # Hosting and System Dependencies Fields
        "Total Dependencies": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Total Dependencies field"
        },
        "Downstream Impact": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Downstream Impact field"
        },
        "Direct Dependencies Count": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Direct Dependencies Count field"
        },
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
        "Upstream System": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Upstream System field"
        },
        "Dependent System": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Dependent System field"
        },
        "Data Exchange Frequency": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Data Exchange Frequency field"
        },
        "Inferred Dependencies": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Inferred Dependencies field"
        },

        # Agency Management Fields
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




    # Define edges
    edges = [
        # Root node connections
        ("DGP 2.0", "System Management", "", ""),
        ("DGP 2.0", "Agency Management", "", ""),

        # System Management Module relationships
        ("System Management", "System Identity & Classification", "", ""),
        ("System Management", "Criticality & Risk", "", ""),
        ("System Management", "System Resilience", "", ""),
        ("System Management", "Hosting and System Dependencies", "", ""),

        # Agency Management Module relationships
        ("Agency Management", "Agency", "", ""),
        ("Agency Management", "Key Appointment Holder", "", ""),

        # System Identity & Classification field relationships
        ("System Identity & Classification", "System ID", "", ""),
        ("System Identity & Classification", "System Name", "", ""),
        ("System Identity & Classification", "System Description", "", ""),
        ("System Identity & Classification", "System Status", "", ""),
        ("System Identity & Classification", "Operational Date", "", ""),
        ("System Identity & Classification", "Decommission Date", "", ""),
        ("System Identity & Classification", "Agency Name", "", ""),
        ("System Identity & Classification", "Ministry Family Name", "", ""),
        ("System Identity & Classification", "Security Classification", "", ""),
        ("System Identity & Classification", "Sensitivity Classification", "", ""),

        # Criticality & Risk field relationships
        ("Criticality & Risk", "Economy", "", ""),
        ("Criticality & Risk", "Public Health and Safety", "", ""),
        ("Criticality & Risk", "National Security", "", ""),
        ("Criticality & Risk", "Social Preparedness", "", ""),
        ("Criticality & Risk", "Public Service", "", ""),
        ("Criticality & Risk", "System Criticality", "", ""),
        ("Criticality & Risk", "Designated CII", "", ""),
        ("Criticality & Risk", "Computed RML", "", ""),
        ("Criticality & Risk", "Computed RML Date", "", ""),
        ("Criticality & Risk", "Agency Proposed RML", "", ""),
        ("Criticality & Risk", "RML Alignment", "", ""),
        ("Criticality & Risk", "RML Justification", "", ""),
        ("Criticality & Risk", "Endorsed RML", "", ""),
        ("Criticality & Risk", "RML Endorsement Date", "", ""),
        ("Criticality & Risk", "Endorsement Comments", "", ""),
        ("Criticality & Risk", "IDSC Approval Date", "", ""),
        ("Criticality & Risk", "IDSC Approval Attachment", "", ""),
        ("Criticality & Risk", "MHA Approval", "", ""),
        ("Criticality & Risk", "CSA Approval", "", ""),
        ("Criticality & Risk", "SNDGO Approval", "", ""),
        ("Criticality & Risk", "MHA Comments", "", ""),
        ("Criticality & Risk", "CSA Comments", "", ""),
        ("Criticality & Risk", "SNDGO Comments", "", ""),

        # System Resilience field relationships
        ("System Resilience", "Service Availability", "", ""),
        ("System Resilience", "RTO", "", ""),
        ("System Resilience", "RPO", "", ""),

        # Hosting and System Dependencies field relationships
        ("Hosting and System Dependencies", "Total Dependencies", "", ""),
        ("Hosting and System Dependencies", "Downstream Impact", "", ""),
        ("Hosting and System Dependencies", "Direct Dependencies Count", "", ""),
        ("Hosting and System Dependencies", "Dependency ID", "", ""),
        ("Hosting and System Dependencies", "Dependency Status", "", ""),
        ("Hosting and System Dependencies", "Dependency Type", "", ""),
        ("Hosting and System Dependencies", "Upstream System", "", ""),
        ("Hosting and System Dependencies", "Dependent System", "", ""),
        ("Hosting and System Dependencies", "Data Exchange Frequency", "", ""),
        ("Hosting and System Dependencies", "Inferred Dependencies", "", ""),

        # Agency field relationships
        ("Agency", "Agency Name", "", ""),
        ("Agency", "Agency Abbreviation (Short Form)", "", ""),
        ("Agency", "Agency Operational Status", "", ""),
        ("Agency", "Ministry Family", "", ""),

        # Key Appointment Holder field relationships
        ("Key Appointment Holder", "Full Name", "", ""),
        ("Key Appointment Holder", "Designation", "", ""),
        ("Key Appointment Holder", "Email", "", "")
    ]


 # ----------- Break ----------


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

    # Add dynamic spacing function
    def get_dynamic_spacing():
        # Count nodes at each level
        level_counts = {}
        for edge in edges:
            source = edge[0]
            if source not in level_counts:
                level_counts[source] = 0
            level_counts[source] += 1
        
        # Calculate maximum nodes at any level
        max_nodes = max(level_counts.values()) if level_counts else 1
        
        # Dynamic spacing calculations
        base_node_spacing = 150
        base_level_separation = 200
        
        # Adjust spacing based on number of nodes
        dynamic_node_spacing = base_node_spacing * (1 + (max_nodes / 20))
        dynamic_level_separation = base_level_separation * (1 + (len(level_counts) / 10))
        
        return dynamic_node_spacing, dynamic_level_separation

    # Get dynamic spacing values
    node_spacing, level_separation = get_dynamic_spacing()

    # Set hierarchical layout options based on toggle
    if view_type:
        net.set_options(f"""{{
            "layout": {{
                "hierarchical": {{
                    "enabled": true,
                    "direction": "UD",
                    "sortMethod": "directed",
                    "nodeSpacing": {node_spacing},
                    "levelSeparation": {level_separation},
                    "treeSpacing": {node_spacing * 1.2},
                    "blockShifting": true,
                    "edgeMinimization": true,
                    "parentCentralization": true,
                    "shakeTowards": "roots"
                }}
            }},
            "physics": {{
                "enabled": true,
                "hierarchicalRepulsion": {{
                    "centralGravity": 0.2,
                    "springLength": {level_separation * 0.75},
                    "springConstant": 0.2,
                    "nodeDistance": {node_spacing * 1.1},
                    "damping": 0.09,
                    "avoidOverlap": 1
                }},
                "stabilization": {{
                    "enabled": true,
                    "iterations": 2000,
                    "updateInterval": 100,
                    "fit": true
                }}
            }},
            "edges": {{
                "smooth": {{
                    "type": "cubicBezier",
                    "forceDirection": "vertical",
                    "roundness": 0.3
                }},
                "color": {{
                    "inherit": false,
                    "color": "#2E7D32",
                    "opacity": 0.6
                }}
            }},
            "nodes": {{
                "fixed": {{
                    "x": false,
                    "y": true
                }},
                "shape": "dot",
                "size": 20,
                "font": {{
                    "size": 12,
                    "face": "arial"
                }}
            }},
            "interaction": {{
                "dragNodes": true,
                "dragView": true,
                "zoomView": true,
                "hover": true
            }},
            "groups": {{
                "useDefaultGroups": false
            }}
        }}""")
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





 # Second Chart - add this after the except block of your first chart
    st.markdown("## Data Model Interdependency Chart")

    # Define entity modules and colors for second chart
    entities_2 = {
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
    for node, color in entities_2.items():
        G2.add_node(node, title=node, color=color)

    # Add edges with labels and custom arrow directions
    for source, target, label, direction in edges_2:
        G2.add_edge(source, target, title=label, label=label, arrows=direction)

    # Create interactive PyVis network for second chart
    net2 = Network(height="700px", width="100%", directed=True)
    net2.from_nx(G2)
    net2.repulsion(node_distance=200, central_gravity=0.3)

    # Customize edge labels and arrows
    for edge in net2.edges:
        edge["label"] = edge["title"]
        if edge["arrows"] == "both":
            edge["arrows"] = "to,from"
        else:
            edge["arrows"] = edge["arrows"]

    # Save and display second chart in Streamlit
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as tmp_file:
            net2.save_graph(tmp_file.name)
            with open(tmp_file.name, 'r', encoding='utf-8') as f:
                components.html(f.read(), height=750, scrolling=True)
            os.unlink(tmp_file.name)
    except Exception as e:
        st.error(f"An error occurred while generating the second graph: {str(e)}")
