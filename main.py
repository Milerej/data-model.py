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

            # Fields
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

    # Define edges
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
        ("Security Classification", "Computed RML", "", ""),
        ("Sensitivity Classification", "Computed RML", "", ""),
        ("System Criticality", "Computed RML", "", ""),
        ("Dependent System", "Computed RML", "", ""),
        
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

    # Create network
    net = Network(height='750px', width='100%', bgcolor='#ffffff', font_color='black')
    net.force_atlas_2based()

    # Add nodes
    for entity, attributes in entities.items():
        net.add_node(
            entity, 
            color=attributes["color"], 
            size=attributes["size"],
            title=attributes["title"],
            shape=attributes["shape"]
        )

    # Add edges
    for edge in edges:
        net.add_edge(edge[0], edge[1])

    # Generate HTML file
    html_file = "network.html"

    click_js = """
    <div style="position: fixed; top: 20px; right: 180px; z-index: 10000;">
        <button 
            style="
                padding: 8px 16px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-family: Arial, sans-serif;
                font-size: 14px;
                margin-right: 10px;
            "
            onclick="expandAll()"
        >
            Expand All
        </button>
        <button 
            style="
                padding: 8px 16px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-family: Arial, sans-serif;
                font-size: 14px;
            "
            onclick="collapseAll()"
        >
            Collapse All
        </button>
    </div>
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        setTimeout(function() {
            collapseAll();
        }, 1000);
    });

    function collapseAll() {
        var network = document.getElementsByClassName('vis-network')[0].__vis_network__;
        var nodes = network.body.data.nodes.get();
        var edges = network.body.data.edges.get();
        
        var nodeUpdates = [];
        var edgeUpdates = [];
        
        nodes.forEach(function(node) {
            if (node.size === 15) {
                nodeUpdates.push({id: node.id, hidden: true});
            }
        });
        
        edges.forEach(function(edge) {
            var fromNode = nodes.find(n => n.id === edge.from);
            var toNode = nodes.find(n => n.id === edge.to);
            if ((fromNode && fromNode.size === 15) || (toNode && toNode.size === 15)) {
                edgeUpdates.push({id: edge.id, hidden: true});
            }
        });
        
        network.body.data.nodes.update(nodeUpdates);
        network.body.data.edges.update(edgeUpdates);
    }

    function expandAll() {
        var network = document.getElementsByClassName('vis-network')[0].__vis_network__;
        var nodes = network.body.data.nodes.get();
        var edges = network.body.data.edges.get();
        
        var nodeUpdates = [];
        var edgeUpdates = [];
        
        nodes.forEach(function(node) {
            if (node.size === 15) {
                nodeUpdates.push({id: node.id, hidden: false});
            }
        });
        
        edges.forEach(function(edge) {
            var fromNode = nodes.find(n => n.id === edge.from);
            var toNode = nodes.find(n => n.id === edge.to);
            if ((fromNode && fromNode.size === 15) || (toNode && toNode.size === 15)) {
                edgeUpdates.push({id: edge.id, hidden: false});
            }
        });
        
        network.body.data.nodes.update(nodeUpdates);
        network.body.data.edges.update(edgeUpdates);
    }

    function toggleConnectedNodes(nodeId) {
        var network = document.getElementsByClassName('vis-network')[0].__vis_network__;
        var connectedNodes = network.getConnectedNodes(nodeId);
        var connectedEdges = network.getConnectedEdges(nodeId);
        var allNodes = network.body.data.nodes.get();
        var nodeUpdates = [];
        var edgeUpdates = [];
        
        // Find the clicked node
        var clickedNode = allNodes.find(n => n.id === nodeId);
        if (clickedNode.size === 15) return; // Don't toggle if clicking on a field node
        
        connectedNodes.forEach(function(connectedNodeId) {
            var node = allNodes.find(n => n.id === connectedNodeId);
            if (node && node.size === 15) {
                nodeUpdates.push({id: connectedNodeId, hidden: !node.hidden});
            }
        });
        
        connectedEdges.forEach(function(edgeId) {
            var edge = network.body.data.edges.get(edgeId);
            var fromNode = allNodes.find(n => n.id === edge.from);
            var toNode = allNodes.find(n => n.id === edge.to);
            if ((fromNode && fromNode.size === 15) || (toNode && toNode.size === 15)) {
                edgeUpdates.push({id: edgeId, hidden: !edge.hidden});
            }
        });
        
        network.body.data.nodes.update(nodeUpdates);
        network.body.data.edges.update(edgeUpdates);
    }

    document.getElementsByClassName('vis-network')[0].addEventListener('click', function(e) {
        var network = this.__vis_network__;
        var selection = network.getNodeAt(e.pointer.DOM);
        if (selection !== undefined) {
            toggleConnectedNodes(selection);
        }
    });
    </script>
    """

    # Save and read the network
    net.save_graph(html_file)
    
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
        
    # Insert the click handling JavaScript just before the </body> tag
    modified_html = html_content.replace('</body>', f'{click_js}</body>')
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(modified_html)

    # Display the network in Streamlit
    with open(html_file, 'r', encoding='utf-8') as f:
        components.html(f.read(), height=800)

    # Clean up the temporary file
    os.remove(html_file)
