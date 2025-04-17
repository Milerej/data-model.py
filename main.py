import streamlit as st
from pyvis.network import Network
import networkx as nx
import streamlit.components.v1 as components
import tempfile
import os
import time

# Set page config once at the start
st.set_page_config(page_title="Interactive Interdependency Graph", layout="wide")

# Initialize session state
if 'graph_key' not in st.session_state:
    st.session_state.graph_key = 0

# Password check function
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


# Define relationships between entities
edges = [
    # Agency Management Module connections
    ("Agency Management", "Agency"),
    ("Agency Management", "Key Appointment Holder"),
    
    # Agency connections
    ("Agency", "Basic Information"),
    ("Basic Information", "Agency Name"),
    ("Basic Information", "Agency Abbreviation (Short Form)"),
    ("Basic Information", "Agency Operational Status"),
    ("Basic Information", "Ministry Family"),
    
    # Key Appointment Holder connections
    ("Key Appointment Holder", "Full Name"),
    ("Key Appointment Holder", "Designation"),
    ("Key Appointment Holder", "Email"),
    
    # System Management Module connections
    ("System Management", "System Identity & Classification"),
    ("System Management", "Criticality & Risk"),
    ("System Management", "System Resilience"),
    ("System Management", "Hosting and System Dependencies"),
    
    # System Identity & Classification connections
    ("System Identity & Classification", "Basic Information"),
    ("System Identity & Classification", "Organizational Context"),
    ("System Identity & Classification", "Classification"),
    
    # Basic Information (System) connections
    ("Basic Information", "System ID"),
    ("Basic Information", "System Name"),
    ("Basic Information", "System Description"),
    ("Basic Information", "System Status"),
    
    # Classification connections
    ("Classification", "Security Classification"),
    ("Classification", "Sensitivity Classification"),
    
    # Criticality & Risk connections
    ("Criticality & Risk", "Impact Assessment"),
    ("Criticality & Risk", "Risk Profile"),
    ("Criticality & Risk", "SCA/RML Approval"),
    
    # Impact Assessment connections
    ("Impact Assessment", "Economy"),
    ("Impact Assessment", "Public Health and Safety"),
    ("Impact Assessment", "National Security"),
    ("Impact Assessment", "Social Preparedness"),
    ("Impact Assessment", "Public Service"),
    
    # Risk Profile connections
    ("Risk Profile", "System Criticality"),
    ("Risk Profile", "Designated CII"),
    ("Risk Profile", "Computed RML"),
    ("Risk Profile", "Computed RML Date"),
    ("Risk Profile", "Agency Proposed RML"),
    ("Risk Profile", "RML Alignment"),
    ("Risk Profile", "RML Justification"),
    
    # SCA/RML Approval connections
    ("SCA/RML Approval", "Endorsed RML"),
    ("SCA/RML Approval", "RML Endorsement Date"),
    ("SCA/RML Approval", "Endorsement Comments"),
    ("SCA/RML Approval", "IDSC Approval Date"),
    ("SCA/RML Approval", "IDSC Approval Attachment"),
    ("SCA/RML Approval", "MHA Approval"),
    ("SCA/RML Approval", "CSA Approval"),
    ("SCA/RML Approval", "SNDGO Approval"),
    ("SCA/RML Approval", "MHA Comments"),
    ("SCA/RML Approval", "CSA Comments"),
    ("SCA/RML Approval", "SNDGO Comments"),
    
    # System Resilience connections
    ("System Resilience", "Availability & Recovery"),
    ("Availability & Recovery", "Service Availability"),
    ("Availability & Recovery", "RTO"),
    ("Availability & Recovery", "RPO"),
    
    # Hosting and System Dependencies connections
    ("Hosting and System Dependencies", "Dependencies Management"),
    ("Dependencies Management", "Total Dependencies"),
    ("Dependencies Management", "Downstream Impact"),
    ("Dependencies Management", "Direct Dependencies Count"),
    ("Dependencies Management", "Dependency ID"),
    ("Dependencies Management", "Dependency Status"),
    ("Dependencies Management", "Dependency Type"),
    ("Dependencies Management", "Upstream System"),
    ("Dependencies Management", "Dependent System"),
    ("Dependencies Management", "Data Exchange Frequency"),
    ("Dependencies Management", "Inferred Dependencies"),
    
    # Organizational Context connections
    ("Organizational Context", "Ministry Family Name"),
]

