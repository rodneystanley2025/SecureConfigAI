# JWT Secret Found

**ID:** `JWT_SECRET_FOUND`
**Severity:** CRITICAL

## Description

A JWT (JSON Web Token) secret was found in the configuration file. Hardcoding JWT secrets is a major security risk. The JWT secret is used to sign and verify the authenticity of tokens. If an attacker gains access to this secret, they can forge valid tokens for any user, including administrators, and gain complete unauthorized access to your application.

## Remediation

JWT secrets should never be hardcoded in configuration files. They should be treated as highly sensitive secrets and loaded into the application at runtime from a secure source.

To remediate this issue, you should:

1.  **Immediately Rotate the Exposed Secret:** Assume the exposed secret has been compromised. Generate a new, strong, and long random string to use as the JWT secret. Deploying this new secret will invalidate all existing user sessions, which is a necessary security measure.
2.  **Use a Secrets Management System:** The best practice is to store the JWT secret in a dedicated secrets management system like AWS Secrets Manager, HashiCorp Vault, or your cloud provider's equivalent.
3.  **Use Environment Variables:** As an alternative, you can use environment variables to load the JWT secret into your application. Ensure that these variables are set in a secure manner on your host environment and are not stored in plaintext files.
4.  **Use Asymmetric Keys:** For higher security applications, consider using asymmetric key pairs (RS256/ES256) to sign and verify JWTs. The private key can be stored in a secure location (like a secrets manager), while the public key can be more widely distributed to services that need to verify tokens.
