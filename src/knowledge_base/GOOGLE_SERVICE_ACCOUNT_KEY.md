# Google Cloud Service Account Key

**ID:** `GOOGLE_SERVICE_ACCOUNT_KEY`
**Severity:** CRITICAL

## Description

A Google Cloud Service Account Key was found in the configuration file. Hardcoding service account keys is a major security risk. If this file is accidentally exposed or committed to a version control system, an attacker could gain access to your Google Cloud project and the resources it has access to.

## Remediation

Google Cloud Service Account Keys should never be hardcoded in configuration files. They should be loaded into the application at runtime from a secure source.

To remediate this issue, you should:

1.  **Immediately Rotate the Exposed Key:** Assume the exposed key has been compromised. In the Google Cloud Console, delete the exposed service account key and create a new one.
2.  **Use Workload Identity Federation:** The best practice for applications running on Google Cloud is to use Workload Identity Federation to grant permissions to your resources. This eliminates the need for long-lived service account keys.
3.  **Use a Secrets Management System:** If you cannot use Workload Identity Federation, store the service account key in a dedicated secrets management system like Google Secret Manager, HashiCorp Vault, or your cloud provider's equivalent.
4.  **Use Environment Variables:** As a last resort, you can use an environment variable to store the path to the service account key file, or the content of the file itself. Ensure that the environment variable and the key file are secured on your host environment.
