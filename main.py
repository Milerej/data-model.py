import streamlit as st
from pyvis.network import Network
import networkx as nx
import streamlit.components.v1 as components
import html

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
    }
    # Add other entities similarly...
}

def create_node_table(node_name, entity_info):
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
                    {''.join(
                        f'<li style="{"text-decoration: underline;" if field.get("is_key") or field.get("is_foreign_key") else ""}'
                        f'{"font-weight: bold;" if field.get("is_key") else ""}'
                        f'{"font-style: italic;" if field.get("is_foreign_key") else ""}">'
                        f'{field["name"]}'
                        f
