# INI Google Cloud Service Account Key Hardcoded

**ID:** `INI_GOOGLE_SERVICEACCOUNTKEY_HARDCODED`
**Severity:** CRITICAL

## Description

A Google Cloud Service Account Key was found hardcoded in an INI configuration file. Service account keys are highly sensitive credentials that grant programmatic access to your Google Cloud project and its resources. Hardcoding these keys is a severe security risk. If this file is exposed, an attacker could gain unauthorized access to your Google Cloud environment, potentially leading to data breaches, resource abuse, or significant financial implications.

## Remediation

Google Cloud Service Account Keys should never be hardcoded in INI or any other configuration files. They must be loaded securely at runtime.

To remediate this issue, you should:

1.  **Immediately Rotate the Exposed Key:** Assume the key has been compromised. In the Google Cloud Console, delete the exposed service account key and create a new one.
2.  **Use Workload Identity Federation:** The recommended best practice for applications running on Google Cloud is to use Workload Identity Federation. This allows your application to authenticate to Google Cloud services using short-lived credentials, eliminating the need for long-lived service account keys.
3.  **Use Google Secret Manager:** Store the service account key (if absolutely necessary to use one) in Google Secret Manager. Your application should retrieve this secret securely at runtime.
4.  **Use Environment Variables:** As an alternative for development or specific scenarios, load the path to the service account key file (or the content of the key file) from an environment variable. Ensure that this variable and the key file are secured on your host environment.
