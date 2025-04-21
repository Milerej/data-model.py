import streamlit as st
from pyvis.network import Network
import networkx as nx
import streamlit.components.v1 as components
import tempfile
import os
import random
from datetime import datetime, timedelta
import pandas as pd

def generate_random_date(start_year=2015):
    start_date = datetime(start_year, 1, 1)
    end_date = datetime.now()
    days_between_dates = (end_date - start_date).days
    random_number_of_days = random.randrange(days_between_dates)
    return (start_date + timedelta(days=random_number_of_days)).strftime("%Y-%m-%d")

def generate_system_data(system_number):
    agencies = ["AGD", "CSA", "GovTech", "IRAS", "MHA", "MOE", "MOF", "MOH"]
    ministry_families = ["PMO", "MHA", "MOF", "MOE", "MOH"]
    security_classifications = ["Official", "Restricted", "Confidential", "Secret"]
    sensitivity_classifications = ["Normal", "Sensitive", "Sensitive High"]
    criticality_levels = ["Low", "Medium", "High"]
    rml_levels = ["1", "2", "3", "4", "5"]
    dependency_types = ["API", "Database", "File Transfer", "Web Service"]
    
    return {
        "System Identity & Classification": {
            "System ID": f"SYS{random.randint(1000, 9999)}",
            "System Name": f"System {system_number}",
            "System Description": f"Description for System {system_number}",
            "System Status": random.choice(["Active", "Inactive", "Maintenance"]),
            "Operational Date": generate_random_date(),
            "Decommission Date": generate_random_date(2025),
            "Agency Name": random.choice(agencies),
            "Ministry Family Name": random.choice(ministry_families),
            "Security Classification": random.choice(security_classifications),
            "Sensitivity Classification": random.choice(sensitivity_classifications)
        },
        "Criticality & Risk": {
            "Economy": random.choice(criticality_levels),
            "Public Health and Safety": random.choice(criticality_levels),
            "National Security": random.choice(criticality_levels),
            "Social Preparedness": random.choice(criticality_levels),
            "Public Service": random.choice(criticality_levels),
            "System Criticality": random.choice(criticality_levels),
            "Designated CII": random.choice(["Yes", "No"]),
            "Computed RML": random.choice(rml_levels),
            "Computed RML Date": generate_random_date(),
            "Agency Proposed RML": random.choice(rml_levels),
            "RML Alignment": random.choice(["Aligned", "Not Aligned"]),
            "Endorsed RML": random.choice(rml_levels),
            "RML Endorsement Date": generate_random_date()
        },
        "System Resilience": {
            "Service Availability": f"{random.randint(90, 100)}%",
            "RTO": random.randint(1, 24),
            "RPO": random.randint(1, 12)
        },
        "Dependencies": {
            "Dependency Type": random.choice(dependency_types),
            "Dependency Status": random.choice(["Active", "Inactive"])
        }
    }

# Initialize session state for password check
if 'password_correct' not in st.session_state:
    st.session_state.password_correct = False

def check_password():
    """Returns `True` if the user had the correct password."""
    if st.session_state.password_correct:
        return True

    password = st.text_input("Password", type="password")
    if password == "Showmethemoney":
        st.session_state.password_correct = True
        return True
    elif password:
        st.error("⚠️ Password incorrect")
        return False
    return False


