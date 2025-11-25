import subprocess
import json
import os
from typing import List, Dict, Any

def scan_with_trufflehog(file_path: str) -> List[Dict[str, Any]]:
    """
    Scans a file using TruffleHog and returns findings in a standardized format.
    """
    findings = []
    
    # Ensure the file exists before scanning
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return findings

    try:
        # Run TruffleHog as a subprocess
        # Using --json for structured output
        # The path is a positional argument for 'filesystem' subcommand
        command = ["trufflehog", "filesystem", file_path, "--json"]
        
        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False # Do not raise an exception for non-zero exit codes (TruffleHog exits with 1 if secrets are found)
        )

        # TruffleHog typically prints findings to stdout as JSON lines
        # Each line is a separate JSON object
        for line in process.stdout.splitlines():
            if line.strip(): # Ensure line is not empty
                try:
                    truffle_finding = json.loads(line)
                    # Convert TruffleHog's finding to our standardized format
                    # TruffleHog output structure varies, so we need to be careful
                    # Example of TruffleHog finding:
                    # {"SourceID": "...", "SourceMetadata": {...}, "DetectorID": "...", "DetectorName": "...", "DecoderName": "...", "Verified": false, "Raw": "...", "Redacted": "...", "ExtraData": null, "StructuredData": null, "Type": "...", "EngineID": "...", "RuleID": "...", "Tags": [...], "Remediation": "...", "Branch": "...", "Commit": "...", "Email": "...", "Timestamp": "...", "DetectedAt": "...", "Properties": {...}, "Filename": "...", "Line": 123, "LineHash": "...", "CommitHash": "...", "CommitMessage": "...", "SecretsFound": [...]}

                    # A simplified conversion, focusing on key information
                    line_number = truffle_finding.get("DetectedAt", {}).get("line")
                    # Trufflehog's "Redacted" field often contains the actual secret, possibly with context
                    line_content = truffle_finding.get("Redacted") or truffle_finding.get("Raw")
                    
                    description = truffle_finding.get("ExtraData", {}).get("reason") or truffle_finding.get("DetectorName", "TruffleHog finding")
                    
                    # TruffleHog doesn't directly provide a severity, so we can default or infer
                    # For now, let's set a default severity for TruffleHog findings.
                    severity = "HIGH" # Default severity for anything TruffleHog finds

                    findings.append({
                        "line_number": line_number,
                        "line_content": line_content, 
                        "rule_id": truffle_finding.get("DetectorID", "TRUFFLEHOG_SECRET_FOUND"),
                        "description": description,
                        "severity": severity,
                        "path": file_path, # TruffleHog reports filename, but our 'path' is more general
                        "trufflehog_data": truffle_finding # Keep original data for richer analysis later
                    })
                except json.JSONDecodeError:
                    # TruffleHog might print non-JSON output in case of errors or warnings
                    print(f"Warning: Could not decode JSON from TruffleHog output: {line}")
        
        if process.stderr:
            print(f"TruffleHog Stderr: {process.stderr}")

    except FileNotFoundError:
        print(f"TruffleHog command not found. Please ensure TruffleHog is installed and in your PATH.")
    except Exception as e:
        print(f"An error occurred while running TruffleHog: {e}")

    return findings

if __name__ == '__main__':
    # Example usage for testing the tool directly.
    
    # Create a dummy file for testing
    dummy_file_content_truffle = """
    This is a test file with a dummy secret.
    AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
    some_secret_key=shh_its_a_secret
    password=root
    """
    test_file_path = "test_truffle_hog_file.txt"
    with open(test_file_path, "w") as f:
        f.write(dummy_file_content_truffle)

    print("--- Testing TruffleHog Scanner ---")
    truffle_findings = scan_with_trufflehog(test_file_path)
    if truffle_findings:
        for issue in truffle_findings:
            print(f"  - Line {issue.get('line_number', 'N/A')}: {issue['rule_id']} ({issue['severity']}) - Path: {issue.get('path', 'N/A')} - Content: {issue.get('line_content', 'N/A')}")
    else:
        print("No issues found by TruffleHog.")
    
    # Clean up the dummy file
    if os.path.exists(test_file_path):
        os.remove(test_file_path)
