# OWASP A05:2021 - Security Misconfiguration

## Description
Security misconfiguration is the most commonly seen issue. This typically results from insecure default configurations, incomplete or ad hoc configurations, open cloud storage, misconfigured HTTP headers, and verbose error messages containing sensitive information. It occurs at every level of an application stack, including the platform, web server, application server, database, framework, and custom code. Automated tools are fast at picking up misconfigurations, but human review is essential to find the gaps.

## Potential Impact
- **Data Exposure:** Sensitive data (e.g., database credentials, API keys) can be exposed if configurations are not properly secured.
- **Unauthorized Access:** Default credentials or overly permissive access controls can lead to unauthorized access to systems or data.
- **System Compromise:** Misconfigured security settings can create pathways for attackers to compromise the entire system.
- **Information Leakage:** Verbose error messages can reveal sensitive information about the application's internal workings.

## How it relates to Configuration Files
Configuration files are a primary source of security misconfigurations. Examples include:
- **Default Passwords:** Using default or weak passwords in `.env`, `application.properties`, or `settings.py`.
- **Debug Mode Enabled:** Leaving `DEBUG=True` or `APP_DEBUG=1` in production configurations, exposing stack traces and sensitive information.
- **Insecure Protocol Enforcement:** Not enforcing HTTPS or allowing insecure HTTP connections.
- **Overly Permissive File/Directory Permissions:** Configuring incorrect permissions for sensitive files or directories.
- **Unrestricted Access to Cloud Resources:** Misconfigured AWS S3 buckets, Azure Blobs, or Google Cloud Storage that are publicly accessible.
- **Outdated Components:** Not keeping track of and updating frameworks, libraries, and server software versions mentioned in configuration files.
- **Error Handling:** Configuration to display detailed error messages to users, which can reveal internal system information.

## Remediation Steps
- **Establish Secure Configuration Process:** Implement a repeatable hardening process for all environments (development, test, production).
- **Automate Configuration Management:** Use tools like Ansible, Puppet, Chef, or Docker/Kubernetes to manage configurations and ensure consistency.
- **Minimize Privileges:** Grant minimum necessary privileges on all systems and services.
- **Remove Unused Features:** Remove or securely configure unnecessary features, components, documentation, and samples.
- **Automate Security Scans:** Use static application security testing (SAST) tools to identify misconfigurations in code and configuration files.
- **Review Permissions:** Regularly review cloud storage and file system permissions.
- **Disable Debugging:** Ensure debug mode is disabled in all production environments.
- **Enforce HTTPS:** Configure applications and servers to strictly enforce HTTPS.
- **Implement Logging and Monitoring:** Ensure adequate logging and monitoring are in place to detect and alert on misconfigurations.

## Relevant Detections
- `DEBUG_MODE_ENABLED`
- `WEAK_PASSWORD`
- `PLACEHOLDER_SECRET`
- `INSECURE_NODE_ENV`
- Hardcoded credentials in `.env`, `.ini`, `.json`, `.yaml` files.
- Overly permissive IAM policies (if scanned via cloud config).