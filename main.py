import streamlit as st
from pyvis.network import Network
import networkx as nx
import streamlit.components.v1 as components
import tempfile
import os

# Page config and Streamlit element hiding
st.set_page_config(
    page_title="Interactive Interdependency Graph",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit elements
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .stApp > header {display: none;}
        .main > .block-container {
            padding-top: 0;
            padding-bottom: 0;
            max-width: 100%;
        }
    </style>
""", unsafe_allow_html=True)

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
    st.title("⚙️ Data Model : System Management")

    # Define entity modules and colors
    entities = {
        "System Management": {
            "color": "#2E7D32", 
            "size": 35, 
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
        ("System Management", "System Overview", "PK: System_ID", "both"),
        ("System Management", "Criticality Assessment", "PK: System_ID", "both"),
        ("System Management", "Security & Sensitivity Classification", "PK: System_ID", "both"),
        ("System Management", "System Resiliency", "PK: System_ID", "both"),
        ("System Management", "Hosting and System Dependencies", "PK: System_ID", "both"),
        ("Risk Materiality Level", "Security & Sensitivity Classification", "relates to", "both"),
        ("Risk Materiality Level", "Hosting and System Dependencies", "relates to", "both"),
        ("Risk Materiality Level", "Criticality Assessment", "relates to", "both"),

        # System Overview field connections
        ("System Overview", "Agency", "contains", "to"),
        ("System Overview", "Ministry Family", "contains", "to"),
        ("System Overview", "System ID", "contains", "to"),
        ("System Overview", "System Name", "contains", "to"),
        ("System Overview", "System Description", "contains", "to"),
        ("System Overview", "System Status", "contains", "to"),

        # Criticality Assessment field connections
        ("Criticality Assessment", "Economy", "contains", "to"),
        ("Criticality Assessment", "Public Health and Safety", "contains", "to"),
        ("Criticality Assessment", "National Security", "contains", "to"),
        ("Criticality Assessment", "Social Preparedness", "contains", "to"),
        ("Criticality Assessment", "Public Service", "contains", "to"),
        ("Criticality Assessment", "Designated CII", "contains", "to"),
        ("Criticality Assessment", "System Criticality", "contains", "to"),
        ("Criticality Assessment", "IDSC Approval Date", "contains", "to"),
        ("Criticality Assessment", "IDSC Approval Attachment", "contains", "to"),
        ("Criticality Assessment", "MHA Approval", "contains", "to"),
        ("Criticality Assessment", "CSA Approval", "contains", "to"),
        ("Criticality Assessment", "SNDGO Approval", "contains", "to"),
        ("Criticality Assessment", "MHA Comments", "contains", "to"),
        ("Criticality Assessment", "CSA Comments", "contains", "to"),
        ("Criticality Assessment", "SNDGO Comments", "contains", "to"),

        # Security & Sensitivity Classification field connections
        ("Security & Sensitivity Classification", "Security Classification", "contains", "to"),
        ("Security & Sensitivity Classification", "Sensitivity Classification", "contains", "to"),

        # Risk Materiality Level field connections
        ("Risk Materiality Level", "Computed RML", "contains", "to"),
        ("Risk Materiality Level", "Computed RML Date", "contains", "to"),
        ("Risk Materiality Level", "Agency Proposed RML", "contains", "to"),
        ("Risk Materiality Level", "RML Alignment", "contains", "to"),
        ("Risk Materiality Level", "RML Justification", "contains", "to"),
        ("Risk Materiality Level", "Endorsed RML", "contains", "to"),
        ("Risk Materiality Level", "RML Endorsement Date", "contains", "to"),
        ("Risk Materiality Level", "Endorsement Comments", "contains", "to"),

        # System Resiliency field connections
        ("System Resiliency", "Service Availability", "contains", "to"),
        ("System Resiliency", "RTO", "contains", "to"),
        ("System Resiliency", "RPO", "contains", "to"),

        # Hosting and System Dependencies field connections
        ("Hosting and System Dependencies", "Total Dependencies", "contains", "to"),
        ("Hosting and System Dependencies", "Downstream Impact", "contains", "to"),
        ("Hosting and System Dependencies", "Direct Dependencies Count", "contains", "to"),
        ("Hosting and System Dependencies", "Dependency ID", "contains", "to"),
        ("Hosting and System Dependencies", "Dependency Status", "contains", "to"),
        ("Hosting and System Dependencies", "Dependency Type", "contains", "to"),
        ("Hosting and System Dependencies", "Upstream System", "contains", "to"),
        ("Hosting and System Dependencies", "Dependent System", "contains", "to"),
        ("Hosting and System Dependencies", "Data Exchange Frequency", "contains", "to"),
        ("Hosting and System Dependencies", "Inferred Dependencies", "contains", "to")
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

    # Create interactive PyVis network with full viewport height
    net = Network(height="100vh", width="100%", directed=True, notebook=True)
    net.from_nx(G)

    # Set options for better spacing and reduced overlapping
    net.set_options('{' + '''
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
                "springLength": 2000,
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
    ''' + '}')

    # Add JavaScript for highlighting
    highlight_js = """
    network.on("click", function(params) {
        if (params.nodes.length > 0) {
            var selectedNode = params.nodes[0];
            var connectedNodes = new Set([selectedNode]);
            var connectedEdges = new Set();
            
            network.getConnectedNodes(selectedNode).forEach(function(connectedNode) {
                connectedNodes.add(connectedNode);
                network.getConnectedEdges(selectedNode).forEach(function(edgeId) {
                    connectedEdges.add(edgeId);
                });
            });

            Object.values(network.body.nodes).forEach(function(node) {
                if (connectedNodes.has(node.id)) {
                    node.options.opacity = 1.0;
                } else {
                    node.options.opacity = 0.2;
                }
            });
            
            Object.values(network.body.edges).forEach(function(edge) {
                if (connectedEdges.has(edge.id)) {
                    edge.options.opacity = 1.0;
                } else {
                    edge.options.opacity = 0.2;
                }
            });
        } else {
            Object.values(network.body.nodes).forEach(node => {
                node.options.opacity = 1.0;
            });
            Object.values(network.body.edges).forEach(edge => {
                edge.options.opacity = 1.0;
            });
        }
        network.redraw();
    });
    """

    # Add enhanced CSS for fullscreen and layout
    st.markdown("""
        <style>
            .fullscreen-button {
                position: absolute;
                top: 10px;
                right: 10px;
                z-index: 1000;
                padding: 10px;
                background: #2E7D32;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            .fullscreen-button:hover {
                background: #1B5E20;
            }
            .element-container iframe {
                height: 100vh !important;
                width: 100vw !important;
                position: fixed !important;
                top: 0 !important;
                left: 0 !important;
                z-index: 99 !important;
            }
            .main > .block-container {
                padding-top: 0;
                padding-bottom: 0;
                max-width: 100%;
            }
        </style>
    """, unsafe_allow_html=True)

    # Create a temporary directory and save the graph
    with tempfile.TemporaryDirectory() as temp_dir:
        path = os.path.join(temp_dir, "graph.html")
        net.save_graph(path)
        
        with open(path, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        # Add fullscreen button and JavaScript
        html_content = html_content.replace('</body>', '''
            <button class="fullscreen-button" onclick="toggleFullScreen()">Toggle Fullscreen</button>
            <script>
                function toggleFullScreen() {
                    const iframe = document.querySelector('iframe');
                    if (!document.fullscreenElement) {
                        iframe.requestFullscreen().catch(err => {
                            alert(`Error attempting to enable fullscreen: ${err.message}`);
                        });
                    } else {
                        document.exitFullscreen();
                    }
                }
            </script>
            ''' + f'<script>{highlight_js}</script></body>')
        
        # Display the graph with maximum dimensions
        components.html(html_content, height=1000, width=1000, scrolling=False)

else:
    st.stop()  # Don't run the rest of the app
