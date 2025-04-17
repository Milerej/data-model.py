import streamlit as st
from pyvis.network import Network
import networkx as nx
import streamlit.components.v1 as components
import tempfile
import os

# Define standard colours and sizes
AGENCY_COLOR = "#0066CC"     # Standard blue for Agency-related items
MINISTRY_COLOR = "#0066CC"   # Standard blue for Ministry-related items
SYSTEM_COLOR = "#2E7D32"     # Green for System-related items
SUBGROUP_COLOR = "#2E7D32"   # Green for subgroups
FIELD_COLOR = "#2E7D32"      # Green for fields

# Standard sizes
MODULE_SIZE = 50      # For main modules
SUBMODULE_SIZE = 25   # For sub-modules
GROUP_SIZE = 20       # For groups
FIELD_SIZE = 15      # For fields

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
    st.title("⚙️ Data Model : System Management and Agency Management")


    # Define entity modules and colors
    entities = {
        # Agency Management Module
        "Agency Management": {
            "color": AGENCY_COLOR,
            "size": MODULE_SIZE,
            "shape": "dot",
            "title": "Agency Management Module"
        },
        "Agency": {
            "color": AGENCY_COLOR,
            "size": SUBMODULE_SIZE,
            "shape": "dot",
            "title": "Agency Sub-Module"
        },
        "Key Appointment Holder": {
            "color": AGENCY_COLOR,
            "size": SUBMODULE_SIZE,
            "shape": "dot",
            "title": "Key Appointment Holder Sub-Module"
        },

        # System Management Module
        "System Management": {
            "color": SYSTEM_COLOR,
            "size": MODULE_SIZE,
            "shape": "dot",
            "title": "System Management Module"
        },
        "System Identity & Classification": {
            "color": SYSTEM_COLOR,
            "size": SUBMODULE_SIZE,
            "shape": "dot",
            "title": "System Identity & Classification Sub-Module"
        },
        "Criticality & Risk": {
            "color": SYSTEM_COLOR,
            "size": SUBMODULE_SIZE,
            "shape": "dot",
            "title": "Criticality & Risk Sub-Module"
        },
        "System Resilience": {
            "color": SYSTEM_COLOR,
            "size": SUBMODULE_SIZE,
            "shape": "dot",
            "title": "System Resilience Sub-Module"
        },
        "Hosting and System Dependencies": {
            "color": SYSTEM_COLOR,
            "size": SUBMODULE_SIZE,
            "shape": "dot",
            "title": "Hosting and System Dependencies Sub-Module"
        },

        # Sub-groups
        "Basic Information": {
            "color": SUBGROUP_COLOR,
            "size": GROUP_SIZE,
            "shape": "dot",
            "title": "Basic Information Sub-Group"
        },
        "Organizational Context": {
            "color": SUBGROUP_COLOR,
            "size": GROUP_SIZE,
            "shape": "dot",
            "title": "Organizational Context Sub-Group"
        },
        "Classification": {
            "color": SUBGROUP_COLOR,
            "size": GROUP_SIZE,
            "shape": "dot",
            "title": "Classification Sub-Group"
        },
        "Impact Assessment": {
            "color": SUBGROUP_COLOR,
            "size": GROUP_SIZE,
            "shape": "dot",
            "title": "Impact Assessment Sub-Group"
        },
        "Risk Profile": {
            "color": SUBGROUP_COLOR,
            "size": GROUP_SIZE,
            "shape": "dot",
            "title": "Risk Profile Sub-Group"
        },
        "SCA/RML Approval": {
            "color": SUBGROUP_COLOR,
            "size": GROUP_SIZE,
            "shape": "dot",
            "title": "SCA/RML Approval Sub-Group"
        },
        "Availability & Recovery": {
            "color": SUBGROUP_COLOR,
            "size": GROUP_SIZE,
            "shape": "dot",
            "title": "Availability & Recovery Sub-Group"
        },
        "Dependencies Management": {
            "color": SUBGROUP_COLOR,
            "size": GROUP_SIZE,
            "shape": "dot",
            "title": "Dependencies Management Sub-Group"
        },

        # Fields
        "Agency Name": {
            "color": AGENCY_COLOR,
            "size": FIELD_SIZE,
            "shape": "dot",
            "title": "Agency Name field"
        },
        "Agency Abbreviation (Short Form)": {
            "color": AGENCY_COLOR,
            "size": FIELD_SIZE,
            "shape": "dot",
            "title": "Agency Abbreviation (Short Form) field"
        },
        "Agency Operational Status": {
            "color": AGENCY_COLOR,
            "size": FIELD_SIZE,
            "shape": "dot",
            "title": "Agency Operational field"
        },
        "Ministry Family": {
            "color": MINISTRY_COLOR,
            "size": FIELD_SIZE,
            "shape": "dot",
            "title": "Ministry Family field"
        },
        "Full Name": {
            "color": AGENCY_COLOR,
            "size": FIELD_SIZE,
            "shape": "dot",
            "title": "Full Name of Key Appointment Holder field"
        },
        "Designation": {
            "color": AGENCY_COLOR,
            "size": FIELD_SIZE,
            "shape": "dot",
            "title": "Designation field"
        },
        "Email": {
            "color": AGENCY_COLOR,
            "size": FIELD_SIZE,
            "shape": "dot",
            "title": "Email field"
        },
        "System ID": {
            "color": FIELD_COLOR,
            "size": FIELD_SIZE,
            "shape": "dot",
            "title": "System ID (Primary Key)"
        },
        "System Name": {
            "color": FIELD_COLOR,
            "size": FIELD_SIZE,
            "shape": "dot",
            "title": "System Name field"
        },
        "System Description": {
            "color": FIELD_COLOR,
            "size": FIELD_SIZE,
            "shape": "dot",
            "title": "System Description field"
        },
        "System Status": {
            "color": FIELD_COLOR,
            "size": FIELD_SIZE,
            "shape": "dot",
            "title": "System Status field"
        },
        "Security Classification": {
            "color": FIELD_COLOR,
            "size": FIELD_SIZE,
            "shape": "dot",
            "title": "Security Classification field"
        },
        "Sensitivity Classification": {
            "color": FIELD_COLOR,
            "size": FIELD_SIZE,
            "shape": "dot",
            "title": "Sensitivity Classification field"
        },

        # Additional Fields
        "Economy": {
            "color": FIELD_COLOR,
            "size": FIELD_SIZE,
            "shape": "dot",
            "title": "Economy Impact field"
        },
        "Public Health and Safety": {
            "color": FIELD_COLOR,
            "size": FIELD_SIZE,
            "shape": "dot",
            "title": "Public Health and Safety Impact field"
        },
        "National Security": {
            "color": FIELD_COLOR,
            "size": FIELD_SIZE,
            "shape": "dot",
            "title": "National Security Impact field"
        },
        "Social Preparedness": {
            "color": FIELD_COLOR,
            "size": FIELD_SIZE,
            "shape": "dot",
            "title": "Social Preparedness Impact field"
        },
        "Public Service": {
            "color": FIELD_COLOR,
            "size": FIELD_SIZE,
            "shape": "dot",
            "title": "Public Service Impact field"
        },
        "System Criticality": {
            "color": FIELD_COLOR,
            "size": FIELD_SIZE,
            "shape": "dot",
            "title": "System Criticality field"
        },
        "Designated CII": {
            "color": FIELD_COLOR,
            "size": FIELD_SIZE,
            "shape": "dot",
            "title": "Designated CII field"
        },
        "Computed RML": {
            "color": FIELD_COLOR,
            "size": FIELD_SIZE,
            "shape": "dot",
            "title": "Computed RML field"
        },
        "Computed RML Date": {
            "color": FIELD_COLOR,
            "size": FIELD_SIZE,
            "shape": "dot",
            "title": "Computed RML Date field"
        },
        "Agency Proposed RML": {
            "color": FIELD_COLOR,
            "size": FIELD_SIZE,
            "shape": "dot",
            "title": "Agency Proposed RML field"
        },
        "RML Alignment": {
            "color": FIELD_COLOR,
            "size": FIELD_SIZE,
            "shape": "dot",
            "title": "RML Alignment field"
        },
        "RML Justification": {
            "color": FIELD_COLOR,
            "size": FIELD_SIZE,
            "shape": "dot",
            "title": "RML Justification field"
        },
        "Endorsed RML": {
            "color": FIELD_COLOR,
            "size": FIELD_SIZE,
            "shape": "dot",
            "title": "Endorsed RML field"
        },
        "RML Endorsement Date": {
            "color": FIELD_COLOR,
            "size": FIELD_SIZE,
            "shape": "dot",
            "title": "RML Endorsement Date field"
        },
        "Endorsement Comments": {
            "color": FIELD_COLOR,
            "size": FIELD_SIZE,
            "shape": "dot",
            "title": "Endorsement Comments field"
        },
        "IDSC Approval Date": {
            "color": FIELD_COLOR,
            "size": FIELD_SIZE,
            "shape": "dot",
            "title": "IDSC Approval Date field"
        },
        "IDSC Approval Attachment": {
            "color": FIELD_COLOR,
            "size": FIELD_SIZE,
            "shape": "dot",
            "title": "IDSC Approval Attachment field"
        },
        "MHA Approval": {
            "color": FIELD_COLOR,
            "size": FIELD_SIZE,
            "shape": "dot",
            "title": "MHA Approval field"
        },
        "CSA Approval": {
            "color": FIELD_COLOR,
            "size": FIELD_SIZE,
            "shape": "dot",
            "title": "CSA Approval field"
        },
        "SNDGO Approval": {
            "color": FIELD_COLOR,
            "size": FIELD_SIZE,
            "shape": "dot",
            "title": "SNDGO Approval field"
        },
        "MHA Comments": {
            "color": FIELD_COLOR,
            "size": FIELD_SIZE,
            "shape": "dot",
            "title": "MHA Comments field"
        },
        "CSA Comments": {
            "color": FIELD_COLOR,
            "size": FIELD_SIZE,
            "shape": "dot",
            "title": "CSA Comments field"
        },
        "SNDGO Comments": {
            "color": FIELD_COLOR,
            "size": FIELD_SIZE,
            "shape": "dot",
            "title": "SNDGO Comments field"
        },
        "Service Availability": {
            "color": FIELD_COLOR,
            "size": FIELD_SIZE,
            "shape": "dot",
            "title": "Service Availability field"
        },
        "RTO": {
            "color": FIELD_COLOR,
            "size": FIELD_SIZE,
            "shape": "dot",
            "title": "RTO field"
        },
        "RPO": {
            "color": FIELD_COLOR,
            "size": FIELD_SIZE,
            "shape": "dot",
            "title": "RPO field"
        },
        "Total Dependencies": {
            "color": FIELD_COLOR,
            "size": FIELD_SIZE,
            "shape": "dot",
            "title": "Total Dependencies field"
        },
        "Downstream Impact": {
            "color": FIELD_COLOR,
            "size": FIELD_SIZE,
            "shape": "dot",
            "title": "Downstream Impact field"
        },
        "Direct Dependencies Count": {
            "color": FIELD_COLOR,
            "size": FIELD_SIZE,
            "shape": "dot",
            "title": "Direct Dependencies Count field"
        },
        "Dependency ID": {
            "color": FIELD_COLOR,
            "size": FIELD_SIZE,
            "shape": "dot",
            "title": "Dependency ID field"
        },
        "Dependency Status": {
            "color": FIELD_COLOR,
            "size": FIELD_SIZE,
            "shape": "dot",
            "title": "Dependency Status field"
        },
        "Dependency Type": {
            "color": FIELD_COLOR,
            "size": FIELD_SIZE,
            "shape": "dot",
            "title": "Dependency Type field"
        },
        "Upstream System": {
            "color": FIELD_COLOR,
            "size": FIELD_SIZE,
            "shape": "dot",
            "title": "Upstream System field"
        },
        "Dependent System": {
            "color": FIELD_COLOR,
            "size": FIELD_SIZE,
            "shape": "dot",
            "title": "Dependent System field"
        },
        "Data Exchange Frequency": {
            "color": FIELD_COLOR,
            "size": FIELD_SIZE,
            "shape": "dot",
            "title": "Data Exchange Frequency field"
        },
        "Inferred Dependencies": {
            "color": FIELD_COLOR,
            "size": FIELD_SIZE,
            "shape": "dot",
            "title": "Inferred Dependencies field"
        },
        "Ministry Family Name": {
            "color": MINISTRY_COLOR,
            "size": FIELD_SIZE,
            "shape": "dot",
            "title": "Ministry Family Name field"
        }
    }

    # Define edges
    edges = [
        # Main module connections
        ("System Management", "System Identity & Classification", "", ""),
        ("System Management", "Criticality & Risk", "", ""),
        ("System Management", "System Resilience", "", ""),
        ("System Management", "Hosting and System Dependencies", "", ""),
        
        ("Agency Management", "Agency", "", ""),
        ("Agency Management", "Key Appointment Holder", "", ""),
      
        # Agency sub-group connection    
        ("Agency", "Agency Name", "", ""),
        ("Agency", "Agency Abbreviation (Short Form)", "", ""),
        ("Agency", "Agency Operational Status", "", ""),
        ("Agency", "Ministry Family", "", ""),
        ("Key Appointment Holder", "Full Name", "", ""),
        ("Key Appointment Holder", "Designation", "", ""),
        ("Key Appointment Holder", "Email", "", ""),
        ("Ministry Family", "Ministry Family Name", "", ""),
         
        # System Identity & Classification sub-group connections
        ("System Identity & Classification", "Basic Information", "", ""),
        ("System Identity & Classification", "Organizational Context", "", ""),
        ("System Identity & Classification", "Classification", "", ""),

        # Basic Information connections
        ("Basic Information", "System ID", "", ""),
        ("Basic Information", "System Name", "", ""),
        ("Basic Information", "System Description", "", ""),
        ("Basic Information", "System Status", "", ""),

        # Organizational Context connections
        ("Organizational Context", "Agency Name", "", ""),
        ("Organizational Context", "Ministry Family Name", "", ""),

        # Classification connections
        ("Classification", "Security Classification", "", ""),
        ("Classification", "Sensitivity Classification", "", ""),

        # Criticality & Risk sub-group connections
        ("Criticality & Risk", "Impact Assessment", "", ""),
        ("Criticality & Risk", "Risk Profile", "", ""),
        ("Criticality & Risk", "SCA/RML Approval", "", ""),

        # Impact Assessment connections
        ("Impact Assessment", "Economy", "", ""),
        ("Impact Assessment", "Public Health and Safety", "", ""),
        ("Impact Assessment", "National Security", "", ""),
        ("Impact Assessment", "Social Preparedness", "", ""),
        ("Impact Assessment", "Public Service", "", ""),
        ("Impact Assessment", "System Criticality", "", ""),
        ("Impact Assessment", "Designated CII", "", ""),

        # Risk Profile connections
        ("Risk Profile", "Computed RML", "", ""),
        ("Risk Profile", "Computed RML Date", "", ""),
        ("Risk Profile", "Agency Proposed RML", "", ""),
        ("Risk Profile", "RML Alignment", "", ""),
        ("Risk Profile", "RML Justification", "", ""),
        ("Risk Profile", "Endorsed RML", "", ""),
        ("Risk Profile", "RML Endorsement Date", "", ""),
        ("Risk Profile", "Endorsement Comments", "", ""),
        ("Computed RML", "System Criticality", "", ""),
        ("Computed RML", "Security Classification", "", ""),
        ("Computed RML", "Sensitivity Classification", "", ""),
        ("Computed RML", "Inferred Dependencies", "", ""),

        # SCA/RML Approval connections
        ("SCA/RML Approval", "IDSC Approval Date", "", ""),
        ("SCA/RML Approval", "IDSC Approval Attachment", "", ""),
        ("SCA/RML Approval", "MHA Approval", "", ""),
        ("SCA/RML Approval", "CSA Approval", "", ""),
        ("SCA/RML Approval", "SNDGO Approval", "", ""),
        ("SCA/RML Approval", "MHA Comments", "", ""),
        ("SCA/RML Approval", "CSA Comments", "", ""),
        ("SCA/RML Approval", "SNDGO Comments", "", ""),

        # System Resilience sub-group connections
        ("System Resilience", "Availability & Recovery", "", ""),
        ("Availability & Recovery", "Service Availability", "", ""),
        ("Availability & Recovery", "RTO", "", ""),
        ("Availability & Recovery", "RPO", "", ""),

        # Hosting and System Dependencies sub-group connections
        ("Hosting and System Dependencies", "Dependencies Management", "", ""),
        ("Dependencies Management", "Total Dependencies", "", ""),
        ("Dependencies Management", "Downstream Impact", "", ""),
        ("Dependencies Management", "Direct Dependencies Count", "", ""),
        ("Dependencies Management", "Dependency ID", "", ""),
        ("Dependencies Management", "Dependency Status", "", ""),
        ("Dependencies Management", "Dependency Type", "", ""),
        ("Dependencies Management", "Upstream System", "", ""),
        ("Dependencies Management", "Dependent System", "", ""),
        ("Dependencies Management", "Data Exchange Frequency", "", ""),
        ("Dependencies Management", "Inferred Dependencies", "", "")
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

    # Create interactive PyVis network
    net = Network(height="900px", width="100%", directed=True, notebook=True)
    net.from_nx(G)

    # Set network options
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
    
