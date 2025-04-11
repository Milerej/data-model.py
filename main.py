from pyvis.network import Network
 import networkx as nx
 import streamlit.components.v1 as components
 import html
 
 st.set_page_config(page_title="Interactive Interdependency Graph", layout="wide")
 
 st.title("🧠 Interactive Data Model Interdependency Chart")
 
 # Define entity modules with fields and relationships
 # Define entity modules and colors
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
     }
     "Ministry Family": "blue",
     "Agency": "blue",
     "System Overview": "teal",
     "Criticality Assessment": "teal",
     "Policy": "red",
     "Policy Waivers": "red",
     "Supplier Profile": "purple",
     "Supplier Risk Management": "purple",
     "Supplier Contracts": "purple",
     "Actions Against Errant Supplier": "purple",
     "Supplier Performance Feedback": "purple",
     "Bulk Tender ECN Details": "purple",
     "EDH Agency": "purple",
     "Risk Assessments": "orange",
     "Risk Treatments": "orange",
     "Audit Findings": "gray",
     # New nodes
     "System Management": "green",
     "Security & Sensitivity Classification": "green",
     "Risk Materiality Level": "green",
     "System Resiliency": "green",
     "Hosting and System Dependencies": "green",
     "Central Programmes": "green"
 }
 
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
     # New edges for System Management
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
 
 # Create NetworkX graph
 G = nx.DiGraph()
 for node, info in entities.items():
     G.add_node(node, 
                title=create_node_table(node, info),
                color=info['color'],
                shape='box')
 
 # Define edges based on foreign key relationships
 edges = []
 for entity_name, entity_info in entities.items():
     for field in entity_info['fields']:
         if field.get('is_foreign_key'):
             referenced_entity = field.get('references')
             if referenced_entity:
                 edges.append((
                     entity_name,
                     referenced_entity,
                     f"FK: {field['name']} → {referenced_entity}"
                 ))
 
 # Add edges to graph
 for node, color in entities.items():
     G.add_node(node, title=node, color=color)
 
 # Add edges with labels
 for source, target, label in edges:
     G.add_edge(source, target, title=label, label=label)
 
 # Create interactive PyVis network
 net = Network(height="700px", width="100%", directed=True)
 net.from_nx(G)
 net.repulsion(node_distance=300, central_gravity=0.2)
 net.repulsion(node_distance=200, central_gravity=0.3)
 
 # Customize edge labels
 for edge in net.edges:
     edge["label"] = edge["title"]
 
 # Save and display in Streamlit
 net.save_graph("graph.html")
 components.html(open("graph.html", "r", encoding='utf-8').read(), height=750, scrolling=True)
 
 import streamlit as st
 from pyvis.network import Network
 import networkx as nx
 import streamlit.components.v1 as components
 
 st.set_page_config(page_title="Interactive Interdependency Graph", layout="wide")
