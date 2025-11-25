# INI Azure Client Secret Hardcoded

**ID:** `INI_AZURE_CLIENTSECRET_HARDCODED`
**Severity:** CRITICAL

## Description

An Azure Client Secret was found hardcoded in an INI configuration file. Azure Client Secrets are credentials used by applications to authenticate themselves to Azure Active Directory (Azure AD) and gain access to Azure resources. Hardcoding these secrets is a severe security risk. If this file is exposed, an attacker could impersonate your application, gain unauthorized access to your Azure subscription, and potentially compromise your cloud resources and data.

## Remediation

Azure Client Secrets should never be hardcoded in INI or any other configuration files. They must be loaded securely at runtime.

To remediate this issue, you should:

1.  **Immediately Rotate the Exposed Secret:** Assume the secret has been compromised. In the Azure portal, generate a new client secret for the affected application registration and ensure the old one is revoked or expired.
2.  **Use Azure Key Vault:** The recommended best practice is to store Azure Client Secrets (and other sensitive credentials) in Azure Key Vault. Your application should retrieve these secrets securely at runtime using Managed Identities, which eliminates the need to manage secrets in your code.
3.  **Use Managed Identities:** For applications deployed within Azure (e.g., Azure App Service, Azure VMs), use Managed Identities for Azure resources. This allows your application to authenticate to Azure AD and access Key Vault (or other Azure services) without any hardcoded credentials.
4.  **Use Environment Variables:** As an alternative for non-Azure deployed applications or development, load the client secret from an environment variable. Ensure that this variable is set in a secure manner on your host environment and is not stored in plaintext files.
