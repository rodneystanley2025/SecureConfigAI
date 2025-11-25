import os
import json
from typing import Dict, Any, List
import google.generativeai as genai

# Import our custom tools
from src.tools.file_type_identifier import identify_file_type
from src.tools.secret_scanner import scan_for_secrets
from src.tools.yaml_parser import parse_yaml_content
from src.tools.json_parser import parse_json_content
from src.tools.cicd_analyzer import analyze_cicd_file
from src.tools.gitleaks_scanner import scan_with_gitleaks # Import Gitleaks scanner

# --- Orchestrator ---
def run_scan(file_path: str, selected_engines: Dict[str, bool]) -> Dict[str, Any]:
    """
    Orchestrates a scan of a single file, including AI analysis.

    Args:
        file_path: The full path to the file to be scanned.

    Returns:
        A dictionary containing the results from the various tools and the AI analysis.
    """
    # 1. Fail fast if API key is not set
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set. Please set your API key in the .env file.")
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro-latest')
    except Exception as e:
        raise RuntimeError(f"Error configuring Gemini API: {e}")

    if not os.path.exists(file_path):
        return {"error": f"File not found at {file_path}"}

    with open(file_path, 'r', encoding='utf-8') as f:
        file_content = f.read()
    
    filename = os.path.basename(file_path)
    
    # 2. Identify the file type
    file_type = identify_file_type(filename, file_content)
    
    # 3. Run tools based on file type
    tool_findings = []
    
    # Run custom secret scanner if enabled (which includes our regex-based and TruffleHog)
    # The decision to run TruffleHog is now inside scan_for_secrets based on selected_engines
    secret_findings = scan_for_secrets(file_content, file_path, selected_engines)
    if secret_findings:
        tool_findings.extend(secret_findings)
    
    # Run Gitleaks if enabled
    if selected_engines.get("gitleaks", False):
        gitleaks_findings = scan_with_gitleaks(file_path)
        if gitleaks_findings:
            tool_findings.extend(gitleaks_findings)
        
    # Run type-specific tools
    if file_type == 'yaml':
        yaml_results = parse_yaml_content(file_content)
        if "error" in yaml_results:
            tool_findings.append({
                "rule_id": "INVALID_YAML",
                "description": f"The file could not be parsed as YAML. Error: {yaml_results['error']}",
                "severity": "HIGH",
                "line_number": None,
                "line_content": None
            })
        
        cicd_findings = analyze_cicd_file(file_content)
        if cicd_findings:
            tool_findings.extend(cicd_findings)
    elif file_type in ['json', 'package_json']: # New logic for JSON
        json_results = parse_json_content(file_content)
        if "error" in json_results:
            tool_findings.append({
                "rule_id": "INVALID_JSON",
                "description": f"The file could not be parsed as JSON. Error: {json_results['error']}",
                "severity": "HIGH",
                "line_number": None,
                "line_content": None
            })

    
    # 4. Get AI Analysis
    ai_analysis = get_ai_analysis(model, file_content, tool_findings, file_type)
    print(f"DEBUG: AI Analysis generated: {ai_analysis[:200]}...") # Print first 200 chars

    # 5. Compile final results
    scan_results = {
        "file_info": {
            "filename": filename,
            "identified_type": file_type
        },
        "tool_findings": tool_findings,
        "ai_analysis": ai_analysis
    }
    
    return {"scan_results": scan_results, "identified_type": file_type}

def get_ai_analysis(model, file_content: str, tool_findings: List[Dict[str, Any]], file_type: str) -> str:
    """
    Analyzes the file content and tool findings using a generative AI model.

    Args:
        model: The generative AI model instance.
        file_content: The full content of the file.
        tool_findings: A list of findings from other tools.
        file_type: The identified type of the file.

    Returns:
        A string containing the AI's analysis and recommendations.
    """
    prompt = f"""
    You are an expert security analyst specializing in configuration file reviews. Your task is to analyze the provided file content and any identified security findings.

    **Security Scan Analysis**

    **File Type:** {file_type}

    **File Content (first 1000 characters for context, if relevant):**
    ```
    {file_content[:1000]}
    ```

    **Detailed Tool Findings:**
    {json.dumps(tool_findings, indent=2)}

    **Instructions for Analysis:**
    1.  **Overall Security Posture:** Provide a concise summary of the file's purpose and its general security posture (e.g., Excellent, Good, Moderate, Poor, Critical).
    2.  **Detailed Findings & Risks:** For each `tool_finding` provided, describe the specific security risk. Explain *why* it is a vulnerability, referencing common security principles (e.g., OWASP Top 10, CWE) where applicable. Even if tool findings are empty, analyze the `file_content` for potential misconfigurations or sensitive data.
    3.  **Actionable Remediation:** For each identified risk, provide clear, concise, and actionable steps to remediate the vulnerability. Suggest best practices and alternatives (e.g., using environment variables, secrets management, principle of least privilege).
    4.  **No Tool Findings - AI Review:** If `tool_findings` is empty, perform a general security review of the `file_content` based on common configuration security best practices for the identified `file_type`.
    5.  **Format:** Structure your response in well-formatted Markdown, using headings, bullet points, and code blocks for readability. Prioritize critical and high-severity issues.
    """

    try:
        response = model.generate_content(prompt)
        print(f"DEBUG: Raw AI response text: {response.text[:200]}...") # Print first 200 chars
        return response.text
    except Exception as e:
        return f"An error occurred during AI analysis: {e}"