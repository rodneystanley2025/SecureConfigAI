# INI Stripe Secret Key Hardcoded

**ID:** `INI_STRIPE_SECRETKEY_HARDCODED`
**Severity:** CRITICAL

## Description

A Stripe Secret Key was found hardcoded in an INI configuration file. Hardcoding payment gateway API keys is a severe security risk. If this file is exposed, an attacker could gain unauthorized access to your Stripe account, potentially leading to financial fraud, unauthorized charges, manipulation of customer data, or disruption of your payment processing.

## Remediation

Stripe Secret Keys should never be hardcoded in INI or any other configuration files. They must be loaded securely at runtime.

To remediate this issue, you should:

1.  **Immediately Rotate the Exposed Key:** Assume the key has been compromised. Log into your Stripe dashboard, revoke the exposed secret key, and generate a new one.
2.  **Use a Secrets Management System:** The recommended best practice is to store payment gateway API keys in a dedicated secrets management system (e.g., HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, Google Secret Manager). Your application should retrieve these credentials securely at runtime.
3.  **Use Environment Variables:** As an alternative, load the Stripe Secret Key from an environment variable. This ensures the key is not present in your codebase. Configure your deployment environment to set this variable securely.
4.  **Implement Least Privilege:** Ensure the Stripe API key only has the minimum necessary permissions required for the application's payment processing functions.
