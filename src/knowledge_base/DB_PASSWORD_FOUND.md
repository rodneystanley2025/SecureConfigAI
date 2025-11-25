# Database Password Found

**ID:** `DB_PASSWORD_FOUND`
**Severity:** CRITICAL

## Description

A database password was found in the configuration file. Hardcoding database credentials is a major security risk. If this file is accidentally exposed or committed to a version control system, an attacker could gain direct access to your database, leading to data theft, modification, or destruction.

## Remediation

Database passwords should never be hardcoded in configuration files. They should be loaded into the application at runtime from a secure source.

To remediate this issue, you should:

1.  **Immediately Rotate the Exposed Password:** Assume the exposed password has been compromised. Change the password for the database user immediately.
2.  **Use a Secrets Management System:** The best practice is to store the database password in a dedicated secrets management system like AWS Secrets Manager, HashiCorp Vault, or your cloud provider's equivalent.
3.  **Use Environment Variables:** As an alternative, you can use environment variables to load the database password into your application. Ensure that these variables are set in a secure manner on your host environment and are not stored in plaintext files.
4.  **Use Database-Specific Authentication Methods:** Some databases offer more secure authentication methods, such as IAM database authentication (for AWS RDS) or managed identities (for Azure SQL). If your database supports it, consider using these methods to avoid long-lived passwords.
