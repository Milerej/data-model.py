# Define entity modules and colors
entities = {
    "System Management": {
        "color": "#2E7D32",  # Darker green for central node
        "size": 30, 
        "shape": "dot",
        "title": "Central node managing system relationships"
    },
    "System Overview": {
        "color": "#4CAF50",  # Standard green
        "size": 25, 
        "shape": "dot",
        "title": "\n".join([
            "Fields:",
            "• Agency",
            "• Ministry Family",
            "• System ID (Primary Key)",
            "• System Name",
            "• System Description",
            "• System Status"
        ])
    },
    "Criticality Assessment": {
        "color": "#4CAF50", 
        "size": 25, 
        "shape": "dot",
        "title": "\n".join([
            "Fields:",
            "• Economy",
            "• Public Health and Safety",
            "• National Security",
            "• Social Preparedness",
            "• Public Service",
            "• Designated CII under the Cybersecurity Act",
            "• System Criticality (System Auto-generated)"
        ])
    },
    "Security & Sensitivity Classification": {
        "color": "#4CAF50", 
        "size": 25, 
        "shape": "dot",
        "title": "Security and sensitivity classification details"
    },
    "Risk Materiality Level": {
        "color": "#4CAF50", 
        "size": 25, 
        "shape": "dot",
        "title": "Risk materiality assessment details"
    },
    "System Resiliency": {
        "color": "#4CAF50", 
        "size": 25, 
        "shape": "dot",
        "title": "System resiliency metrics and details"
    },
    "Hosting and System Dependencies": {
        "color": "#4CAF50", 
        "size": 25, 
        "shape": "dot",
        "title": "Hosting environment and system dependency information"
    },
    "Central Programmes": {
        "color": "#4CAF50", 
        "size": 25, 
        "shape": "dot",
        "title": "Central programmes information"
    }
}
