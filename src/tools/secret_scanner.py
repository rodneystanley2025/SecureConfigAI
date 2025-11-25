from .json_parser import parse_json_content
from .yaml_parser import parse_yaml_content
from .ini_parser import parse_ini_content # New import
from .trufflehog_scanner import scan_with_trufflehog # Import TruffleHog scanner
from typing import List, Dict, Any, Union
import re

# (Keep LINE_RULES, KEY_PATTERNS, and VALUE_PATTERNS the same)
LINE_RULES = [
    {
        "id": "DEBUG_MODE_ENABLED",
        "description": "Debug mode is enabled, which can expose sensitive information.",
        "severity": "HIGH",
        "pattern": r"debug\s*[:=]\s*true|debug\s*[:=]\s*1|debug_mode\s*[:=]\s*true|debug_mode\s*[:=]\s*1"
    },
    {
        "id": "WEAK_PASSWORD",
        "description": "A weak, default, or common password was found. Such passwords are often short, lack complexity, contain common words or personal information, follow predictable patterns, or are reused across multiple accounts, all of which drastically reduce their security and increase the risk of unauthorized access.",
        "severity": "MEDIUM",
        "pattern": r"password\s*[:=]\s*\b(?:123456|password|admin|qwerty|12345678|111111|password123|p@ssword)\b"
    },
    {
        "id": "AWS_ACCESS_KEY_ID_FOUND",
        "description": "An AWS Access Key ID was found in the file.",
        "severity": "CRITICAL",
        "pattern": r"AWS_ACCESS_KEY_ID\s*[:=]"
    },
    {
        "id": "AWS_SECRET_ACCESS_KEY_FOUND",
        "description": "An AWS Secret Access Key was found in the file.",
        "severity": "CRITICAL",
        "pattern": r"AWS_SECRET_ACCESS_KEY\s*[:=]"
    },
    {
        "id": "STRIPE_SECRET_KEY_FOUND",
        "description": "A Stripe Secret Key was found in the file.",
        "severity": "CRITICAL",
        "pattern": r"STRIPE_SECRET_KEY\s*[:=]"
    },
    {
        "id": "MAILGUN_API_KEY_FOUND",
        "description": "A Mailgun API Key was found in the file.",
        "severity": "CRITICAL",
        "pattern": r"MAILGUN_API_KEY\s*[:=]"
    },
    {
        "id": "JWT_SECRET_FOUND",
        "description": "A JWT Secret was found in the file.",
        "severity": "CRITICAL",
        "pattern": r"JWT_SECRET\s*[:=]"
    },
    {
        "id": "DB_PASSWORD_FOUND",
        "description": "A database password was found in the file.",
        "severity": "CRITICAL",
        "pattern": r"DB_PASSWORD\s*[:=]"
    },
    {
        "id": "ADMIN_PASSWORD_FOUND",
        "description": "An admin password was found in the file.",
        "severity": "CRITICAL",
        "pattern": r"ADMIN_PASSWORD\s*[:=]"
    }
]
KEY_PATTERNS = [
    re.compile(r'password', re.IGNORECASE),
    re.compile(r'passwd', re.IGNORECASE),
    re.compile(r'secret(key)?', re.IGNORECASE),
    re.compile(r'token', re.IGNORECASE),
    re.compile(r'api_key', re.IGNORECASE),
    re.compile(r'auth_key', re.IGNORECASE),
    re.compile(r'client_secret', re.IGNORECASE),
    re.compile(r'api_token', re.IGNORECASE),
    re.compile(r'private_key', re.IGNORECASE),
    re.compile(r'privatekey', re.IGNORECASE),
    re.compile(r'jwtsecret', re.IGNORECASE),
    re.compile(r'accesskey', re.IGNORECASE), # For AWS SecretAccessKey
]

VALUE_PATTERNS = {
    "WEAK_PASSWORD": re.compile(r'\b(123456|password|admin|root|qwerty|12345678|111111|password123|p@ssword)\b', re.IGNORECASE),
    "DOCKER_IMAGE_LATEST_TAG": re.compile(r":latest$"),
    "GENERIC_API_KEY": re.compile(r'sk_[a-zA-Z0-9]{24,}|dev_apikey_[a-zA-Z0-9]+', re.IGNORECASE),
    "PLACEHOLDER_SECRET": re.compile(r'your-secret-key-here|changeme|secret|development', re.IGNORECASE),
    "INSECURE_NODE_ENV": re.compile(r'\bdevelopment\b', re.IGNORECASE),
    "AWS_ACCESS_KEY_ID": re.compile(r'AKIA[0-9A-Z]{16}'),
    "AWS_SECRET_ACCESS_KEY": re.compile(r'^[0-9a-zA-Z\/+]{40}$'),
    "GOOGLE_SERVICE_ACCOUNT_KEY": re.compile(r"-----BEGIN PRIVATE KEY-----\n[a-zA-Z0-9\s+/=\n]+\n-----END PRIVATE KEY-----\n?"),
}

