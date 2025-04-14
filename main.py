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
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True

if check_password():
    st.set_page_config(page_title="Interactive Interdependency Graph", layout="wide")

    st.title("⚙️ Data Model : System Management")

    # Define entity modules and colors
    entities = {
        "System Management": {
            "color": "#2E7D32", 
            "size": 50, 
            "shape": "dot",
            "title": "System Management Module"
        },
        # Main Modules
        "System Overview": {
            "color": "#4CAF50", 
            "size": 25, 
            "shape": "dot",
            "title": "System Overview Sub-Module"
        },
        "Criticality Assessment": {
            "color": "#4CAF50", 
            "size": 25,
            "shape": "dot",
            "title": "Criticality Assessment Sub-Module"
        },
        "Security & Sensitivity Classification": {
            "color": "#4CAF50", 
            "size": 25, 
            "shape": "dot",
            "title": "Security & Sensitivity Classification Sub-Module"
        },
        "Risk Materiality Level": {
            "color": "#4CAF50", 
            "size": 25, 
            "shape": "dot",
            "title": "Risk Materiality Level Sub-Module"
        },
        "System Resiliency": {
            "color": "#4CAF50", 
            "size": 25, 
            "shape": "dot",
            "title": "System Resiliency Sub-Module"
        },
        "Hosting and System Dependencies": {
            "color": "#4CAF50", 
            "size": 25, 
            "shape": "dot",
            "title": "Hosting and System Dependencies Sub-Module"
        },

            # System Overview Fields
        "Agency": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Agency field"
        },
        "Ministry Family": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Ministry Family field"
        },
        "System ID": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "System ID (Primary Key)"
        },
        "System Name": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "System Name field"
        },
        "System Description": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "System Description field"
        },
        "System Status": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "System Status field"
        },

        # Criticality Assessment Fields
        "Economy": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Economy impact field"
        },
        "Public Health and Safety": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Public Health and Safety field"
        },
        "National Security": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "National Security field"
        },
        "Social Preparedness": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Social Preparedness field"
        },
        "Public Service": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Public Service field"
        },
        "Designated CII": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Designated CII under Cybersecurity Act"
        },
        "System Criticality": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "System Criticality (Auto-generated)"
        },
        "IDSC Approval Date": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "IDSC's Approval Date (CA)"
        },
        "IDSC Approval Attachment": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "IDSC's Approval Attachment (CA)"
        },
        "MHA Approval": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Approved by MHA?"
        },
        "CSA Approval": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Approved by CSA?"
        },
        "SNDGO Approval": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Approved by SNDGO?"
        },
        "MHA Comments": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "MHA Comments"
        },
        "CSA Comments": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "CSA Comments"
        },
        "SNDGO Comments": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "SNDGO Comments"
        },

            # Security & Sensitivity Classification Fields
        "Security Classification": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Security Classification field"
        },
        "Sensitivity Classification": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Sensitivity Classification field"
        },

        # Risk Materiality Level Fields
        "Computed RML": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Computed Risk Materiality Level"
        },
        "Computed RML Date": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Computed RML Date"
        },
        "Agency Proposed RML": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Agency Proposed Risk Materiality Level"
        },
        "RML Alignment": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "In line with Computed RML?"
        },
        "RML Justification": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Justification if not in line"
        },
        "Endorsed RML": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Endorsed Risk Materiality Level"
        },
        "RML Endorsement Date": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Date Endorsed"
        },
        "Endorsement Comments": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Endorsed Comments"
        },

        # System Resiliency Fields
        "Service Availability": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Service Availability"
        },
        "RTO": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Recovery Time Objective"
        },
        "RPO": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Recovery Point Objective"
        },

        # Hosting and System Dependencies Fields
        "Total Dependencies": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Total Downstream Dependencies"
        },
        "Downstream Impact": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Sub-System Downstream Impact"
        },
        "Direct Dependencies Count": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Count of Direct Dependencies"
        },
        "Dependency ID": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Dependency ID"
        },
        "Dependency Status": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Dependency Status"
        },
        "Dependency Type": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Type of Dependency"
        },
        "Upstream System": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Dependent Sub-System Upstream"
        },
        "Dependent System": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Dependent System/Service Name"
        },
        "Data Exchange Frequency": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Frequency of Data Exchange"
        },
        "Inferred Dependencies": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Count of Inferred Dependencies"
        }
    }

    # Define edges with PK/FK relationships
    edges = [
        # Main module connections
        ("System Management", "System Overview", "PK: System_ID", ""),
        ("System Management", "Criticality Assessment", "PK: System_ID", ""),
        ("System Management", "Security & Sensitivity Classification", "PK: System_ID", ""),
        ("System Management", "System Resiliency", "PK: System_ID", ""),
        ("System Management", "Hosting and System Dependencies", "PK: System_ID", ""),
        ("Risk Materiality Level", "Security & Sensitivity Classification", "o", ""),
        ("Risk Materiality Level", "Hosting and System Dependencies", "o", ""),
        ("Risk Materiality Level", "Criticality Assessment", "o", ""),

        # System Overview field connections
        ("System Overview", "Agency", "", "to"),
        ("System Overview", "Ministry Family", "", "to"),
        ("System Overview", "System ID", "", "to"),
        ("System Overview", "System Name", "", "to"),
        ("System Overview", "System Description", "", "to"),
        ("System Overview", "System Status", "", "to"),

        # Criticality Assessment field connections
        ("Criticality Assessment", "Economy", "", "to"),
        ("Criticality Assessment", "Public Health and Safety", "", "to"),
        ("Criticality Assessment", "National Security", "", "to"),
        ("Criticality Assessment", "Social Preparedness", "", "to"),
        ("Criticality Assessment", "Public Service", "", "to"),
        ("Criticality Assessment", "Designated CII", "", "to"),
        ("Criticality Assessment", "System Criticality", "", "to"),
        ("Criticality Assessment", "IDSC Approval Date", "", "to"),
        ("Criticality Assessment", "IDSC Approval Attachment", "", "to"),
        ("Criticality Assessment", "MHA Approval", "", "to"),
        ("Criticality Assessment", "CSA Approval", "", "to"),
        ("Criticality Assessment", "SNDGO Approval", "", "to"),
        ("Criticality Assessment", "MHA Comments", "", "to"),
        ("Criticality Assessment", "CSA Comments", "", "to"),
        ("Criticality Assessment", "SNDGO Comments", "", "to"),

        # Security & Sensitivity Classification field connections
        ("Security & Sensitivity Classification", "Security Classification", "", "to"),
        ("Security & Sensitivity Classification", "Sensitivity Classification", "", "to"),

        # Risk Materiality Level field connections
        ("Risk Materiality Level", "Computed RML", "", "to"),
        ("Risk Materiality Level", "Computed RML Date", "", "to"),
        ("Risk Materiality Level", "Agency Proposed RML", "", "to"),
        ("Risk Materiality Level", "RML Alignment", "", "to"),
        ("Risk Materiality Level", "RML Justification", "", "to"),
        ("Risk Materiality Level", "Endorsed RML", "", "to"),
        ("Risk Materiality Level", "RML Endorsement Date", "", "to"),
        ("Risk Materiality Level", "Endorsement Comments", "", "to"),

        # System Resiliency field connections
        ("System Resiliency", "Service Availability", "", "to"),
        ("System Resiliency", "RTO", "", "to"),
        ("System Resiliency", "RPO", "", "to"),

        # Hosting and System Dependencies field connections
        ("Hosting and System Dependencies", "Total Dependencies", "", "to"),
        ("Hosting and System Dependencies", "Downstream Impact", "", "to"),
        ("Hosting and System Dependencies", "Direct Dependencies Count", "", "to"),
        ("Hosting and System Dependencies", "Dependency ID", "", "to"),
        ("Hosting and System Dependencies", "Dependency Status", "", "to"),
        ("Hosting and System Dependencies", "Dependency Type", "", "to"),
        ("Hosting and System Dependencies", "Upstream System", "", "to"),
        ("Hosting and System Dependencies", "Dependent System", "", "to"),
        ("Hosting and System Dependencies", "Data Exchange Frequency", "", "to"),
        ("Hosting and System Dependencies", "Inferred Dependencies", "", "to")
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

       # Save and display the network
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as tmp_file:
            net.save_graph(tmp_file.name)
            with open(tmp_file.name, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Insert the button and script just before the closing body tag
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
                        } else if (elem.webkitRequestFullscreen) { /* Safari */
                            elem.webkitRequestFullscreen();
                        } else if (elem.msRequestFullscreen) { /* IE11 */
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
            
            # Insert the button just before </body>
            modified_html = html_content.replace('</body>', f'{fullscreen_html}</body>')
            
            components.html(modified_html, height=900)
            # Clean up the temporary file
            os.unlink(tmp_file.name)
    except Exception as e:
        st.error(f"An error occurred while generating the graph: {str(e)}")
