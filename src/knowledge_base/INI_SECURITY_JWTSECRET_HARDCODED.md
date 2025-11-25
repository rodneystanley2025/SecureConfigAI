# INI JWT Secret Hardcoded

**ID:** `INI_SECURITY_JWTSECRET_HARDCODED`
**Severity:** CRITICAL

## Description

A JWT (JSON Web Token) secret was found hardcoded in an INI configuration file. This secret is used to sign and verify the authenticity of JSON Web Tokens. If an attacker gains access to this secret, they can forge valid tokens for any user, including administrators, and gain complete unauthorized access to your application. Hardcoding this secret makes it a critical vulnerability.

## Remediation

JWT secrets should never be hardcoded in INI or any other configuration files. They must be treated as highly sensitive secrets and loaded securely at runtime.

To remediate this issue, you should:

1.  **Immediately Rotate the Exposed Secret:** Assume the secret has been compromised. Generate a new, strong, and long random string to use as the JWT secret. Deploying this new secret will invalidate all existing user sessions, which is a necessary security measure.
2.  **Use a Secrets Management System:** The recommended best practice is to store the JWT secret in a dedicated secrets management system (e.g., HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, Google Secret Manager). Your application should retrieve this secret securely at runtime.
3.  **Use Environment Variables:** As an alternative, load the JWT secret from an environment variable. This ensures the secret is not present in your codebase. Configure your deployment environment to set this variable securely.
4.  **Use Asymmetric Keys:** For higher security applications, consider using asymmetric key pairs (RS256/ES256) to sign and verify JWTs. The private key can be stored in a secure location (like a secrets manager), while the public key can be more widely distributed to services that need to verify tokens.
