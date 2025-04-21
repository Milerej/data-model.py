#PART1
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
    st.title("⚙️ Data Model : System Management and Agency Management V2.3)")

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


#PART2


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


#PART3


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


#PART4


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


#PART5


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


#PART6


        # System Management Fields - Availability & Recovery
        "Availability Tier": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Availability Tier field"
        },
        "Recovery Tier": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Recovery Tier field"
        },

        # Agency Management Fields
        "Agency Code": {
            "color": COLOR_SCHEMES["agency_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Agency Code field"
        },
        "Agency Name": {
            "color": COLOR_SCHEMES["agency_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Agency Name field"
        },
        "Agency Sector": {
            "color": COLOR_SCHEMES["agency_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Agency Sector field"
        },
        "Agency Type": {
            "color": COLOR_SCHEMES["agency_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Agency Type field"
        }
    }

    # Define all edges (connections between nodes)
    edges = [
        ("DGP 2.0", "System Management"),
        ("DGP 2.0", "Agency Management"),

        # System Management connections
        ("System Management", "System Identity & Classification"),
        ("System Management", "Criticality & Risk"),
        ("System Management", "System Resilience"),
        ("System Management", "Hosting and System Dependencies"),

        # System Identity & Classification connections
        ("System Identity & Classification", "Basic Information"),
        ("System Identity & Classification", "Organizational Context"),
        ("System Identity & Classification", "Classification"),

        # Criticality & Risk connections
        ("Criticality & Risk", "Impact Assessment"),
        ("Criticality & Risk", "Risk Materiality Level"),
        ("Criticality & Risk", "SCA/RML Approval"),

        # System Resilience connections
        ("System Resilience", "Availability & Recovery"),

        # Hosting and System Dependencies connections
        ("Hosting and System Dependencies", "Dependencies Management"),


#PART7


        # Basic Information field connections
        ("Basic Information", "System ID"),
        ("Basic Information", "System Name"),
        ("Basic Information", "System Description"),
        ("Basic Information", "System Status"),
        ("Basic Information", "Operational Date"),
        ("Basic Information", "Decommission Date"),

        # Classification field connections
        ("Classification", "Security Classification"),
        ("Classification", "Sensitivity Classification"),

        # Impact Assessment field connections
        ("Impact Assessment", "Economy"),
        ("Impact Assessment", "Public Health and Safety"),
        ("Impact Assessment", "National Security"),
        ("Impact Assessment", "Social Preparedness"),
        ("Impact Assessment", "Public Service"),

        # Risk Materiality Level field connections
        ("Risk Materiality Level", "System Criticality"),
        ("Risk Materiality Level", "Designated CII"),
        ("Risk Materiality Level", "Computed RML"),
        ("Risk Materiality Level", "Computed RML Date"),
        ("Risk Materiality Level", "Agency Proposed RML"),
        ("Risk Materiality Level", "RML Alignment"),
        ("Risk Materiality Level", "RML Justification"),
        ("Risk Materiality Level", "Endorsed RML"),
        ("Risk Materiality Level", "RML Endorsement Date"),
        ("Risk Materiality Level", "Endorsement Comments"),

        # SCA/RML Approval field connections
        ("SCA/RML Approval", "IDSC Approval Date"),
        ("SCA/RML Approval", "IDSC Approval Attachment"),
        ("SCA/RML Approval", "MHA Approval"),
        ("SCA/RML Approval", "CSA Approval"),
        ("SCA/RML Approval", "SNDGO Approval"),

        # Availability & Recovery field connections
        ("Availability & Recovery", "Availability Tier"),
        ("Availability & Recovery", "Recovery Tier"),

        # Agency Management connections
        ("Agency Management", "Agency"),
        ("Agency Management", "Key Appointment Holder"),

        # Agency field connections
        ("Agency", "Agency Code"),
        ("Agency", "Agency Name"),
        ("Agency", "Agency Sector"),
        ("Agency", "Agency Type"),
    ]

    # Create network
    net = Network(height='750px', width='100%', bgcolor='#ffffff', font_color='black')
    net.force_atlas_2based()

    # Add nodes
    for node_id, attrs in entities.items():
        net.add_node(
            node_id,
            color=attrs['color'],
            size=attrs['size'],
            title=attrs['title'],
            shape=attrs['shape']
        )


#PART8


    # Add edges
    for edge in edges:
        net.add_edge(edge[0], edge[1])

    # Configure hierarchical layout if enabled
    if view_type:
        net.set_options("""
        const options = {
            "layout": {
                "hierarchical": {
                    "enabled": true,
                    "levelSeparation": 150,
                    "nodeSpacing": 150,
                    "treeSpacing": 200,
                    "blockShifting": true,
                    "edgeMinimization": true,
                    "parentCentralization": true,
                    "direction": "UD",
                    "sortMethod": "directed",
                    "shakeTowards": "roots"
                }
            },
            "physics": {
                "hierarchicalRepulsion": {
                    "centralGravity": 0.5,
                    "springLength": 200,
                    "springConstant": 0.01,
                    "nodeDistance": 200,
                    "damping": 0.09
                },
                "minVelocity": 0.75,
                "solver": "hierarchicalRepulsion"
            }
        }
        """)
    else:
        net.set_options("""
        const options = {
            "physics": {
                "forceAtlas2Based": {
                    "gravitationalConstant": -100,
                    "centralGravity": 0.01,
                    "springLength": 200,
                    "springConstant": 0.08,
                    "damping": 0.4,
                    "avoidOverlap": 1
                },
                "minVelocity": 0.75,
                "solver": "forceAtlas2Based"
            }
        }
        """)

    # Save and display the network
    try:
        path = os.path.join(tempfile.gettempdir(), "graph.html")
        net.save_graph(path)
        with open(path, 'r', encoding='utf-8') as file:
            components.html(file.read(), height=800)
    except Exception as e:
        st.error(f"Error displaying graph: {str(e)}")
