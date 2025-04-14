import streamlit as st
from pyvis.network import Network
import networkx as nx
import streamlit.components.v1 as components
import tempfile
import os

st.set_page_config(page_title="Interactive Interdependency Graph", layout="wide")

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
        "title": "System Overview Module"
    },
    "Criticality Assessment": {
        "color": "#4CAF50", 
        "size": 25,
        "shape": "dot",
        "title": "Criticality Assessment Module"
    },
    "Security & Sensitivity Classification": {
        "color": "#4CAF50", 
        "size": 25, 
        "shape": "dot",
        "title": "Security & Sensitivity Classification Module"
    },
    "Risk Materiality Level": {
        "color": "#4CAF50", 
        "size": 25, 
        "shape": "dot",
        "title": "Risk Materiality Level Module"
    },
    "System Resiliency": {
        "color": "#4CAF50", 
        "size": 25, 
        "shape": "dot",
        "title": "System Resiliency Module"
    },
    "Hosting and System Dependencies": {
        "color": "#4CAF50", 
        "size": 25, 
        "shape": "dot",
        "title": "Hosting and System Dependencies Module"
    },
    "Central Programmes": {
        "color": "#4CAF50", 
        "size": 25, 
        "shape": "dot",
        "title": "Central Programmes Module"
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
    ("System Management", "Risk Materiality Level", "PK: System_ID", "both"),
    ("System Management", "System Resiliency", "PK: System_ID", "both"),
    ("System Management", "Hosting and System Dependencies", "PK: System_ID", "both"),
    ("System Management", "Central Programmes", "PK: System_ID", "both"),
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

# Create interactive PyVis network
net = Network(height="700px", width="100%", directed=True, notebook=True)
net.from_nx(G)

# Set options as a string
net.set_options('{' + '''
    "physics": {
        "enabled": true,
        "stabilization": {
            "enabled": true,
            "iterations": 1000,
            "updateInterval": 50,
            "onlyDynamicEdges": false,
            "fit": true
        },
        "barnesHut": {
            "gravitationalConstant": -8000,
            "centralGravity": 0.3,
            "springLength": 200,
            "springConstant": 0.04,
            "damping": 0.09,
            "avoidOverlap": 1
        },
        "minVelocity": 0.75,
        "maxVelocity": 45
    },
    "edges": {
        "smooth": {
            "type": "continuous",
            "forceDirection": "none"
        },
        "length": 250,
        "font": {
            "size": 12,
            "strokeWidth": 2,
            "strokeColor": "#ffffff"
        }
    },
    "nodes": {
        "font": {
            "size": 14,
            "strokeWidth": 2,
            "strokeColor": "#ffffff"
        },
        "margin": 10,
        "fixed": {
            "x": false,
            "y": false
        }
    },
    "interaction": {
        "dragNodes": true,
        "dragView": true,
        "zoomView": true,
        "hover": true
    },
    "layout": {
        "improvedLayout": true,
        "randomSeed": 42,
        "hierarchical": {
            "enabled": false,
            "nodeSpacing": 200,
            "levelSeparation": 200
        }
    }
''' + '}')

# Customize edge labels and arrows
for edge in net.edges:
    edge["label"] = edge.get("title", "")
    if edge.get("arrows") == "both":
        edge["arrows"] = "to,from"

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

# Create a temporary directory and save the graph
with tempfile.TemporaryDirectory() as temp_dir:
    path = os.path.join(temp_dir, "graph.html")
    net.save_graph(path)
    
    with open(path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # Add JavaScript
    html_content = html_content.replace('</body>', f'<script>{highlight_js}</script></body>')
    
    components.html(html_content, height=750, scrolling=True)
