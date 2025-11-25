# INI Database Password Hardcoded

**ID:** `INI_DB_PASSWORD_HARDCODED`
**Severity:** CRITICAL

## Description

A database password was found hardcoded in an INI configuration file. Hardcoding sensitive credentials directly in configuration files, especially for databases, is a severe security vulnerability. If this file is accessed by unauthorized individuals (e.g., through a code repository leak, misconfigured server, or local machine compromise), it grants direct access to your database, leading to potential data theft, corruption, or destruction.

## Remediation

Database passwords should never be hardcoded in INI or any other configuration files. They must be loaded securely at runtime.

To remediate this issue, you should:

1.  **Immediately Rotate the Exposed Password:** Assume the password has been compromised. Change the password for the affected database user(s) immediately.
2.  **Use a Secrets Management System:** The recommended best practice is to store database passwords in a dedicated secrets management system (e.g., HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, Google Secret Manager). Your application should retrieve these credentials securely at runtime.
3.  **Use Environment Variables:** As an alternative, load the database password from an environment variable. This ensures the password is not present in your codebase. Configure your deployment environment to set this variable securely.
4.  **Avoid Plaintext Storage:** Ensure no plaintext copies of the password exist in your version control system (even in history), local development environment, or deployment artifacts.
