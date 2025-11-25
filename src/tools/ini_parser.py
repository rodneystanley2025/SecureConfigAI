from configparser import ConfigParser
from io import StringIO
from typing import Dict, Any, List, Tuple

def parse_ini_content(file_content: str) -> Dict[str, Any]:
    """
    Parses the given string content as an INI file, including a source map for line numbers.

    Args:
        file_content: The content of the INI file as a string.

    Returns:
        A dictionary containing the parsed data and a source map,
        or an "error" key if parsing fails.
    """
    
    # Manually track line numbers for sections and keys
    line_map: Dict[str, int] = {}
    current_section: str = ""
    lines = file_content.splitlines()

    for i, line in enumerate(lines):
        stripped_line = line.strip()
        if stripped_line.startswith('[') and stripped_line.endswith(']'):
            current_section = stripped_line[1:-1]
            line_map[f"[{current_section}]"] = i + 1
        elif '=' in stripped_line and current_section:
            key = stripped_line.split('=', 1)[0].strip()
            line_map[f"[{current_section}].{key.lower()}"] = i + 1

    config = ConfigParser()
    try:
        # ConfigParser expects a file-like object
        config.read_string(file_content)

        parsed_data: Dict[str, Any] = {}
        for section in config.sections():
            parsed_data[section] = {}
            for key, value in config.items(section):
                parsed_data[section][key] = value
        
        return {
            "data": parsed_data,
            "source_map": line_map
        }
    except Exception as e:
        return {"error": f"An unexpected error occurred during INI parsing: {e}"}

if __name__ == '__main__':
    # Example usage for testing the tool directly.

    valid_ini = """
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

[Logging]
Level = INFO
Path = /var/log/myapp/app.log
"""

    invalid_ini = """
[Section without closing bracket
Key = Value
"""
    
    print("--- Testing Valid INI ---")
    result_valid = parse_ini_content(valid_ini)
    if "error" not in result_valid:
        import json
        print("Data:", json.dumps(result_valid["data"], indent=2))
        print("Source Map:", json.dumps(result_valid["source_map"], indent=2))
    else:
        print(result_valid)

    print("\n--- Testing Invalid INI ---")
    result_invalid = parse_ini_content(invalid_ini)
    print(result_invalid)
