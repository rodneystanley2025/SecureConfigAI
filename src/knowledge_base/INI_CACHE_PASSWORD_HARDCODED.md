# INI Cache Password Hardcoded

**ID:** `INI_CACHE_PASSWORD_HARDCODED`
**Severity:** CRITICAL

## Description

A cache password (e.g., for Redis, Memcached) was found hardcoded in an INI configuration file. Caching systems often store sensitive data (e.g., session tokens, user data). Hardcoding cache credentials is a security risk. If this file is exposed, an attacker could gain unauthorized access to your caching system, potentially leading to:
*   Accessing or manipulating cached sensitive data.
*   Session hijacking.
*   Denial of Service (DoS) by flushing the cache.

## Remediation

Cache passwords should never be hardcoded in INI or any other configuration files. They must be loaded securely at runtime.

To remediate this issue, you should:

1.  **Immediately Rotate the Exposed Password:** Assume the password has been compromised. Change the password for the affected cache instance(s) immediately.
2.  **Use a Secrets Management System:** The recommended best practice is to store cache passwords in a dedicated secrets management system (e.g., HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, Google Secret Manager). Your application should retrieve these credentials securely at runtime.
3.  **Use Environment Variables:** As an alternative, load the cache password from an environment variable. This ensures the password is not present in your codebase. Configure your deployment environment to set this variable securely.
4.  **Secure Cache Access:** Ensure cache instances are not publicly exposed and are only accessible from trusted application servers.
