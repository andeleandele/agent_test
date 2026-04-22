Open Questions & TODOs

    This project intentionally contains some ambiguous aspects and open requirements, which may require clarification or extension:

    Authentication
        TODO: Add authentication to all user endpoints.  
        The method of authentication is not specified (e.g., OAuth2, JWT, API key, session).  
        Further discussion is needed to decide the appropriate authentication mechanism.

    User Deletion Semantics
        TODO: Should deleted users be removed from the database (hard delete) or just marked as inactive (soft delete)?  
        Currently, users are completely removed. There's a plan to potentially add an is_active field for deactivation.

    Email Validation
        TODO: Should email addresses be validated to ensure they end with @company.com?  
        The rule is not enforced. Clarify validation requirements as necessary.

    Additional User Fields
        TODO: Add more user fields (e.g., phone number) and specify their validation rules.