VALUE_PATTERNS_METADATA = {
    "WEAK_PASSWORD": {
        "description": "A weak, default, or common password was found. Such passwords are often short, lack complexity, contain common words or personal information, follow predictable patterns, or are reused across multiple accounts, all of which drastically reduce their security and increase the risk of unauthorized access.",
        "severity": "HIGH",
    },
    "DOCKER_IMAGE_LATEST_TAG": {
        "description": "Using the latest tag for Docker images introduces significant security risks and is not inherently vulnerable, but it creates an environment where vulnerabilities are more likely to be present and harder to manage. The latest tag is a moving target, meaning it can point to different image versions over time, potentially introducing unexpected updates, breaking changes, or newly discovered vulnerabilities without notice.",
        "severity": "HIGH",
    },
    "GENERIC_API_KEY": {
        "description": "A generic API key was found.",
        "severity": "CRITICAL",
    },
    "PLACEHOLDER_SECRET": {
        "description": "A placeholder or weak default secret was found.",
        "severity": "HIGH",
    },
    "INSECURE_NODE_ENV": {
        "description": "The application is configured to run in a development environment. In many frameworks, this mode disables crucial security protections, enables verbose error messages that leak internal application structure, and may enable other debugging endpoints.",
        "severity": "HIGH",
    },
    "AWS_ACCESS_KEY_ID": {
        "description": "An AWS Access Key ID was found.",
        "severity": "CRITICAL",
    },
    "AWS_SECRET_ACCESS_KEY": {
        "description": "An AWS Secret Access Key was found.",
        "severity": "CRITICAL",
    },
    "GOOGLE_SERVICE_ACCOUNT_KEY": {
        "description": "A Google Cloud Service Account Key was found.",
        "severity": "CRITICAL",
    },
}

# Specific INI rules (section.key)
INI_SPECIFIC_RULES = {
    r"[Database]\.Password": {
        "rule_id": "INI_DB_PASSWORD_HARDCODED",
        "description": "Hardcoded database password found.",
        "severity": "CRITICAL",
    },
    r"\bSecurity\b\.SecretKey": {
        "rule_id": "INI_SECURITY_SECRETKEY_HARDCODED",
        "description": "Hardcoded application secret key found.",
        "severity": "CRITICAL",
    },
    r"\bSecurity\b\.JWTSecret": {
        "rule_id": "INI_SECURITY_JWTSECRET_HARDCODED",
        "description": "Hardcoded JWT secret found.",
        "severity": "CRITICAL",
    },
    r"\bAPI\b\.APIKey": {
        "rule_id": "INI_API_KEY_HARDCODED",
        "description": "Hardcoded API key found.",
        "severity": "CRITICAL",
    },
    r"\bEmail\b\.Password": {
        "rule_id": "INI_EMAIL_PASSWORD_HARDCODED",
        "description": "Hardcoded email password found.",
        "severity": "CRITICAL",
    },
    r"\bCache\b\.Password": {
        "rule_id": "INI_CACHE_PASSWORD_HARDCODED",
        "description": "Hardcoded cache password found.",
        "severity": "CRITICAL",
    },
    r"\bExternalServices\.Stripe\b\.SecretKey": {
        "rule_id": "INI_STRIPE_SECRETKEY_HARDCODED",
        "description": "Hardcoded Stripe secret key found.",
        "severity": "CRITICAL",
    },
    r"\bExternalServices\.AWS\b\.SecretAccessKey": {
        "rule_id": "INI_AWS_SECRETACCESSKEY_HARDCODED",
        "description": "Hardcoded AWS Secret Access Key found.",
        "severity": "CRITICAL",
    },
    r"\bExternalServices\.AWS\b\.AccessKeyId": {
        "rule_id": "INI_AWS_ACCESSKEYID_HARDCODED",
        "description": "Hardcoded AWS Access Key ID found.",
        "severity": "CRITICAL",
    },
    r"\bExternalServices\.Azure\b\.ClientSecret": {
        "rule_id": "INI_AZURE_CLIENTSECRET_HARDCODED",
        "description": "Hardcoded Azure Client Secret found.",
        "severity": "CRITICAL",
    },
    r"\bExternalServices\.Google\b\.ServiceAccountKey": {
        "rule_id": "INI_GOOGLE_SERVICEACCOUNTKEY_HARDCODED",
        "description": "Hardcoded Google Cloud Service Account Key found.",
        "severity": "CRITICAL",
    },
}

