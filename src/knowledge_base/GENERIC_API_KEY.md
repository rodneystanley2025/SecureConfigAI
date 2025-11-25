# Generic API Key

**ID:** `GENERIC_API_KEY`
**Severity:** CRITICAL

## Description

A generic API key was found in the configuration file. Hardcoding API keys is a major security risk. If this file is accidentally exposed or committed to a version control system, an attacker could use the API key to impersonate your application, steal data, or incur costs on your behalf.

## Remediation

API keys should never be hardcoded in configuration files. They should be loaded into the application at runtime from a secure source.

To remediate this issue, you should:

1.  **Immediately Rotate the Exposed Key:** Assume the exposed key has been compromised. In your service provider's dashboard, revoke the exposed API key and generate a new one.
2.  **Use a Secrets Management System:** The best practice is to store the API key in a dedicated secrets management system like AWS Secrets Manager, HashiCorp Vault, or your cloud provider's equivalent.
3.  **Use Environment Variables:** As an alternative, you can use environment variables to load the API key into your application. Ensure that these variables are set in a secure manner on your host environment and are not stored in plaintext files.
