import streamlit as st
from pyvis.network import Network
import networkx as nx
import streamlit.components.v1 as components
import tempfile
import os
import random
from datetime import datetime, timedelta
import pandas as pd

# [Previous password check function remains the same]

def generate_random_date(start_year=2015):
    """Generate a random date from start_year to current date"""
    start_date = datetime(start_year, 1, 1)
    end_date = datetime.now()
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    return start_date + timedelta(days=random_number_of_days)

def generate_system_data():
    """Generate realistic system data"""
    agencies = ["AGD", "CSA", "GovTech", "IRAS", "MHA", "MOE", "MOF", "MOH"]
    ministry_families = ["PMO", "MHA", "MOF", "MOE", "MOH"]
    security_classifications = ["Official", "Restricted", "Confidential", "Secret"]
    sensitivity_classifications = ["Normal", "Sensitive", "Sensitive High"]
    criticality_levels = ["Low", "Medium", "High", "Critical"]
    rml_levels = ["1", "2", "3", "4", "5"]
    dependency_types = ["API", "Database", "File Transfer", "Web Service"]
    
    return {
        "System Identity & Classification": {
            "System ID": f"SYS{random.randint(1000, 9999)}",
            "System Name": f"System {random.randint(1, 200)}",
            "System Description": f"This is a description for System {random.randint(1, 200)}",
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
            "Dependency Status": random.choice(["Active", "Inactive"]),
            "Downstream Dependencies": []
        }
    }

if check_password():
    st.set_page_config(page_title="System Impact Analysis", layout="wide")
    st.title("🔄 System Impact Analysis")

    # Generate systems with detailed information
    systems_data = {}
    for i in range(1, 201):
        systems_data[f"System {i}"] = generate_system_data()

    # Create network graph
    G = nx.DiGraph()
    
    # Add nodes with attributes
    for system_name, system_info in systems_data.items():
        G.add_node(system_name, **system_info)

    # Generate dependencies
    for system_name in systems_data.keys():
        num_dependencies = random.randint(2, 4)
        possible_targets = [s for s in systems_data.keys() if s != system_name]
        if possible_targets:
            targets = random.sample(possible_targets, min(num_dependencies, len(possible_targets)))
            for target in targets:
                dependency_type = random.choice(["API", "Database", "File Transfer", "Web Service"])
                G.add_edge(system_name, target, 
                          dependency_type=dependency_type,
                          title=f"{dependency_type} dependency")
                systems_data[system_name]["Dependencies"]["Downstream Dependencies"].append(target)

    # Sidebar for system selection and analysis
    st.sidebar.title("Impact Analysis")
    selected_system = st.sidebar.selectbox(
        "Select a system to analyze impact:",
        options=["None"] + sorted(systems_data.keys())
    )

    if selected_system != "None":
        # Find impacted systems
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
        system_info = systems_data[selected_system]
        
        # System Identity
        st.sidebar.markdown("#### System Identity")
        identity_info = system_info["System Identity & Classification"]
        for key, value in identity_info.items():
            st.sidebar.markdown(f"**{key}:** {value}")

        # Criticality
        st.sidebar.markdown("#### Criticality & Risk")
        criticality_info = system_info["Criticality & Risk"]
        for key, value in criticality_info.items():
            st.sidebar.markdown(f"**{key}:** {value}")

        # Resilience
        st.sidebar.markdown("#### System Resilience")
        resilience_info = system_info["System Resilience"]
        for key, value in resilience_info.items():
            st.sidebar.markdown(f"**{key}:** {value}")

        # Impact Analysis
        st.sidebar.markdown("### Impact Analysis")
        st.sidebar.markdown(f"**Number of Impacted Systems:** {len(impacted_systems) - 1}")
        
        # Create network visualization
        net = Network(height="900px", width="100%", directed=True)
        
        # Add nodes with colors based on impact
        for node in G.nodes():
            color = "#FF0000" if node == selected_system else "#FFA500" if node in impacted_systems else "#CCCCCC"
            net.add_node(node, color=color, title=f"System: {node}\nCriticality: {systems_data[node]['Criticality & Risk']['System Criticality']}\nRML: {systems_data[node]['Criticality & Risk']['Endorsed RML']}")

        # Add edges with dependency information
        for edge in G.edges(data=True):
            net.add_edge(edge[0], edge[1], title=edge[2]['title'])

        # Network visualization options
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
                "stabilization": {"iterations": 1000}
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
                    components.html(f.read(), height=900)
                os.unlink(tmp_file.name)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

        # Export functionality
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
