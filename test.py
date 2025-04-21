import streamlit as st
# Must be the first Streamlit command
st.set_page_config(page_title="System Impact Analysis", layout="wide")

from pyvis.network import Network
import networkx as nx
import streamlit.components.v1 as components
import tempfile
import os
import random
from datetime import datetime, timedelta
import pandas as pd

# Initialize session state for password check
if 'password_correct' not in st.session_state:
    st.session_state.password_correct = False

def generate_random_date(start_year=2015):
    start_date = datetime(start_year, 1, 1)
    end_date = datetime.now()
    days_between_dates = (end_date - start_date).days
    random_number_of_days = random.randrange(days_between_dates)
    return (start_date + timedelta(days=random_number_of_days)).strftime("%Y-%m-%d")

def generate_system_data(system_number):
    agencies = ["Agency 1", "Agency 2", "Agency 3", "Agency 4", "Agency 5", "Agency 6", "Agency 7", "Agency 8"]
    ministry_families = ["MF 1", "MF 2", "MF 3", "MF 4", "MF 5"]
    security_classifications = ["Official", "Restricted", "Confidential", "Secret"]
    sensitivity_classifications = ["Sensitive Normal", "Non-Sensitive", "Sensitive High"]
    system_criticality = ["Others", "SII", "High"]
    rml_levels = ["Low", "Medium", "High"]
    dependency_types = ["Upstream", "Downstream"]
    
    # Logic to ensure consistent criticality and RML relationships
    chosen_criticality = random.choice(system_criticality)
    
    # Determine RML based on criticality
    if chosen_criticality == "High":
        possible_rml = ["Medium", "High"]
        recommended_rml = "High"
    elif chosen_criticality == "SII":
        possible_rml = ["Medium", "High"]
        recommended_rml = "Medium"
    else:  # Others
        possible_rml = ["Low", "Medium"]
        recommended_rml = "Low"
        
    computed_rml = random.choice(possible_rml)
    agency_proposed_rml = random.choice(possible_rml)
    endorsed_rml = recommended_rml  # Using recommended RML as endorsed RML
    
    # Determine RML alignment
    rml_alignment = "Aligned" if computed_rml == endorsed_rml else "Not Aligned"
    
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
            "System Criticality": chosen_criticality,
            "Computed RML": computed_rml,
            "Computed RML Date": generate_random_date(),
            "Agency Proposed RML": agency_proposed_rml,
            "RML Alignment": rml_alignment,
            "Endorsed RML": endorsed_rml,
            "RML Endorsement Date": generate_random_date()
        },
        "System Resilience": {
            "Service Availability": f"{random.randint(90, 100)}%",
            "RTO": f"{random.randint(1, 24)} hours",
            "RPO": f"{random.randint(1, 12)} hours"
        },
        "Dependencies": {
            "Dependency Type": random.choice(dependency_types),
            "Dependency Status": random.choice(["Active", "Inactive"])
        }
    }

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

    # Generate dependencies with hierarchical structure
    if 'dependencies' not in st.session_state:
        st.session_state.dependencies = []
        
        # Create layered hierarchy (10 layers)
        systems_list = list(st.session_state.systems_data.keys())
        
        # Sort systems by criticality to ensure high criticality systems are at the top
        systems_by_criticality = {
            "High": [],
            "SII": [],
            "Others": []
        }
        
        for system in systems_list:
            criticality = st.session_state.systems_data[system]["Criticality & Risk"]["System Criticality"]
            systems_by_criticality[criticality].append(system)
        
        # Create layers
        layers = [[] for _ in range(10)]  # 10 layers
        
        # Layer 0 (top) - Primarily High criticality systems
        top_systems = (systems_by_criticality["High"] + 
                      systems_by_criticality["SII"])[:5]
        layers[0] = top_systems
        remaining_systems = [s for s in systems_list if s not in top_systems]
        
        # Distribute remaining systems across layers
        for layer_idx in range(1, 10):
            # Number of systems in this layer (more in middle layers, fewer in bottom layers)
            if layer_idx < 5:
                num_systems = random.randint(4, 8)  # More systems in upper-middle layers
            else:
                num_systems = random.randint(2, 5)  # Fewer systems in lower layers
                
            if remaining_systems:
                layer_systems = random.sample(remaining_systems, 
                                            min(num_systems, len(remaining_systems)))
                layers[layer_idx] = layer_systems
                remaining_systems = [s for s in remaining_systems 
                                   if s not in layer_systems]
        
        # Create dependencies between layers
        for layer_idx in range(len(layers) - 1):
            current_layer = layers[layer_idx]
            next_layer = layers[layer_idx + 1]
            
            for system in current_layer:
                # Create 2-4 downstream dependencies to next layer
                num_dependencies = random.randint(2, 4)
                if next_layer:
                    downstream_systems = random.sample(next_layer, 
                                                     min(num_dependencies, len(next_layer)))
                    for downstream in downstream_systems:
                        st.session_state.dependencies.append((system, downstream, "Downstream"))
                        
                        # Add some cross-layer dependencies (skip connections)
                        if random.random() < 0.3 and layer_idx + 2 < len(layers):  # 30% chance
                            skip_layer = layers[layer_idx + 2]
                            if skip_layer:
                                skip_system = random.choice(skip_layer)
                                st.session_state.dependencies.append((downstream, skip_system, 
                                                                   "Downstream"))
        
        # Add some upstream dependencies
        for layer_idx in range(1, len(layers)):
            current_layer = layers[layer_idx]
            upper_layer = layers[layer_idx - 1]
            
            for system in current_layer:
                # 20% chance of creating an upstream dependency
                if random.random() < 0.2 and upper_layer:
                    upstream = random.choice(upper_layer)
                    st.session_state.dependencies.append((system, upstream, "Upstream"))

    # Add edges from session state
    for source, target, dep_type in st.session_state.dependencies:
        G.add_edge(source, target, dependency_type=dep_type)

    # Sidebar for layout selection and system selection
    layout_type = st.sidebar.radio(
        "Select Layout Type",
        ["Force-Directed", "Hierarchical"],
        key="layout_selector"
    )

    system_options = ["Show All Systems"] + sorted(list(st.session_state.systems_data.keys()))
    
    # Initialize session state for selected system if not exists
    if 'selected_system' not in st.session_state:
        st.session_state.selected_system = "Show All Systems"
    
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
                "SII": "#FFAA00",     # Orange for SII
                "Others": "#44AA44"   # Green for others
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
            
        # Show overall statistics
        st.sidebar.markdown("### System Statistics")
        criticality_counts = {
            "High": sum(1 for s in st.session_state.systems_data.values() 
                       if s["Criticality & Risk"]["System Criticality"] == "High"),
            "SII": sum(1 for s in st.session_state.systems_data.values() 
                      if s["Criticality & Risk"]["System Criticality"] == "SII"),
            "Others": sum(1 for s in st.session_state.systems_data.values() 
                        if s["Criticality & Risk"]["System Criticality"] == "Others")
        }

        st.sidebar.markdown(f"Total Systems: {len(G.nodes())}")
        st.sidebar.markdown(f"High Criticality: {criticality_counts['High']}")
        st.sidebar.markdown(f"SII Systems: {criticality_counts['SII']}")
        st.sidebar.markdown(f"Other Systems: {criticality_counts['Others']}")
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

        # Add nodes with impact-based colors
        for node in G.nodes():
            system_info = st.session_state.systems_data[node]
            criticality = system_info["Criticality & Risk"]["System Criticality"]
            
            if node == selected_system:
                color = "#FF0000"  # Red for selected system
            elif node in impacted_systems:
                color = {
                    "High": "#FF6666",    # Lighter red for high criticality
                    "SII": "#FFCC66",     # Lighter orange for SII
                    "Others": "#66CC66"   # Lighter green for others
                }.get(criticality, "#CCCCCC")
            else:
                color = {
                    "High": "#FF4444",    # Red for high criticality
                    "SII": "#FFAA00",     # Orange for SII
                    "Others": "#44AA44"   # Green for others
                }.get(criticality, "#CCCCCC")
            
            tooltip = f"""
System: {node}
Criticality: {criticality}
RML: {system_info['Criticality & Risk']['Endorsed RML']}
Status: {system_info['System Identity & Classification']['System Status']}
Agency: {system_info['System Identity & Classification']['Agency Name']}
Ministry: {system_info['System Identity & Classification']['Ministry Family Name']}
"""
            net.add_node(node, color=color, title=tooltip)

    # Add edges with visual distinction between upstream and downstream
    for edge in G.edges(data=True):
        source, target = edge[0], edge[1]
        dep_type = edge[2].get('dependency_type', 'Unknown')
        edge_color = "#FF0000" if dep_type == "Upstream" else "#0000FF"  # Red for upstream, Blue for downstream
        edge_style = "dashed" if dep_type == "Upstream" else "solid"
        net.add_edge(source, target, 
                    title=f"Dependency Type: {dep_type}",
                    color=edge_color,
                    style=edge_style)

    # Set network options based on layout type
    if layout_type == "Hierarchical":
        network_options = """
        {
            "physics": {
                "enabled": false
            },
            "edges": {
                "smooth": {
                    "type": "cubicBezier",
                    "forceDirection": "vertical"
                },
                "arrows": {"to": {"enabled": true}},
                "color": {
                    "inherit": false
                },
                "width": 2
            },
            "nodes": {
                "font": {
                    "size": 12,
                    "face": "Arial"
                },
                "borderWidth": 2,
                "borderWidthSelected": 4,
                "shape": "box",
                "scaling": {
                    "min": 20,
                    "max": 30
                },
                "margin": 10
            },
            "layout": {
                "hierarchical": {
                    "enabled": true,
                    "direction": "UD",
                    "sortMethod": "directed",
                    "nodeSpacing": 200,
                    "treeSpacing": 200,
                    "levelSeparation": 150,
                    "blockShifting": true,
                    "edgeMinimization": true,
                    "parentCentralization": true
                }
            },
            "interaction": {
                "hover": true,
                "navigationButtons": true,
                "keyboard": {
                    "enabled": true
                },
                "zoomView": true,
                "dragView": true
            }
        }
        """
    else:
        network_options = """
        {
            "physics": {
                "enabled": true,
                "forceAtlas2Based": {
                    "gravitationalConstant": -2000,
                    "centralGravity": 0.005,
                    "springLength": 200,
                    "springConstant": 0.05,
                    "damping": 0.9,
                    "avoidOverlap": 1
                },
                "solver": "forceAtlas2Based",
                "stabilization": {
                    "enabled": true,
                    "iterations": 200,
                    "updateInterval": 50,
                    "fit": true
                },
                "minVelocity": 0.75,
                "maxVelocity": 30
            },
            "edges": {
                "smooth": {
                    "type": "continuous"
                },
                "arrows": {"to": {"enabled": true}},
                "color": {
                    "inherit": false
                },
                "width": 2
            },
            "nodes": {
                "font": {
                    "size": 12,
                    "face": "Arial"
                },
                "borderWidth": 2,
                "borderWidthSelected": 4,
                "shape": "dot",
                "scaling": {
                    "min": 20,
                    "max": 30
                }
            },
            "interaction": {
                "hover": true,
                "navigationButtons": true,
                "keyboard": {
                    "enabled": true
                },
                "zoomView": true,
                "dragView": true
            }
        }
        """

    # Set the network options
    net.set_options(network_options)

    # Display the network
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as tmp_file:
            net.save_graph(tmp_file.name)
            with open(tmp_file.name, 'r', encoding='utf-8') as f:
                components.html(f.read(), height=800)
            os.unlink(tmp_file.name)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