def _get_line_content(lines: List[str], line_num: int) -> str:
    """Safely gets the content of a specific line."""
    if line_num and 0 < line_num <= len(lines):
        return lines[line_num - 1].strip()
    return "N/A"

def _get_line_from_map(source_map: Dict, path: str, parser_type: str, get_key_line: bool = False) -> Union[int, None]:
    """Gets the line number from the appropriate source map."""
    if parser_type == 'json':
        json_path = f"/{path.replace('.', '/')}"
        line_info = source_map.get(json_path)
        if line_info:
            if get_key_line:
                return line_info.key_start.line + 1 # 0-indexed
            return line_info.value_start.line + 1 # 0-indexed
    elif parser_type == 'yaml':
        return source_map.get(path)
    elif parser_type == 'ini':
        # INI source map stores "[Section].Key" -> line_num
        return source_map.get(path)

def _scan_structured_data_recursive(data: Any, source_map: Dict, lines: List[str], findings: List[Dict[str, Any]], parser_type: str, path: str = ""):
    """Recursively scans a dictionary or list for secrets, now with line number awareness."""
    if isinstance(data, dict):
        for key, value in data.items():
            current_path = f"{path}.{key}" if path else key
            
            # Apply INI specific rules if applicable
            ini_specific_rule_triggered = False
            if parser_type == 'ini':
                # For INI, the 'path' parameter is the section name (e.g., "Database", "ExternalServices.AWS")
                # and 'key' is the current key in that section.
                # ini_lookup_path needs to be "[Section].Key"
                ini_lookup_path_key = f"[{path}].{key.lower()}" if path else f"[{key}]" # section headers also have line numbers
                
                for pattern_str, rule_info in INI_SPECIFIC_RULES.items():
                    if re.match(pattern_str, ini_lookup_path_key, re.IGNORECASE):
                        line_num = _get_line_from_map(source_map, ini_lookup_path_key, parser_type)
                        findings.append({
                            "line_number": line_num,
                            "line_content": _get_line_content(lines, line_num),
                            "rule_id": rule_info["rule_id"],
                            "description": rule_info["description"],
                            "severity": rule_info["severity"],
                            "path": ini_lookup_path_key,
                        })
                        ini_specific_rule_triggered = True
                        break # Only report the most specific INI rule

            # Check keys for suspicious names (general rule), but only if no specific INI rule was triggered
            if not ini_specific_rule_triggered:
                for pattern in KEY_PATTERNS:
                    if pattern.search(key):
                        # If the value is a string and starts with ENCRYPTED|, skip this finding
                        if isinstance(value, str) and value.startswith("ENCRYPTED|"):
                            continue
                        
                        line_num = None
                        if parser_type == 'ini':
                            # Construct path for INI lookup map using the consistent format
                            ini_lookup_path = f"[{path}].{key.lower()}" if path else f"[{key}]"
                            line_num = _get_line_from_map(source_map, ini_lookup_path, parser_type, get_key_line=True)
                        else:
                            line_num = _get_line_from_map(source_map, current_path, parser_type, get_key_line=True)

                        findings.append({
                            "line_number": line_num,
                            "line_content": _get_line_content(lines, line_num),
                            "rule_id": "SUSPICIOUS_KEY_NAME",
                            "description": f"Key '{key}' may contain sensitive information.",
                            "severity": "MEDIUM",
                            "path": current_path,
                        })
                        break # Only report once for KEY_PATTERNS
            _scan_structured_data_recursive(value, source_map, lines, findings, parser_type, current_path)
            
    elif isinstance(data, list):
        for i, item in enumerate(data):
            current_path = f"{path}[{i}]"
            _scan_structured_data_recursive(item, source_map, lines, findings, parser_type, current_path)
            
    elif isinstance(data, str):
        # Apply VALUE_PATTERNS for string values
        line_num = None
        if parser_type == 'ini':
            # For INI, path is like "Section.Key"
            parts = path.rsplit('.', 1) # Split only on the last dot
            if len(parts) == 2:
                section_part = parts[0]
                key_part = parts[1]
                ini_lookup_path = f"[{section_part}].{key_part.lower()}"
                line_num = _get_line_from_map(source_map, ini_lookup_path, parser_type)
            elif len(parts) == 1 and path: # It might be a top-level section without a key, or an error
                 ini_lookup_path = f"[{path}]"
                 line_num = _get_line_from_map(source_map, ini_lookup_path, parser_type)
        else:
            line_num = _get_line_from_map(source_map, path, parser_type)

        # Extract the current key from the path for more precise rule application
        current_key = path.rsplit('.', 1)[-1] if '.' in path else path

        for rule_id, pattern in VALUE_PATTERNS.items():
            # Only check for weak passwords if the current_key contains "pass" or "secret"
            if rule_id == "WEAK_PASSWORD" and not ("pass" in current_key.lower() or "secret" in current_key.lower()):
                continue
            # Only check for insecure node env if the key is "NODE_ENV"
            if rule_id == "INSECURE_NODE_ENV" and "node_env" not in path.lower():
                continue
            
            match = pattern.search(data)

            if match:
                metadata = VALUE_PATTERNS_METADATA[rule_id]
                findings.append({
                    "line_number": line_num,
                    "line_content": _get_line_content(lines, line_num),
                    "rule_id": rule_id,
                    "description": metadata["description"],
                    "severity": metadata["severity"],
                    "path": path,
                })

