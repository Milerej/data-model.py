    # Modify the nodes dictionary to include initial collapsed state
    for node, attributes in entities.items():
        # Check if the node is a field (size 15)
        if attributes["size"] == 15:
            # Hide fields by default
            attributes["hidden"] = True

    # Create NetworkX graph with modified attributes
    G = nx.DiGraph()
    for node, attributes in entities.items():
        node_attrs = {
            "color": attributes["color"],
            "size": attributes["size"],
            "shape": attributes["shape"],
            "title": attributes["title"],
            "label": node,
            "hidden": attributes.get("hidden", False)  # Fields are hidden by default
        }
        G.add_node(node, **node_attrs)

    # Add edges with labels and custom arrow directions
    for source, target, label, direction in edges:
        G.add_edge(source, target, title=label, label=label, arrows=direction)

    # Create interactive PyVis network
    net = Network(height="900px", width="100%", directed=True, notebook=True)
    net.from_nx(G)

    # Modify the options to include click handling
    net.set_options("""
    {
        "physics": {
            "enabled": true,
            "stabilization": {
                "enabled": true,
                "iterations": 2000,
                "updateInterval": 25,
                "onlyDynamicEdges": false,
                "fit": true
            },
            "barnesHut": {
                "gravitationalConstant": -60000,
                "centralGravity": 0.1,
                "springLength": 1000,
                "springConstant": 0.08,
                "damping": 0.12,
                "avoidOverlap": 20
            },
            "minVelocity": 0.75,
            "maxVelocity": 30
        },
        "edges": {
            "smooth": {
                "type": "curvedCW",
                "roundness": 0.2,
                "forceDirection": "horizontal"
            },
            "length": 300,
            "font": {
                "size": 11,
                "strokeWidth": 2,
                "strokeColor": "#ffffff"
            },
            "color": {
                "inherit": false,
                "color": "#2E7D32",
                "opacity": 0.8
            },
            "width": 1.5,
            "hidden": false
        },
        "nodes": {
            "font": {
                "size": 12,
                "strokeWidth": 2,
                "strokeColor": "#ffffff"
            },
            "margin": 12,
            "scaling": {
                "min": 10,
                "max": 30
            },
            "fixed": {
                "x": false,
                "y": false
            }
        },
        "interaction": {
            "hover": true,
            "navigationButtons": true,
            "keyboard": true,
            "hideEdgesOnDrag": true
        },
        "layout": {
            "improvedLayout": true,
            "randomSeed": 42,
            "hierarchical": {
                "enabled": false,
                "nodeSpacing": 300,
                "levelSeparation": 300,
                "treeSpacing": 300
            }
        }
    }
    """)

    # Add click handling JavaScript
    click_js = """
    <script>
        function toggleConnectedNodes(nodeId) {
            var network = document.getElementsByClassName('vis-network')[0].__vis_network__;
            var connectedNodes = network.getConnectedNodes(nodeId);
            var allNodes = network.body.data.nodes.get();
            var updates = [];
            
            connectedNodes.forEach(function(connectedNode) {
                var node = allNodes.find(n => n.id === connectedNode);
                if (node && node.size === 15) {  // Only toggle field nodes (size 15)
                    updates.push({id: connectedNode, hidden: !node.hidden});
                }
            });
            
            network.body.data.nodes.update(updates);
        }

        document.getElementsByClassName('vis-network')[0].addEventListener('click', function(e) {
            var network = this.__vis_network__;
            var selection = network.getNodeAt(e.pointer.DOM);
            if (selection !== undefined) {
                toggleConnectedNodes(selection);
            }
        });
    </script>
    """

    # Modify the save and display section to include the click handling
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as tmp_file:
            net.save_graph(tmp_file.name)
            with open(tmp_file.name, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Add both fullscreen and click handling scripts
            modified_html = html_content.replace('</body>', f'{fullscreen_html}{click_js}</body>')
            
            components.html(modified_html, height=900)
            os.unlink(tmp_file.name)
    except Exception as e:
        st.error(f"An error occurred while generating the graph: {str(e)}")
