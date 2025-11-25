import re
from typing import List, Dict, Any

def analyze_cicd_file(file_content: str) -> List[Dict[str, Any]]:
    """
    Analyzes CI/CD configuration files (e.g., CircleCI, GitHub Actions)
    for common security best practices and misconfigurations.

    Args:
        file_content: The full content of the configuration file as a string.

    Returns:
        A list of findings. Each finding is a dictionary containing details about the detected issue.
    """
    findings = []
    lines = file_content.splitlines()

    for line_number, line in enumerate(lines, 1):
        # Rule: Avoid using `eval`
        if re.search(r'\beval\b', line):
            findings.append({
                "line_number": line_number,
                "rule_id": "CICD_AVOID_EVAL",
                "description": "The use of 'eval' is dangerous and can lead to command injection. Avoid it wherever possible.",
                "severity": "HIGH",
                "line_content": line.strip()
            })
            
    return findings

if __name__ == '__main__':
    # Example usage for testing the tool directly.
    
    test_circleci_content = """
version: 2.1
jobs:
  build:
    docker:
      - image: cimg/base:2023.01
    steps:
      - run:
          name: \"Run a risky command\"
          command: | 
            DANGEROUS_VAR=\"; ls -la\"
            echo \"Running eval...\"
            eval \"my_var=\\\"hello${DANGEROUS_VAR}\\\"\"
            echo $my_var
    """
    
    print("--- Analyzing Insecure CI/CD File ---")
    insecure_findings = analyze_cicd_file(test_circleci_content)
    if insecure_findings:
        for finding in insecure_findings:
            print(f"  - Line {finding.get('line_number', 'N/A')}: {finding['rule_id']} ({finding['severity']}) - {finding['description']} (Found: '{finding['line_content']}')")
    else:
        print("No issues found.")
