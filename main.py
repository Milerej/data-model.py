# Define edges with labels for relationships - organized by domain
edges = [
    # Ministry and Agency relationships
    ("Agency", "Ministry Family", 
     "FK: Agency.Ministry_ID -> Ministry_Family.Ministry_ID"),
    
    # System Overview relationships
    ("System Overview", "Agency", 
     "FK: System_Overview.Agency_ID -> Agency.Agency_ID"),
    ("Criticality Assessment", "System Overview", 
     "FK: Criticality_Assessment.System_ID -> System_Overview.System_ID"),
    
    # Policy relationships
    ("Policy Waivers", "Policy", 
     "FK: Policy_Waivers.Policy_ID -> Policy.Policy_ID"),
    
    # Supplier relationships
    ("Supplier Risk Management", "Supplier Profile", 
     "FK: Supplier_Risk_Management.Supplier_ID -> Supplier_Profile.Supplier_ID"),
    ("Supplier Contracts", "Supplier Profile", 
     "FK: Supplier_Contracts.Supplier_ID -> Supplier_Profile.Supplier_ID"),
    ("Actions Against Errant Supplier", "Supplier Profile", 
     "FK: Actions_Against_Errant_Supplier.Supplier_ID -> Supplier_Profile.Supplier_ID"),
    ("Supplier Performance Feedback", "Supplier Profile", 
     "FK: Supplier_Performance_Feedback.Supplier_ID -> Supplier_Profile.Supplier_ID"),
    ("Bulk Tender ECN Details", "Supplier Profile", 
     "FK: Bulk_Tender_ECN_Details.Supplier_ID -> Supplier_Profile.Supplier_ID"),
    
    # Risk Management relationships
    ("Risk Treatments", "Risk Assessments", 
     "FK: Risk_Treatments.Assessment_ID -> Risk_Assessments.Assessment_ID"),
    
    # System Management relationships
    ("System Management", "System Overview", 
     "FK: System_Management.System_ID -> System_Overview.System_ID"),
    ("Security & Sensitivity Classification", "System Overview", 
     "FK: Security_Classification.System_ID -> System_Overview.System_ID"),
    ("Risk Materiality Level", "System Overview", 
     "FK: Risk_Materiality.System_ID -> System_Overview.System_ID"),
    ("System Resiliency", "System Overview", 
     "FK: System_Resiliency.System_ID -> System_Overview.System_ID"),
    ("Hosting and System Dependencies", "System Overview", 
     "FK: Hosting_Dependencies.System_ID -> System_Overview.System_ID"),
    ("Central Programmes", "System Overview", 
     "FK: Central_Programmes.System_ID -> System_Overview.System_ID"),
    
    # Cross-domain relationships
    ("Supplier Contracts", "System Overview", 
     "FK: Supplier_Contracts.System_ID -> System_Overview.System_ID"),
    ("Audit Findings", "System Overview", 
     "FK: Audit_Findings.System_ID -> System_Overview.System_ID")
]
