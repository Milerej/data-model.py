import networkx as nx
import matplotlib.pyplot as plt

# Create a directed graph
G = nx.DiGraph()

# Add nodes with color/type info
G.add_node("System A", type="System")
G.add_node("Supplier X", type="Supplier")
G.add_node("Risk 1", type="Risk")
G.add_node("Policy P1", type="Policy")

# Add relationships (edges)
G.add_edge("System A", "Supplier X")  # direct
G.add_edge("Supplier X", "Risk 1")    # indirect
G.add_edge("Policy P1", "Risk 1")     # logical

# Set colors based on type
color_map = {
    "System": "teal",
    "Supplier": "purple",
    "Risk": "orange",
    "Policy": "red"
}
node_colors = [color_map[G.nodes[n]['type']] for n in G.nodes]

# Draw
nx.draw(G, with_labels=True, node_color=node_colors, node_size=1500, font_size=10, arrows=True)
plt.title("System-Supplier-Risk Interdependency")
plt.show()
