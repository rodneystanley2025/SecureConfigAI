# INI API Key Hardcoded

**ID:** `INI_API_KEY_HARDCODED`
**Severity:** CRITICAL

## Description

An API key was found hardcoded in an INI configuration file. API keys are credentials used to access various services (e.g., third-party APIs, internal microservices). Hardcoding API keys is a severe security risk. If this file is exposed, an attacker could gain unauthorized access to the services associated with that key, potentially leading to data breaches, service abuse, or financial implications.

## Remediation

API keys should never be hardcoded in INI or any other configuration files. They must be loaded securely at runtime.

To remediate this issue, you should:

1.  **Immediately Rotate the Exposed Key:** Assume the key has been compromised. In the respective service provider's dashboard or internal system, revoke the exposed API key and generate a new one.
2.  **Use a Secrets Management System:** The recommended best practice is to store API keys in a dedicated secrets management system (e.g., HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, Google Secret Manager). Your application should retrieve these credentials securely at runtime.
3.  **Use Environment Variables:** As an alternative, load the API key from an environment variable. This ensures the key is not present in your codebase. Configure your deployment environment to set this variable securely.
4.  **Implement Least Privilege:** Ensure the API key only has the minimum necessary permissions required for the application to function.
