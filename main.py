import streamlit as st
from pyvis.network import Network
import networkx as nx
import streamlit.components.v1 as components
import html

# This MUST be the first Streamlit command
st.set_page_config(page_title="Interactive Interdependency Graph", layout="wide")

st.title("🧠 Interactive Data Model Interdependency Chart")

# Define entity modules with fields and relationships
entities = {
    "Ministry Family": {
        "color": "blue",
        "fields": [
            {"name": "Ministry_ID", "is_key": True},
            {"name": "Ministry_Name", "is_key": False},
            {"name": "Description", "is_key": False}
        ],
        "type": "Entity"
    },
    "Agency": {
        "color": "blue",
        "fields": [
            {"name": "Agency_ID", "is_key": True},
            {"name": "Agency_Name", "is_key": False},
            {"name": "Ministry_ID", "is_foreign_key": True, "references": "Ministry Family"},
            {"name": "Status", "is_key": False}
        ],
        "type": "Entity"
    },
    "System Overview": {
        "color": "teal",
        "fields": [
            {"name": "System_ID", "is_key": True},
            {"name": "System_Name", "is_key": False},
            {"name": "Agency_ID", "is_foreign_key": True, "references": "Agency"},
            {"name": "Description", "is_key": False}
        ],
        "type": "Entity"
    },
    "Criticality Assessment": {
        "color": "teal",
        "fields": [
            {"name": "Assessment_ID", "is_key": True},
            {"name": "System_ID", "is_foreign_key": True, "references": "System Overview"}
        ],
        "type": "Entity"
    },
    "Policy": {
        "color": "red",
        "fields": [
            {"name": "Policy_ID", "is_key": True}
        ],
        "type": "Entity"
    },
    "Policy Waivers": {
        "color": "red",
        "fields": [
            {"name": "Waiver_ID", "is_key": True},
            {"name": "Policy_ID", "is_foreign_key": True, "references": "Policy"}
        ],
        "type": "Entity"
    },
    "Supplier Profile": {
        "color": "purple",
        "fields": [
            {"name": "Supplier_ID", "is_key": True}
        ],
        "type": "Entity"
    },
    "Supplier Risk Management": {
        "color": "purple",
        "fields": [
            {"name": "Risk_ID", "is_key": True},
            {"name": "Supplier_ID", "is_foreign_key": True, "references": "Supplier Profile"}
        ],
        "type": "Entity"
    },
    "Supplier Contracts": {
        "color": "purple",
        "fields": [
            {"name": "Contract_ID", "is_key": True},
            {"name": "Supplier_ID", "is_foreign_key": True, "references": "Supplier Profile"}
        ],
        "type": "Entity"
    },
    "Actions Against Errant Supplier": {
        "color": "purple",
        "fields": [
            {"name": "Action_ID", "is_key": True},
            {"name": "Supplier_ID", "is_foreign_key": True, "references": "Supplier Profile"}
        ],
        "type": "Entity"
    },
    "Supplier Performance Feedback": {
        "color": "purple",
        "fields": [
            {"name": "Feedback_ID", "is_key": True},
            {"name": "Supplier_ID", "is_foreign_key": True, "references": "Supplier Profile"}
        ],
        "type": "Entity"
    },
    "Bulk Tender ECN Details": {
        "color": "purple",
        "fields": [
            {"name": "ECN_ID", "is_key": True},
            {"name": "Supplier_ID", "is_foreign_key": True, "references": "Supplier Profile"}
        ],
        "type": "Entity"
    },
    "EDH Agency": {
        "color": "purple",
        "fields": [
            {"name": "EDH_ID", "is_key": True}
        ],
        "type": "Entity"
    },
    "Risk Assessments": {
        "color": "orange",
        "fields": [
            {"name": "Assessment_ID", "is_key": True}
        ],
        "type": "Entity"
    },
    "Risk Treatments": {
        "color": "orange",
        "fields": [
            {"name": "Treatment_ID", "is_key": True},
            {"name": "Assessment_ID", "is_foreign_key": True, "references": "Risk Assessments"}
        ],
        "type": "Entity"
    },
    "Audit Findings": {
        "color": "gray",
        "fields": [
            {"name": "Finding_ID", "is_key": True}
        ],
        "type": "Entity"
    },
    "System Management": {
        "color": "green",
        "fields": [
            {"name": "Management_ID", "is_key": True},
            {"name": "System_ID", "is_foreign_key": True, "references": "System Overview"}
        ],
        "type": "Entity"
    },
    "Security & Sensitivity Classification": {
        "color": "green",
        "fields": [
            {"name": "Classification_ID", "is_key": True}
        ],
        "type": "Entity"
    },
    "Risk Materiality Level": {
        "color": "green",
        "fields": [
            {"name": "Materiality_ID", "is_key": True}
        ],
        "type": "Entity"
    },
    "System Resiliency": {
        "color": "green",
        "fields": [
            {"name": "Resiliency_ID", "is_key": True}
        ],
        "type": "Entity"
    },
    "Hosting and System Dependencies": {
        "color": "green",
        "fields": [
            {"name": "Dependency_ID", "is_key": True}
        ],
        "type": "Entity"
    },
    "Central Programmes": {
        "color": "green",
        "fields": [
            {"name": "Programme_ID", "is_key": True}
        ],
        "type": "Entity"
    }
}