# Main app
if check_password():
    st.set_page_config(page_title="System Impact Analysis", layout="wide")
    st.title("🔄 System Impact Analysis")

    # Initialize session state for systems data if not exists
    if 'systems_data' not in st.session_state:
        st.session_state.systems_data = {
            f"System {i}": generate_system_data(i) for i in range(1, 51)
        }

    # Create network graph
    G = nx.DiGraph()
    
    # Add nodes
    for system_name, system_info in st.session_state.systems_data.items():
        G.add_node(system_name, **system_info)

    # Generate dependencies if not in session state
    if 'dependencies' not in st.session_state:
        st.session_state.dependencies = []
        for system_name in st.session_state.systems_data.keys():
            num_dependencies = random.randint(1, 3)
            possible_targets = [s for s in st.session_state.systems_data.keys() if s != system_name]
            if possible_targets:
                targets = random.sample(possible_targets, min(num_dependencies, len(possible_targets)))
                for target in targets:
                    dependency_type = random.choice(["API", "Database", "File Transfer", "Web Service"])
                    st.session_state.dependencies.append((system_name, target, dependency_type))

    # Add edges from session state
    for source, target, dep_type in st.session_state.dependencies:
        G.add_edge(source, target, dependency_type=dep_type)

    # Sidebar for system selection
    system_options = ["Show All Systems"] + sorted(list(st.session_state.systems_data.keys()))
    
    # Initialize session state for selected system if not exists
    if 'selected_system' not in st.session_state:
        st.session_state.selected_system = "Show All Systems"
    
    # Create the selectbox with a key
    selected_system = st.sidebar.selectbox(
        "Select a system to analyze impact:",
        options=system_options,
        key='system_selector',
        index=system_options.index(st.session_state.selected_system)
    )
    
    # Update session state
    st.session_state.selected_system = selected_system

    # Create network visualization
    net = Network(height="800px", width="100%", directed=True, bgcolor='#ffffff')


    if selected_system == "Show All Systems":
        # Show all systems with default color
        for node in G.nodes():
            system_info = st.session_state.systems_data[node]
            criticality = system_info["Criticality & Risk"]["System Criticality"]
            # Color coding based on system criticality
            color = {
                "High": "#FF4444",    # Red for high criticality
                "Medium": "#FFAA00",   # Orange for medium criticality
                "Low": "#44AA44"      # Green for low criticality
            }.get(criticality, "#CCCCCC")
            
            # Create detailed tooltip
            tooltip = f"""
System: {node}
Criticality: {criticality}
RML: {system_info['Criticality & Risk']['Endorsed RML']}
Status: {system_info['System Identity & Classification']['System Status']}
Agency: {system_info['System Identity & Classification']['Agency Name']}
Ministry: {system_info['System Identity & Classification']['Ministry Family Name']}
"""
            net.add_node(node, color=color, title=tooltip)
            
        # Add legend to sidebar
        st.sidebar.markdown("### Color Legend")
        st.sidebar.markdown("🔴 High Criticality")
        st.sidebar.markdown("🟠 Medium Criticality")
        st.sidebar.markdown("🟢 Low Criticality")
        
        # Show overall statistics
        st.sidebar.markdown("### System Statistics")
        criticality_counts = {
            "High": sum(1 for s in st.session_state.systems_data.values() 
                       if s["Criticality & Risk"]["System Criticality"] == "High"),
            "Medium": sum(1 for s in st.session_state.systems_data.values() 
                         if s["Criticality & Risk"]["System Criticality"] == "Medium"),
            "Low": sum(1 for s in st.session_state.systems_data.values() 
                      if s["Criticality & Risk"]["System Criticality"] == "Low")
        }
        st.sidebar.markdown(f"Total Systems: {len(G.nodes())}")
        st.sidebar.markdown(f"High Criticality: {criticality_counts['High']}")
        st.sidebar.markdown(f"Medium Criticality: {criticality_counts['Medium']}")
        st.sidebar.markdown(f"Low Criticality: {criticality_counts['Low']}")
        st.sidebar.markdown(f"Total Dependencies: {len(G.edges())}")

    else:
        # Impact analysis for selected system
        impacted_systems = set()
        def find_dependencies(node, visited):
            if node not in visited:
                visited.add(node)
                impacted_systems.add(node)
                for successor in G.successors(node):
                    find_dependencies(successor, visited)
                for predecessor in G.predecessors(node):
                    find_dependencies(predecessor, visited)

        find_dependencies(selected_system, set())

        # Display system details
        st.sidebar.markdown("### Selected System Details")
        system_info = st.session_state.systems_data[selected_system]
        
        for category, details in system_info.items():
            st.sidebar.markdown(f"#### {category}")
            for key, value in details.items():
                st.sidebar.markdown(f"**{key}:** {value}")

        # Impact Analysis
        st.sidebar.markdown("### Impact Analysis")
        st.sidebar.markdown(f"**Number of Impacted Systems:** {len(impacted_systems) - 1}")

        # Add nodes with impact-based colors
        for node in G.nodes():
            system_info = st.session_state.systems_data[node]
            if node == selected_system:
                color = "#FF0000"  # Red for selected system
            elif node in impacted_systems:
                color = "#FFA500"  # Orange for impacted systems
            else:
                color = "#CCCCCC"  # Grey for unimpacted systems
            
            tooltip = f"""
System: {node}
Criticality: {system_info['Criticality & Risk']['System Criticality']}
RML: {system_info['Criticality & Risk']['Endorsed RML']}
Status: {system_info['System Identity & Classification']['System Status']}
Agency: {system_info['System Identity & Classification']['Agency Name']}
Ministry: {system_info['System Identity & Classification']['Ministry Family Name']}
"""
            net.add_node(node, color=color, title=tooltip)

    # Add edges with dependency type information
    for edge in G.edges(data=True):
        source, target = edge[0], edge[1]
        dep_type = edge[2].get('dependency_type', 'Unknown')
        net.add_edge(source, target, title=f"Dependency Type: {dep_type}")

    # Set network options
    net.set_options("""
    {
        "physics": {
            "enabled": true,
            "forceAtlas2Based": {
                "gravitationalConstant": -50,
                "centralGravity": 0.01,
                "springLength": 100,
                "springConstant": 0.08
            },
            "solver": "forceAtlas2Based",
            "stabilization": {"iterations": 100}
        },
        "edges": {
            "smooth": {"type": "continuous"},
            "arrows": {"to": {"enabled": true}},
            "color": {"inherit": false, "color": "#666666"}
        },
        "nodes": {
            "font": {
                "size": 12
            },
            "borderWidth": 2,
            "borderWidthSelected": 4
        },
        "interaction": {
            "hover": true,
            "navigationButtons": true,
            "keyboard": {
                "enabled": true
            }
        }
    }
    """)

    # Display the network
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as tmp_file:
            net.save_graph(tmp_file.name)
            with open(tmp_file.name, 'r', encoding='utf-8') as f:
                components.html(f.read(), height=800)
            os.unlink(tmp_file.name)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
