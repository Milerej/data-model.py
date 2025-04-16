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
        "System Identity & Classification": {
            "color": "#4CAF50", 
            "size": 25, 
            "shape": "dot",
            "title": "System Identity & Classification Sub-Module"
        },
        "Criticality & Risk": {
            "color": "#4CAF50", 
            "size": 25,
            "shape": "dot",
            "title": "Criticality & Risk Sub-Module"
        },
        "System Resilience": {
            "color": "#4CAF50", 
            "size": 25,
            "shape": "dot",
            "title": "System Resilience Sub-Module"
        },
        "Hosting and System Dependencies": {
            "color": "#4CAF50", 
            "size": 25,
            "shape": "dot",
            "title": "Hosting and System Dependencies Sub-Module"
        },

        # Sub-groups
        "Basic Information": {
            "color": "#66BB6A", 
            "size": 20, 
            "shape": "dot",
            "title": "Basic Information Sub-Group"
        },
        "Organizational Context": {
            "color": "#66BB6A", 
            "size": 20, 
            "shape": "dot",
            "title": "Organizational Context Sub-Group"
        },
        "Classification": {
            "color": "#66BB6A", 
            "size": 20, 
            "shape": "dot",
            "title": "Classification Sub-Group"
        },
        "Impact Assessment": {
            "color": "#66BB6A", 
            "size": 20, 
            "shape": "dot",
            "title": "Impact Assessment Sub-Group"
        },
        "Risk Profile": {
            "color": "#66BB6A", 
            "size": 20, 
            "shape": "dot",
            "title": "Risk Profile Sub-Group"
        },
        "SCA/RML Approval": {
            "color": "#66BB6A", 
            "size": 20, 
            "shape": "dot",
            "title": "SCA/RML Approval Sub-Group"
        },
        "Availability & Recovery": {
            "color": "#66BB6A", 
            "size": 20, 
            "shape": "dot",
            "title": "Availability & Recovery Sub-Group"
        },
        "Dependencies Management": {
            "color": "#66BB6A", 
            "size": 20, 
            "shape": "dot",
            "title": "Dependencies Management Sub-Group"
        },

        # Fields (all the existing fields remain the same)
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
        "Security Classification": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Security Classification field"
        },
        "Sensitivity Classification": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Sensitivity Classification field"
        },
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
        "System Criticality": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "System Criticality (Auto-generated)"
        },
        "Designated CII": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Designated CII under Cybersecurity Act"
        },
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
        "IDSC Approval Date": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "IDSC's Approval Date"
        },
        "IDSC Approval Attachment": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "IDSC's Approval Attachment"
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
        "Total Dependencies": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Total Dependencies"
        },
        "Downstream Impact": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Downstream Impact"
        },
        "Direct Dependencies Count": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Direct Dependencies Count"
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
            "title": "Dependency Type"
        },
        "Upstream System": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Upstream System"
        },
        "Dependent System": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Dependent System"
        },
        "Data Exchange Frequency": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Data Exchange Frequency"
        },
        "Inferred Dependencies": {
            "color": "#81C784", "size": 15, "shape": "dot",
            "title": "Inferred Dependencies"
        }
    }

    # Define edges with the new hierarchical structure
    edges = [
        # Main module connections
        ("System Management", "System Identity & Classification", "", ""),
        ("System Management", "Criticality & Risk", "", ""),
        ("System Management", "System Resilience", "", ""),
        ("System Management", "Hosting and System Dependencies", "", ""),

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
        ("Organizational Context", "Agency", "", ""),
        ("Organizational Context", "Ministry Family", "", ""),

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