def create_network():
    # Create network
    net = Network(height="750px", width="100%", bgcolor="#ffffff", font_color="black")
    net.force_atlas_2based()
    
    # Add nodes
    for node, attributes in entities.items():
        net.add_node(
            node,
            color=attributes["color"],
            size=attributes["size"],
            shape=attributes["shape"],
            title=attributes["title"]
        )
    
    # Add edges
    for edge in edges:
        net.add_edge(edge[0], edge[1], color="#808080")
    
    # Set physics layout options
    net.set_options("""
    const options = {
      "physics": {
        "enabled": true,
        "forceAtlas2Based": {
          "gravitationalConstant": -50,
          "centralGravity": 0.01,
          "springLength": 200,
          "springConstant": 0.08,
          "damping": 0.9,
          "avoidOverlap": 1
        },
        "maxVelocity": 15,
        "minVelocity": 0.75,
        "solver": "forceAtlas2Based",
        "stabilization": {
          "enabled": true,
          "iterations": 1000,
          "updateInterval": 25,
          "fit": true
        },
        "timestep": 0.3,
        "adaptiveTimestep": true
      },
      "interaction": {
        "hover": true,
        "tooltipDelay": 300,
        "dragNodes": true,
        "dragView": true,
        "zoomView": true
      },
      "edges": {
        "smooth": {
          "type": "continuous",
          "forceDirection": "none"
        }
      }
    }
    """)
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as tmp_file:
        net.save_graph(tmp_file.name)
        return tmp_file.name

def get_network_html():
    # Create a unique key for the current graph state
    current_time = int(time.time())
    if st.session_state.graph_key != current_time:
        st.session_state.graph_key = current_time
        
        # Generate the network
        tmp_file_path = create_network()
        
        # Read the file content
        with open(tmp_file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
            
        # Delete the temporary file
        os.unlink(tmp_file_path)
        
        return html_content
    return None

def main():
    if not check_password():
        st.stop()

    # Title and description
    st.title("Interactive System Interdependency Graph")
    st.markdown("""
    This interactive graph visualizes the relationships between different components 
    in the system. You can:
    * Drag nodes to rearrange the layout
    * Zoom in/out using mouse wheel
    * Hover over nodes to see details
    * Click and drag the background to pan
    * Double-click to reset the view
    """)

    # Add a refresh button
    if st.button("Refresh Graph"):
        st.session_state.graph_key = 0

    # Create tabs
    tab1, tab2 = st.tabs(["Graph View", "Legend"])

    with tab1:
        # Display the network
        html_content = get_network_html()
        if html_content:
            components.html(html_content, height=800)

    with tab2:
        # Create legend
        st.header("Legend")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Node Colors")
            st.markdown(f"""
            * <span style='color:{AGENCY_COLOR}'>●</span> Blue: Agency/Ministry related
            * <span style='color:{SYSTEM_COLOR}'>●</span> Green: System related
            """, unsafe_allow_html=True)
            
            st.subheader("Node Sizes")
            st.markdown("""
            * Large: Main modules
            * Medium: Sub-modules
            * Small: Groups
            * Tiny: Fields
            """)

        with col2:
            st.subheader("Modules")
            st.markdown("""
            * Agency Management
                * Agency
                * Key Appointment Holder
            * System Management
                * System Identity & Classification
                * Criticality & Risk
                * System Resilience
                * Hosting and System Dependencies
            """)

        st.markdown("""
        ---
        ### Navigation Tips
        1. **Zoom**: Use mouse wheel to zoom in/out
        2. **Pan**: Click and drag the background
        3. **Move Nodes**: Click and drag individual nodes
        4. **View Details**: Hover over nodes to see additional information
        5. **Reset View**: Double-click on the background
        """)

if __name__ == "__main__":
    main()
