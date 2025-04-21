import streamlit as st
from pyvis.network import Network
import networkx as nx
import streamlit.components.v1 as components
import tempfile
import os
import random
from datetime import datetime, timedelta
import pandas as pd

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
                    st.session_state.dependencies.append((system_name, target))

    # Add edges from session state
    for source, target in st.session_state.dependencies:
        G.add_edge(source, target)

    # Sidebar for system selection - now with "Show All Systems" as default
    selected_system = st.sidebar.selectbox(
        "Select a system to analyze impact:",
        options=["Show All Systems"] + sorted(st.session_state.systems_data.keys())
    )

    # Create network visualization
    net = Network(height="800px", width="100%", directed=True)
    
    if selected_system == "Show All Systems":
        # Show all systems with default color
        for node in G.nodes():
            system_info = st.session_state.systems_data[node]
            criticality = system_info["Criticality & Risk"]["System Criticality"]
            # Color coding based on system criticality
            color = {
                "High": "#FF4444",    # Red for high criticality
                "Medium": "#FFAA00",  # Orange for medium criticality
                "Low": "#44AA44"      # Green for low criticality
            }.get(criticality, "#CCCCCC")
            
            # Create detailed tooltip
            tooltip = f"""
System: {node}
Criticality: {criticality}
RML: {system_info['Criticality & Risk']['Endorsed RML']}
Status: {system_info['System Identity & Classification']['System Status']}
Agency: {system_info['System Identity & Classification']['Agency Name']}
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
        # Existing impact analysis logic for selected system
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
            if node == selected_system:
                color = "#FF0000"  # Red for selected system
            elif node in impacted_systems:
                color = "#FFA500"  # Orange for impacted systems
            else:
                color = "#CCCCCC"  # Grey for unimpacted systems
            
            system_info = st.session_state.systems_data[node]
            tooltip = f"""
System: {node}
Criticality: {system_info['Criticality & Risk']['System Criticality']}
RML: {system_info['Criticality & Risk']['Endorsed RML']}
Status: {system_info['System Identity & Classification']['System Status']}
Agency: {system_info['System Identity & Classification']['Agency Name']}
"""
            net.add_node(node, color=color, title=tooltip)

    # Add edges
    for edge in G.edges():
        net.add_edge(edge[0], edge[1])

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
            "arrows": {"to": {"enabled": true}}
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

    # Export functionality
    if selected_system != "Show All Systems":
        if st.sidebar.button("Export Impact Analysis"):
            impact_data = {
                "Selected System": selected_system,
                "Impacted Systems": list(impacted_systems),
                "System Details": system_info
            }
            st.sidebar.download_button(
                "Download Analysis Report",
                data=pd.DataFrame([impact_data]).to_csv(index=False),
                file_name=f"impact_analysis_{selected_system}.csv",
                mime="text/csv"
            )
