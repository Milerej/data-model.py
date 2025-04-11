# Replace the existing net.set_options section with this:
net.set_options('''
{
    "physics": {
        "enabled": true,
        "stabilization": {
            "enabled": true,
            "iterations": 1000,
            "updateInterval": 100,
            "onlyDynamicEdges": false,
            "fit": true
        },
        "barnesHut": {
            "gravitationalConstant": -2000,
            "centralGravity": 0.3,
            "springLength": 200,
            "springConstant": 0.04,
            "damping": 0.09,
            "avoidOverlap": 0.1
        },
        "minVelocity": 0.1,
        "maxVelocity": 50
    },
    "edges": {
        "smooth": {
            "type": "continuous",
            "forceDirection": "none"
        }
    },
    "interaction": {
        "dragNodes": true,
        "dragView": true,
        "zoomView": true
    }
}
''')
