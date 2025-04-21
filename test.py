import streamlit as st
from pyvis.network import Network
import networkx as nx
import streamlit.components.v1 as components
import tempfile
import os
import random
from datetime import datetime, timedelta
import pandas as pd

def check_password():
    """Returns `True` if the user had the correct password."""
    def password_entered():
        if st.session_state["password"] == "Showmethemoney":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        st.error("⚠️ Password incorrect")
        return False
    else:
        return True

def generate_random_date(start_year=2015):
    start_date = datetime(start_year, 1, 1)
    end_date = datetime.now()
    days_between_dates = (end_date - start_date).days
    random_number_of_days = random.randrange(days_between_dates)
    return (start_date + timedelta(days=random_number_of_days)).strftime("%Y-%m-%d")

def generate_system_data(system_number):
    return {
        "System Identity & Classification": {
            "System ID": f"SYS{random.randint(1000, 9999)}",
            "System Name": f"System {system_number}",
            "System Description": f"Description for System {system_number}",
            "System Status": random.choice(["Active", "Inactive"]),
            "Operational Date": generate_random_date(),
            "Agency Name": random.choice(["AGD", "CSA", "GovTech", "IRAS"]),
            "Security Classification": random.choice(["Official", "Restricted", "Confidential"]),
        },
        "Criticality & Risk": {
            "System Criticality": random.choice(["Low", "Medium", "High"]),
            "Computed RML": str(random.randint(1, 5)),
            "Endorsed RML": str(random.randint(1, 5))
        },
        "System Resilience": {
            "Service Availability": f"{random.randint(90, 100)}%",
            "RTO": random.randint(1, 24),
            "RPO": random.randint(1, 12)
        }
    }

if check_password():
    st.set_page_config(page_title="System Impact Analysis", layout="wide")
    st.title("🔄 System Impact Analysis")

    # Initialize session state for systems data if not exists
    if 'systems_data' not in st.session_state:
        st.session_state.systems_data = {
            f"System {i}": generate_system_data(i) for i in range(1, 51)  # Reduced to 50 systems
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
            num_dependencies = random.randint(1, 3)  # Reduced number of dependencies
            possible_targets = [s for s in st.session_state.systems_data.keys() if s != system_name]
            if possible_targets:
                targets = random.sample(possible_targets, min(num_dependencies, len(possible_targets)))
                for target in targets:
                    st.session_state.dependencies.append((system_name, target))

    # Add edges from session state
    for source, target in st.session_state.dependencies:
        G.add_edge(source, target)

    # Sidebar for system selection
    selected_system = st.sidebar.selectbox(
        "Select a system to analyze impact:",
        options=["None"] + sorted(st.session_state.systems_data.keys())
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
        system_info = st.session_state.systems_data[selected_system]
        
        for category, details in system_info.items():
            st.sidebar.markdown(f"#### {category}")
            for key, value in details.items():
                st.sidebar.markdown(f"**{key}:** {value}")

        # Impact Analysis
        st.sidebar.markdown("### Impact Analysis")
        st.sidebar.markdown(f"**Number of Impacted Systems:** {len(impacted_systems) - 1}")
        
        # Create network visualization
        net = Network(height="800px", width="100%", directed=True)
        
        # Add nodes with colors
        for node in G.nodes():
            color = "#FF0000" if node == selected_system else "#FFA500" if node in impacted_systems else "#CCCCCC"
            net.add_node(node, color=color, title=node)

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
