# main.py

import networkx as nx
import matplotlib.pyplot as plt

def build_interdependency_chart():
    # Define entities and their module color
    entities = {
        "Ministry": "blue",
        "Family": "blue",
        "Agency": "blue",
        "System Overview": "teal",
        "Criticality Assessment": "teal",
        "Policy": "red",
        "Policy Waivers": "red",
        "Industry Waiver": "red",
        "Supplier Profile": "purple",
        "Supplier Risk Management": "purple",
        "Supplier Contracts": "purple",
        "Actions Against Errant Supplier": "purple",
        "Supplier Performance Feedback": "purple",
        "Bulk Tender ECN Details": "purple",
        "EDH Agency": "purple",
        "Risk Assessments": "orange",
        "Risk Treatments": "orange",
        "Audit Findings": "gray"
    }

    # Define relationships (edges)
    edges = [
        ("Agency", "System Overview"),
        ("System Overview", "Criticality Assessment"),
        ("Policy", "Policy Waivers"),
        ("Policy", "Industry Waiver"),
        ("Supplier Profile", "Supplier Risk Management"),
        ("Supplier Profile", "Supplier Contracts"),
        ("Supplier Profile", "Actions Against Errant Supplier"),
        ("Supplier Profile", "Supplier Performance Feedback"),
        ("Supplier Profile", "Bulk Tender ECN Details"),
        ("Supplier Profile", "EDH Agency"),
        ("Risk Assessments", "Risk Treatments"),
        ("Audit Findings", "Risk Treatments"),
        ("Supplier Risk Management", "Risk Assessments"),
        ("Supplier Performance Feedback", "Supplier Risk Management"),
        ("Actions Against Errant Supplier", "Supplier Contracts"),
        ("System Overview", "Supplier Contracts")
    ]

    # Create the graph
    G = nx.DiGraph()
    for entity, color in entities.items():
        G.add_node(entity, color=color)

    G.add_edges_from(edges)

    node_colors = [G.nodes[n]["color"] for n in G.nodes]

    # Draw
    plt.figure(figsize=(16, 10))
    pos = nx.spring_layout(G, k=0.6, iterations=50, seed=42)
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=2000,
            font_size=10, edge_color='black', arrows=True)
    plt.title("Data Model Interdependency Chart", fontsize=16)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    build_interdependency_chart()
