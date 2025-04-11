import streamlit as st
from pyvis.network import Network
import networkx as nx
import streamlit.components.v1 as components
import tempfile
import os

st.set_page_config(page_title="Interactive Interdependency Graph", layout="wide")

st.title("🧠 Interactive System Management Data Model")

# Define custom CSS for tooltips
custom_css = """
<style>
.tooltip-table {
    border-collapse: collapse;
    width: 100%;
    background-color: white;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.tooltip-table td {
    padding: 8px;
    border: 1px solid #ddd;
}
.tooltip-table .field-name {
    font-weight: bold;
    background-color: #f5f5f5;
}
</style>
"""

# Define tooltip content for each node
tooltip_info = {
    "System Overview": """
    <table class='tooltip-table'>
        <tr><td class='field-name'>Agency</td><td>MOF</td></tr>
        <tr><td class='field-name'>Ministry Family</td><td>Ministry of Finance</td></tr>
        <tr><td class='field-name'>System ID</td><td><b>SYS_001</b></td></tr>
        <tr><td class='field-name'>System Name</td><td>System Overview Module</td></tr>
        <tr><td class='field-name'>System Description</td><td>Core module for system information management</td></tr>
        <tr><td class='field-name'>System Status</td><td>Active</td></tr>
    </table>
    """,
    "System Management": """
    <table class='tooltip-table'>
        <tr><td class='field-name'>Agency</td><td>MOF</td></tr>
        <tr><td class='field-name'>Ministry Family</td><td>Ministry of Finance</td></tr>
        <tr><td class='field-name'>System ID</td><td><b>SYS_002</b></td></tr>
        <tr><td class='field-name'>System Name</td><td>System Management Console</td></tr>
        <tr><td class='field-name'>System Description</td><td>Central management interface</td></tr>
        <tr><td class='field-name'>System Status</td><td>Active</td></tr>
    </table>
    """,
    "Criticality Assessment": """
    <table class='tooltip-table'>
        <tr><td class='field-name'>Agency</td><td>MOF</td></tr>
        <tr><td class='field-name'>Ministry Family</td><td>Ministry of Finance</td></tr>
        <tr><td class='field-name'>System ID</td><td><b>SYS_003</b></td></tr>
        <tr><td class='field-name'>System Name</td><td>Criticality Assessment Module</td></tr>
        <tr><td class='field-name'>System Description</td><td>System criticality evaluation tool</td></tr>
        <tr><td class='field-name'>System Status</td><td>Active</td></tr>
    </table>
    """,
    "Security & Sensitivity Classification": """
    <table class='tooltip-table'>
        <tr><td class='field-name'>Agency</td><td>MOF</td></tr>
        <tr><td class='field-name'>Ministry Family</td><td>Ministry of Finance</td></tr>
        <tr><td class='field-name'>System ID</td><td><b>SYS_004</b></td></tr>
        <tr><td class='field-name'>System Name</td><td>Security Classification Module</td></tr>
        <tr><td class='field-name'>System Description</td><td>Security level management system</td></tr>
        <tr><td class='field-name'>System Status</td><td>Active</td></tr>
    </table>
    """,
    "Risk Materiality Level": """
    <table class='tooltip-table'>
        <tr><td class='field-name'>Agency</td><td>MOF</td></tr>
        <tr><td class='field-name'>Ministry Family</td><td>Ministry of Finance</td></tr>
        <tr><td class='field-name'>System ID</td><td><b>SYS_005</b></td></tr>
        <tr><td class='field-name'>System Name</td><td>Risk Assessment Module</td></tr>
        <tr><td class='field-name'>System Description</td><td>Risk evaluation and tracking system</td></tr>
        <tr><td class='field-name'>System Status</td><td>Active</td></tr>
    </table>
    """,
    "System Resiliency": """
    <table class='tooltip-table'>
        <tr><td class='field-name'>Agency</td><td>MOF</td></tr>
        <tr><td class='field-name'>Ministry Family</td><td>Ministry of Finance</td></tr>
        <tr><td class='field-name'>System ID</td><td><b>SYS_006</b></td></tr>
        <tr><td class='field-name'>System Name</td><td>Resiliency Management Module</td></tr>
        <tr><td class='field-name'>System Description</td><td>System resilience monitoring tool</td></tr>
        <tr><td class='field-name'>System Status</td><td>Active</td></tr>
    </table>
    """,
    "Hosting and System Dependencies": """
    <table class='tooltip-table'>
        <tr><td class='field-name'>Agency</td><td>MOF</td></tr>
        <tr><td class='field-name'>Ministry Family</td><td>Ministry of Finance</td></tr>
        <tr><td class='field-name'>System ID</td><td><b>SYS_007</b></td></tr>
        <tr><td class='field-name'>System Name</td><td>Dependencies Management Module</td></tr>
        <tr><td class='field-name'>System Description</td><td>System dependencies tracking tool</td></tr>
        <tr><td class='field-name'>System Status</td><td>Active</td></tr>
    </table>
    """,
    "Central Programmes": """
    <table class='tooltip-table'>
        <tr><td class='field-name'>Agency</td><td>MOF</td></tr>
        <tr><td class='field-name'>Ministry Family</td><td>Ministry of Finance</td></tr>
        <tr><td class='field-name'>System ID</td><td><b>SYS_008</b></td></tr>
        <tr><td class='field-name'>System Name</td><td>Central Programs Module</td></tr>
        <tr><td class='field-name'>System Description</td><td>Program management system</td></tr>
        <tr><td class='field-name'>System Status</td><td>Active</td></tr>
    </table>
    """
}

# Define entity modules and colors
entities = {
    "System Management": {"color": "green", "size": 30},
    "System Overview": {"color": "green", "size": 20},
    "Criticality Assessment": {"color": "green", "size": 20},
    "Security & Sensitivity Classification": {"color": "green", "size": 20},
    "Risk Materiality Level": {"color": "green", "size": 20},
    "System Resiliency": {"color": "green", "size": 20},
    "Hosting and System Dependencies": {"color": "green", "size": 20},
    "Central Programmes": {"color": "green", "size": 20}
}

# Define edges with PK/FK relationships
edges = [
    ("System Management", "System Overview", "PK: System_ID", "both"),
    ("System Management", "Criticality Assessment", "PK: System_ID", "both"),
    ("System Management", "Security & Sensitivity Classification", "PK: System_ID", "both"),
    ("System Management", "Risk Materiality Level", "PK: System_ID", "both"),
    ("System Management", "System Resiliency