# Define edges with labels for relationships
edges = [
    ("Agency", "System Overview", "relates to"),
    ("Agency", "Ministry Family", "manages"),
    ("System Overview", "Criticality Assessment", "supports"),
    ("System Overview", "Policy", "defines"),
    ("Policy", "Policy Waivers", "grants"),
    ("Supplier Profile", "Supplier Risk Management", "informs"),
    ("Supplier Profile", "Supplier Contracts", "oversees"),
    ("Supplier Profile", "Actions Against Errant Supplier", "initiates"),
    ("Supplier Profile", "Supplier Performance Feedback", "monitors"),
    ("Supplier Profile", "Bulk Tender ECN Details", "includes"),
    ("Supplier Profile", "EDH Agency", "collaborates with"),
    ("Risk Assessments", "Risk Treatments", "leads to"),
    ("Audit Findings", "Risk Treatments", "triggers"),
    ("Supplier Risk Management", "Risk Assessments", "feeds into"),
    ("Supplier Performance Feedback", "Supplier Risk Management", "affects"),
    ("Actions Against Errant Supplier", "Supplier Contracts", "cancels"),
    ("System Overview", "Supplier Contracts", "references"),
    ("System Overview", "Audit Findings", "monitors"),
    ("System Management", "System Overview", "manages"),
    ("System Management", "Criticality Assessment", "supports"),
    ("System Management", "Security & Sensitivity Classification", "evaluates"),
    ("System Management", "Risk Materiality Level", "determines"),
    ("System Management", "System Resiliency", "improves"),
    ("System Management", "Hosting and System Dependencies", "depends on"),
    ("System Management", "Central Programmes", "aligns with"),
    ("System Management", "Supplier Contracts", "depends on"),
    ("Supplier Contracts", "Hosting and System Dependencies", "depends on")
]

def create_node_table(node_name, entity_info):
    field_list = []
    for field in entity_info["fields"]:
        style = ""
        if field.get("is_key"):
            style = "font-weight: bold; text-decoration: underline;"
        elif field.get("is_foreign_key"):
            style = "font-style: italic; text-decoration: underline;"
        
        suffix = " (PK)" if field.get("is_key") else " (FK)" if field.get("is_foreign_key") else ""
        field_list.append(f'<li style="{style}">{field["name"]}{suffix}</li>')
    
    table_html = f"""
    <table border="1" style="background-color: {entity_info['color']}; border-collapse: collapse; width: 200px;">
        <tr>
            <th style="text-align: center; padding: 5px; border: 1px solid black; background-color: {entity_info['color']};">
                {node_name}
            </th>
        </tr>
        <tr>
            <td style="padding: 5px; border: 1px solid black;">
                <ul style="margin: 0; padding-left: 20px;">
                    {''.join(field_list)}
                </ul>
            </td>
        </tr>
    </table>
    """
    return html.escape(table_html)

# Create NetworkX graph
G = nx.DiGraph()
for node, info in entities.items():
    G.add_node(node, 
               title=create_node_table(node, info),
               color=info['color'],
               shape='box')

# Add edges to graph
for source, target, label in edges:
    G.add_edge(source, target, title=label, label=label)

# Create interactive PyVis network
net = Network(height="700px", width="100%", directed=True)
net.from_nx(G)
net.repulsion(node_distance=300, central_gravity=0.2)

# Customize nodes and edges
for node in net.nodes:
    node["shape"] = "box"
    node["font"] = {"size": 12}
    node["margin"] = 10

for edge in net.edges:
    edge["label"] = edge["title"]
    edge["font"] = {"size": 10}
    edge["arrows"] = "to"

# Save and display in Streamlit
net.save_graph("graph.html")
with open("graph.html", "r", encoding='utf-8') as f:
    components.html(f.read(), height=750, scrolling=True)

# Add legend
st.sidebar.title("Legend")
st.sidebar.markdown("""
    **Key:**
    - **Bold Underline** = Primary Key (PK)
    - *Italic Underline* = Foreign Key (FK)
""")
for entity, info in entities.items():
    st.sidebar.markdown(
        f'<div style="background-color:{info["color"]};width:20px;height:20px;display:inline-block"></div> '
        f'{entity} ({info["type"]})', 
        unsafe_allow_html=True
    )
