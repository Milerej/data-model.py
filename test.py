#Part 1 - Initial imports and password check:

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

#Part 2 - Color schemes and start of entities dictionary:


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



#Part 3 - Agency Management Module nodes and System Management subgroups:


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



#Part 4 - System Management Fields - Basic Information and Classification:



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



#Part 5 - System Management Fields - Risk Materiality Level:


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



#Part 6 - Additional Approval Fields and System Resilience Fields:



        # Additional Approval Fields
        "Approval Status": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Approval Status field"
        },
        "Approval Comments": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Approval Comments field"
        },

        # System Resilience Fields
        "Recovery Time Objective": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Recovery Time Objective field"
        },
        "Recovery Point Objective": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Recovery Point Objective field"
        },
        "Availability Requirement": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Availability Requirement field"
        },
        "Business Continuity Plan": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Business Continuity Plan field"
        },
        "Disaster Recovery Plan": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Disaster Recovery Plan field"
        },
        "Last DR Test Date": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Last DR Test Date field"
        },
        "Next DR Test Date": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Next DR Test Date field"
        },
        "DR Test Result": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "DR Test Result field"
        },



#Part 7 - Dependencies Management Fields and Agency Management Fields:



        # Dependencies Management Fields
        "Hosting Environment": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Hosting Environment field"
        },
        "Hosting Type": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Hosting Type field"
        },
        "Data Centre": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Data Centre field"
        },
        "Cloud Service Provider": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Cloud Service Provider field"
        },
        "Dependencies": {
            "color": COLOR_SCHEMES["system_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Dependencies field"
        },

        # Agency Management Fields
        "Agency Name": {
            "color": COLOR_SCHEMES["agency_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Agency Name field"
        },
        "Agency Code": {
            "color": COLOR_SCHEMES["agency_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Agency Code field"
        },
        "Ministry": {
            "color": COLOR_SCHEMES["agency_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Ministry field"
        },
        "Agency Type": {
            "color": COLOR_SCHEMES["agency_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "Agency Type field"
        },
        "CIO Name": {
            "color": COLOR_SCHEMES["agency_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "CIO Name field"
        },
        "CIO Email": {
            "color": COLOR_SCHEMES["agency_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "CIO Email field"
        },
        "CISO Name": {
            "color": COLOR_SCHEMES["agency_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "CISO Name field"
        },
        "CISO Email": {
            "color": COLOR_SCHEMES["agency_management"]["field"],
            "size": NODE_SETTINGS["field"]["size"],
            "shape": NODE_SETTINGS["field"]["shape"],
            "title": "CISO Email field"
        }
    }



#Part 8 - Relationships dictionary and network creation:



    # Define relationships between entities
    relationships = [
        # Root to Modules
        ("DGP 2.0", "System Management"),
        ("DGP 2.0", "Agency Management"),

        # System Management to Sub-modules
        ("System Management", "System Identity & Classification"),
        ("System Management", "Criticality & Risk"),
        ("System Management", "System Resilience"),
        ("System Management", "Hosting and System Dependencies"),

        # Agency Management to Sub-modules
        ("Agency Management", "Agency"),
        ("Agency Management", "Key Appointment Holder"),

        # System Identity & Classification to Sub-groups
        ("System Identity & Classification", "Basic Information"),
        ("System Identity & Classification", "Organizational Context"),
        ("System Identity & Classification", "Classification"),

        # Criticality & Risk to Sub-groups
        ("Criticality & Risk", "Impact Assessment"),
        ("Criticality & Risk", "Risk Materiality Level"),
        ("Criticality & Risk", "SCA/RML Approval"),

        # System Resilience to Sub-groups
        ("System Resilience", "Availability & Recovery"),

        # Hosting and System Dependencies to Sub-groups
        ("Hosting and System Dependencies", "Dependencies Management"),

        # Basic Information to Fields
        ("Basic Information", "System ID"),
        ("Basic Information", "System Name"),
        ("Basic Information", "System Description"),
        ("Basic Information", "System Status"),
        ("Basic Information", "Operational Date"),
        ("Basic Information", "Decommission Date"),

        # Classification to Fields
        ("Classification", "Security Classification"),
        ("Classification", "Sensitivity Classification"),

        # Impact Assessment to Fields
        ("Impact Assessment", "Economy"),
        ("Impact Assessment", "Public Health and Safety"),
        ("Impact Assessment", "National Security"),
        ("Impact Assessment", "Social Preparedness"),
        ("Impact Assessment", "Public Service"),

        # Risk Materiality Level to Fields
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

        # SCA/RML Approval to Fields
        ("SCA/RML Approval", "IDSC Approval Date"),
        ("SCA/RML Approval", "IDSC Approval Attachment"),
        ("SCA/RML Approval", "MHA Approval"),
        ("SCA/RML Approval", "CSA Approval"),
        ("SCA/RML Approval", "SNDGO Approval"),
        ("SCA/RML Approval", "Approval Status"),
        ("SCA/RML Approval", "Approval Comments"),

        # Availability & Recovery to Fields
        ("Availability & Recovery", "Recovery Time Objective"),
        ("Availability & Recovery", "Recovery Point Objective"),
        ("Availability & Recovery", "Availability Requirement"),
        ("Availability & Recovery", "Business Continuity Plan"),
        ("Availability & Recovery", "Disaster Recovery Plan"),
        ("Availability & Recovery", "Last DR Test Date"),
        ("Availability & Recovery", "Next DR Test Date"),
        ("Availability & Recovery", "DR Test Result"),

        # Dependencies Management to Fields
        ("Dependencies Management", "Hosting Environment"),
        ("Dependencies Management", "Hosting Type"),
        ("Dependencies Management", "Data Centre"),
        ("Dependencies Management", "Cloud Service Provider"),
        ("Dependencies Management", "Dependencies"),

        # Agency to Fields
        ("Agency", "Agency Name"),
        ("Agency", "Agency Code"),
        ("Agency", "Ministry"),
        ("Agency", "Agency Type"),

        # Key Appointment Holder to Fields
        ("Key Appointment Holder", "CIO Name"),
        ("Key Appointment Holder", "CIO Email"),
        ("Key Appointment Holder", "CISO Name"),
        ("Key Appointment Holder", "CISO Email"),
    ]


#Part 9 - Network creation and visualization code:


    # Create network
    net = Network(height='750px', width='100%', bgcolor='#ffffff', font_color='black')
    net.force_atlas_2based()

    # Add nodes
    for entity, attributes in entities.items():
        net.add_node(
            entity,
            color=attributes["color"],
            size=attributes["size"],
            shape=attributes["shape"],
            title=attributes["title"]
        )

    # Add edges
    for source, target in relationships:
        net.add_edge(source, target)

    # Configure physics
    net.set_options("""
    const options = {
        "physics": {
            "enabled": true,
            "forceAtlas2Based": {
                "gravitationalConstant": -100,
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
                "updateInterval": 25
            }
        },
        "interaction": {
            "hover": true,
            "tooltipDelay": 200
        },
        "edges": {
            "color": {
                "color": "#000000",
                "highlight": "#000000",
                "hover": "#000000",
                "inherit": false,
                "opacity": 1.0
            },
            "smooth": {
                "type": "continuous",
                "forceDirection": "none"
            }
        }
    }
    """)

    # If hierarchical layout is enabled
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
                    "sortMethod": "directed"
                }
            },
            "physics": {
                "enabled": false
            },
            "interaction": {
                "hover": true,
                "tooltipDelay": 200
            },
            "edges": {
                "color": {
                    "color": "#000000",
                    "highlight": "#000000",
                    "hover": "#000000",
                    "inherit": false,
                    "opacity": 1.0
                },
                "smooth": {
                    "type": "continuous",
                    "forceDirection": "none"
                }
            }
        }
        """)

    # Save and display network
    try:
        path = os.path.join(tempfile.gettempdir(), "pyvis_graph.html")
        net.save_graph(path)
        HtmlFile = open(path, 'r', encoding='utf-8')
        components.html(HtmlFile.read(), height=750)
    except Exception as e:
        st.error(f"Error displaying graph: {str(e)}")