def _scan_line_by_line(lines: List[str]) -> List[Dict[str, Any]]:
    """Fallback to line-by-line regex scanning."""
    findings = []
    for line_number, line in enumerate(lines, 1):
        for rule in LINE_RULES:
            if re.search(rule["pattern"], line, re.IGNORECASE):
                finding = {
                    "line_number": line_number,
                    "rule_id": rule["id"],
                    "description": rule["description"],
                    "severity": rule["severity"],
                    "line_content": line.strip()
                }
                findings.append(finding)
    return findings

def scan_for_secrets(file_content: str, file_path: str, selected_engines: Dict[str, bool]) -> List[Dict[str, Any]]:
    """
    Scans the given file content for secrets and misconfigurations using selected engines.
    """
    findings = []
    lines = file_content.splitlines()

    # Run custom structured and line-by-line scanners if enabled
    if selected_engines.get("customScanner", True): # Default to True if not specified
        json_result = parse_json_content(file_content)
        if "data" in json_result:
            _scan_structured_data_recursive(json_result["data"], json_result["source_map"], lines, findings, 'json')
        else:
            yaml_result = parse_yaml_content(file_content)
            if "data" in yaml_result:
                _scan_structured_data_recursive(yaml_result["data"], yaml_result["source_map"], lines, findings, 'yaml')
            else:
                ini_result = parse_ini_content(file_content)
                if "data" in ini_result:
                    _scan_structured_data_recursive(ini_result["data"], ini_result["source_map"], lines, findings, 'ini')
                else:
                    # Fallback to line-by-line scanning if no structured parsing is successful
                    fallback_findings = _scan_line_by_line(lines)
                    findings.extend(fallback_findings)

    # Run TruffleHog if enabled
    if selected_engines.get("truffleHog", False): # Default to False if not specified
        truffle_findings = scan_with_trufflehog(file_path)
        findings.extend(truffle_findings)

    return findings

