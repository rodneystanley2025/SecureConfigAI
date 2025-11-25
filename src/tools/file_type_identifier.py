import os
import re
from typing import Optional

def identify_file_type(filename: str, file_content: str) -> str:
    """
    Identifies the type of configuration file based on its filename and content.

    Args:
        filename: The name of the file, including its extension.
        file_content: The full content of the file as a string.

    Returns:
        A string representing the identified file type (e.g., "dotenv", "dockerfile", "yaml", "json", "unknown").
    """
    name_lower = filename.lower()
    
    # Check by filename/extension first
    if name_lower == ".env" or name_lower.endswith(".env"):
        return "dotenv"
    if name_lower == "dockerfile" or name_lower.endswith(".dockerfile"):
        return "dockerfile"
    if name_lower.endswith((".yaml", ".yml")):
        return "yaml"
    if name_lower.endswith(".json"):
        # Differentiate between generic JSON and package.json
        if name_lower == "package.json":
            return "package_json"
        return "json"
    if name_lower.endswith(".toml"):
        return "toml"
    if name_lower.endswith(".ini") or name_lower.endswith(".conf"):
        return "ini_conf"
    
    # Check by content if extension is ambiguous or generic
    content_lower = file_content.lower()
    
    # Dockerfile content check (if filename is generic like 'config')
    if re.search(r"^\s*FROM\s+", file_content, re.MULTILINE | re.IGNORECASE) and \
       re.search(r"^\s*(RUN|COPY|ADD)\s+", file_content, re.MULTILINE | re.IGNORECASE):
        return "dockerfile"
    
    # YAML content check (simple heuristic)
    if re.search(r"^\s*\w+:\s", file_content, re.MULTILINE) and not re.search(r"^\s*\[.*\]", file_content, re.MULTILINE):
        return "yaml"
        
    # JSON content check (simple heuristic)
    if file_content.strip().startswith("{") and file_content.strip().endswith("}"):
        return "json"

    # Default to unknown if no specific type is identified
    return "unknown"

if __name__ == '__main__':
    # Example usage for testing the tool directly.
    
    # Test cases
    test_cases = [
        ("my_app.env", "DEBUG=true\nAPI_KEY=123"),
        ("Dockerfile", "FROM alpine\nRUN echo hello"),
        ("docker-compose.yml", "version: '3.8'\nservices:\n  web:"),
        ("config.yaml", "database:\n  host: localhost"),
        ("settings.json", '{"debug": true, "port": 8080}'),
        ("package.json", '{"name": "my-app", "version": "1.0.0"}'),
        ("config", "FROM ubuntu\nRUN apt-get update"), # Dockerfile by content
        ("config", "server:\n  port: 8080"), # YAML by content
        ("config", '{"user": "admin"}'), # JSON by content
        ("README.md", "# My Project"), # Unknown
        ("config.toml", "title = \"TOML Example\""),
        ("my.ini", "[database]\nuser=root"),
    ]

    for filename, content in test_cases:
        file_type = identify_file_type(filename, content)
        print(f"File: '{filename}' (Content snippet: '{content.splitlines()[0]}...') -> Type: {file_type}")
