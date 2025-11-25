import subprocess
import json
import os
from typing import List, Dict, Any

def scan_with_gitleaks(file_path: str) -> List[Dict[str, Any]]:
    """
    Scans a file using Gitleaks and returns findings in a standardized format.
    """
    findings = []
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return findings

    try:
        # Run Gitleaks as a subprocess
        # Using --report-format json for structured output
        # Using --no-git to scan plain files, not just git repos
        command = ["gitleaks", "detect", "--source", file_path, "--report-format", "json", "--no-git"]
        
        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False # Do not raise an exception for non-zero exit codes (Gitleaks exits with 1 if secrets are found)
        )

        if process.stdout:
            try:
                gitleaks_findings = json.loads(process.stdout)
                for gitleaks_finding in gitleaks_findings:
                    # Convert Gitleaks' finding to our standardized format
                    # Example of Gitleaks finding:
                    # {"Description":"AWS Access Key","StartLine":1,"EndLine":1,"StartColumn":1,"EndColumn":20,"Match":"AKIA...","Secret":"AKIA...", "File":"path/to/file", ...}
                    
                    description = gitleaks_finding.get("Description", "Gitleaks finding")
                    
                    # Gitleaks provides severity, but let's use a default if not present or map it
                    severity = "HIGH" # Default to HIGH for Gitleaks findings

                    findings.append({
                        "line_number": gitleaks_finding.get("StartLine"),
                        "line_content": gitleaks_finding.get("Secret"), # Gitleaks "Secret" is the matched secret
                        "rule_id": gitleaks_finding.get("RuleID", "GITLEAKS_SECRET_FOUND"),
                        "description": description,
                        "severity": severity,
                        "path": file_path, # Gitleaks reports filename, but our 'path' is more general
                        "gitleaks_data": gitleaks_finding # Keep original data for richer analysis later
                    })
            except json.JSONDecodeError:
                print(f"Warning: Could not decode JSON from Gitleaks output: {process.stdout}")
        
        if process.stderr:
            print(f"Gitleaks Stderr: {process.stderr}")

    except FileNotFoundError:
        print(f"Gitleaks command not found. Please ensure Gitleaks is installed and in your PATH.")
    except Exception as e:
        print(f"An error occurred while running Gitleaks: {e}")

    return findings

if __name__ == '__main__':
    # Example usage for testing the tool directly.
    dummy_file_content_gitleaks = """
    This is a test file with an AWS key.
    aws_access_key_id = AKIAIOSFODNN7EXAMPLE
    Another secret: shh_this_is_a_secret_key
    """
    test_file_path = "test_gitleaks_file.txt"
    with open(test_file_path, "w") as f:
        f.write(dummy_file_content_gitleaks)

    print("--- Testing Gitleaks Scanner ---")
    gitleaks_findings = scan_with_gitleaks(test_file_path)
    if gitleaks_findings:
        for issue in gitleaks_findings:
            print(f"  - Line {issue.get('line_number', 'N/A')}: {issue['rule_id']} ({issue['severity']}) - Path: {issue.get('path', 'N/A')} - Content: {issue.get('line_content', 'N/A')}")
    else:
        print("No issues found by Gitleaks.")
    
    if os.path.exists(test_file_path):
        os.remove(test_file_path)