if __name__ == '__main__':
    # Example usage for testing the tool directly.
    import tempfile
    import os
    
    test_json_content = """
{
  "vm": {
    "ip": "192.168.44.44",
    "memory": "1024",
    "synced_folders": [
      {
        "host_path": "data/",
        "guest_path": "/var/www",
        "type": "default"
      }
    ],
    "forwarded_ports": []
  },
  "vdd": {
    "sites": {
      "drupal8": {
        "account_name": "root",
        "account_pass": "root",
        "account_mail": "box@example.com",
        "site_name": "Drupal 8",
        "site_mail": "box@example.com",
        "vhost": {
          "document_root": "drupal8",
          "url": "drupal8.dev",
          "alias": ["www.drupal8.dev"]
        }
      },
      "drupal7": {
        "account_name": "root",
        "account_pass": "root",
        "account_mail": "box@example.com",
        "site_name": "Drupal 7",
        "site_mail": "box@example.com",
        "vhost": {
          "document_root": "drupal7",
          "url": "drupal7.dev",
          "alias": ["www.drupal7.dev"]
        }
      }
    }
  }
}
    """
    
    test_yaml_content = """
    server:
      port: 8080
    secrets:
      jwt_secret: "a-very-long-and-secret-string"
      db_password: "admin"
    """

    test_ini_content = """
[Database]
Host = localhost
Port = 5432
User = admin
Password = s3cr3tP@ss!

[Security]
EnableCSRF = True
SecretKey = your-secret-key-here-for-development
JWTSecret = another-dev-secret

[API]
APIKey = dev_apikey_12345

[Email]
Server = smtp.example.com
Port = 587
User = email_user
Password = email_pass123

[Cache]
Type = Redis
Host = localhost
Password = redis_pass

[ExternalServices.Stripe]
SecretKey = sk_live_xyz123abc456

[ExternalServices.AWS]
AccessKeyId = AKIAIOSFODNN7EXAMPLE
SecretAccessKey = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
"""

if __name__ == '__main__':
    # Example usage for testing the tool directly.
    
    test_json_content = """
{
  "vm": {
    "ip": "192.168.44.44",
    "memory": "1024",
    "synced_folders": [
      {
        "host_path": "data/",
        "guest_path": "/var/www",
        "type": "default"
      }
    ],
    "forwarded_ports": []
  },
  "vdd": {
    "sites": {
      "drupal8": {
        "account_name": "root",
        "account_pass": "root",
        "account_mail": "box@example.com",
        "site_name": "Drupal 8",
        "site_mail": "box@example.com",
        "vhost": {
          "document_root": "drupal8",
          "url": "drupal8.dev",
          "alias": ["www.drupal8.dev"]
        }
      },
      "drupal7": {
        "account_name": "root",
        "account_pass": "root",
        "account_mail": "box@example.com",
        "site_name": "Drupal 7",
        "site_mail": "box@example.com",
        "vhost": {
          "document_root": "drupal7",
          "url": "drupal7.dev",
          "alias": ["www.drupal7.dev"]
        }
      }
    }
  }
}
    """
    
    test_yaml_content = """
    server:
      port: 8080
    secrets:
      jwt_secret: "a-very-long-and-secret-string"
      db_password: "admin"
    """

    test_ini_content = """
[Database]
Host = localhost
Port = 5432
User = admin
Password = s3cr3tP@ss!

[Security]
EnableCSRF = True
SecretKey = your-secret-key-here-for-development
JWTSecret = another-dev-secret

[API]
APIKey = dev_apikey_12345

[Email]
Server = smtp.example.com
Port = 587
User = email_user
Password = email_pass123

[Cache]
Type = Redis
Host = localhost
Password = redis_pass

[ExternalServices.Stripe]
SecretKey = sk_live_xyz123abc456

[ExternalServices.AWS]
AccessKeyId = AKIAIOSFODNN7EXAMPLE
SecretAccessKey = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
"""

    # Default selected engines for testing directly
    default_selected_engines = {"truffleHog": True, "customScanner": True}

    print("--- Testing Structured Scan on JSON ---")
    # For testing, we don't have a real file_path, so use a dummy one
    json_findings = scan_for_secrets(test_json_content, "dummy_file.json", default_selected_engines)
    if json_findings:
        for issue in json_findings:
            print(f"  - Line {issue.get('line_number', 'N/A')}: {issue['rule_id']} ({issue['severity']}) - Path: {issue.get('path', 'N/A')}")
    else:
        print("No issues found.")

    print("\n--- Testing Structured Scan on YAML ---")
    yaml_findings = scan_for_secrets(test_yaml_content, "dummy_file.yaml", default_selected_engines)
    if yaml_findings:
        for issue in yaml_findings:
            print(f"  - Line {issue.get('line_number', 'N/A')}: {issue['rule_id']} ({issue['severity']}) - Path: {issue.get('path', 'N/A')}")
    else:
        print("No issues found.")
        
    print("\n--- Testing Structured Scan on INI ---")
    ini_findings = scan_for_secrets(test_ini_content, "dummy_file.ini", default_selected_engines)
    if ini_findings:
        for issue in ini_findings:
            print(f"  - Line {issue.get('line_number', 'N/A')}: {issue['rule_id']} ({issue['severity']}) - Path: {issue.get('path', 'N/A')}")
    else:
        print("No issues found.")