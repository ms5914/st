def match_contacts(prospects, contacts):
    """
    Match contacts to prospects based on domain and preferred personas.
    Handles wildcards (*) in department or seniority.
    """

    def extract_domain(email):
        """Extract domain from email address."""
        return email.split('@')[1]

    def matches_persona(contact, persona):
        """
        Check if a contact matches a persona pattern.
        Persona format: "department.seniority"
        Supports wildcards: "*.vp" or "c-suite.*"
        """
        persona_parts = persona.split('.')
        if len(persona_parts) != 2:
            return False

        persona_dept, persona_seniority = persona_parts
        contact_dept = contact.get('department', '')
        contact_seniority = contact.get('seniority', '')

        dept_match = (persona_dept == '*' or persona_dept == contact_dept)
        seniority_match = (persona_seniority == '*' or persona_seniority == contact_seniority)

        return dept_match and seniority_match

    # Process each prospect
    for prospect in prospects:
        domain = prospect['domain']
        personas = prospect.get('personas', [])

        # Find all contacts matching this domain
        domain_contacts = [c for c in contacts if extract_domain(c['email']) == domain]

        # If no personas specified, output all matching contacts
        if not personas:
            emails = [c['email'] for c in domain_contacts]
            print(f"{domain}: {', '.join(emails)}")
            continue

        # Match contacts to personas in order, avoiding duplicates
        matched_contacts = []
        seen_emails = set()

        for persona in personas:
            for contact in domain_contacts:
                email = contact['email']
                if email not in seen_emails and matches_persona(contact, persona):
                    # Format the actual persona (not the pattern)
                    actual_persona = f"{contact['department']}.{contact['seniority']}"
                    matched_contacts.append((email, actual_persona))
                    seen_emails.add(email)

        # Format and print output
        if matched_contacts:
            output_parts = [f"{email} ({persona})" for email, persona in matched_contacts]
            print(f"{domain}: {', '.join(output_parts)}")
        else:
            print(f"{domain}: ")


# Example test cases
print("Test Case 1: Basic matching")
prospects1 = [
    {"domain": "startup.com"},
    {"domain": "enterprise.com"}
]
contacts1 = [
    {"email": "zara@startup.com", "department": "c-suite", "seniority": "ceo"},
    {"email": "mariana@startup.com", "department": "c-suite", "seniority": "founder"},
    {"email": "bob@enterprise.com", "department": "HR", "seniority": "vp"},
]
match_contacts(prospects1, contacts1)

print("\nTest Case 2: With personas")
prospects2 = [
    {"domain": "startup.com", "personas": ["c-suite.founder", "c-suite.ceo"]},
    {"domain": "enterprise.com", "personas": ["finance.vp"]}
]
contacts2 = [
    {"email": "zara@startup.com", "department": "c-suite", "seniority": "ceo"},
    {"email": "mariana@startup.com", "department": "c-suite", "seniority": "founder"},
    {"email": "bob@enterprise.com", "department": "HR", "seniority": "vp"},
    {"email": "alice@startup.com", "department": "c-suite", "seniority": "cto"},
    {"email": "christoph@enterprise.com", "department": "finance", "seniority": "vp"}
]
match_contacts(prospects2, contacts2)

print("\nTest Case 3: With wildcards")
prospects3 = [
    {"domain": "startup.com", "personas": ["c-suite.founder", "c-suite.*"]},
    {"domain": "enterprise.com", "personas": ["finance.vp", "*.vp"]}
]
contacts3 = [
    {"email": "zara@startup.com", "department": "c-suite", "seniority": "ceo"},
    {"email": "mariana@startup.com", "department": "c-suite", "seniority": "founder"},
    {"email": "bob@enterprise.com", "department": "HR", "seniority": "vp"},
    {"email": "alice@startup.com", "department": "c-suite", "seniority": "cto"},
    {"email": "christoph@enterprise.com", "department": "finance", "seniority": "vp"}
]
match_contacts(prospects3, contacts3)