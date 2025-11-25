# INI Email Password Hardcoded

**ID:** `INI_EMAIL_PASSWORD_HARDCODED`
**Severity:** CRITICAL

## Description

An email account password was found hardcoded in an INI configuration file. Hardcoding email credentials is a severe security risk. If this file is exposed, an attacker could gain unauthorized access to the email account, potentially leading to:
*   Sending spam or phishing emails from your domain.
*   Accessing sensitive communications.
*   Resetting other accounts associated with that email.

## Remediation

Email account passwords should never be hardcoded in INI or any other configuration files. They must be loaded securely at runtime.

To remediate this issue, you should:

1.  **Immediately Rotate the Exposed Password:** Assume the password has been compromised. Change the password for the affected email account(s) immediately.
2.  **Use a Secrets Management System:** The recommended best practice is to store email passwords in a dedicated secrets management system (e.g., HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, Google Secret Manager). Your application should retrieve these credentials securely at runtime.
3.  **Use Environment Variables:** As an alternative, load the email password from an environment variable. This ensures the password is not present in your codebase. Configure your deployment environment to set this variable securely.
4.  **Use API Keys for Email Services:** If using a third-party email service (e.g., SendGrid, Mailgun), prefer using API keys over direct email passwords, and manage these API keys securely.
