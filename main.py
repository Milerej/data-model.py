with col2:
    st.header("Sub-modules and Fields (List View)")
    
    # Create a new NetworkX graph for the list view
    G_list = nx.DiGraph()
    
    # Add main module
    G_list.add_node("System Management", **{
        "color": "#2E7D32",
        "size": 35,
        "shape": "dot",
        "title": "System Management Module",
        "label": "System Management"
    })
    
    # Add sub-modules
    sub_modules = {
        "System Overview": [],
        "Criticality Assessment": [],
        "Security & Sensitivity Classification": [],
        "Risk Materiality Level": [],
        "System Resiliency": [],
        "Hosting and System Dependencies": []
    }
    
    # Add sub-modules to graph and collect fields
    for sub_module in sub_modules.keys():
        G_list.add_node(sub_module, **{
            "color": "#4CAF50",
            "size": 25,
            "shape": "dot",
            "title": entities[sub_module]["title"],
            "label": sub_module
        })
        G_list.add_edge("System Management", sub_module)
        
        # Collect fields for each sub-module
        fields_html = ""
        for source, target, label, _ in edges:
            if source == sub_module and label == "contains":
                fields_html += f"• {target}<br>"
                sub_modules[sub_module].append(target)
        
        if fields_html:
            # Add fields as HTML in the node title
            G_list.nodes[sub_module]["title"] = f"<h3>{sub_module}</h3><p>{fields_html}</p>"

    # Create interactive PyVis network for list view
    net_list = Network(height="700px", width="100%", directed=True, notebook=True)
    net_list.from_nx(G_list)
    
    # Set options for the list view
    net_list.set_options('{' + '''
        "physics": {
            "enabled": true,
            "stabilization": {
                "enabled": true,
                "iterations": 1000,
                "updateInterval": 25
            },
            "hierarchicalRepulsion": {
                "centralGravity": 0.0,
                "springLength": 200,
                "springConstant": 0.01,
                "nodeDistance": 250,
                "damping": 0.09
            }
        },
        "edges": {
            "smooth": {
                "type": "continuous",
                "forceDirection": "none"
            },
            "color": {
                "inherit": false,
                "color": "#2E7D32",
                "opacity": 0.8
            },
            "width": 1.5
        },
        "nodes": {
            "font": {
                "size": 16,
                "strokeWidth": 2,
                "strokeColor": "#ffffff"
            },
            "scaling": {
                "min": 20,
                "max": 35
            }
        },
        "layout": {
            "hierarchical": {
                "enabled": true,
                "direction": "UD",
                "sortMethod": "directed",
                "nodeSpacing": 200,
                "levelSeparation": 200
            }
        },
        "interaction": {
            "hover": true,
            "tooltipDelay": 0
        }
    ''' + '}')

    # Create a temporary directory and save the list view graph
    with tempfile.TemporaryDirectory() as temp_dir:
        path = os.path.join(temp_dir, "graph_list.html")
        net_list.save_graph(path)
        
        with open(path, "r", encoding="utf-8") as f:
            html_content_list = f.read()
        
        components.html(html_content_list, height=750, scrolling=True)
