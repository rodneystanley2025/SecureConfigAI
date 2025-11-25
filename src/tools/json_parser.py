import json
import json_source_map
from typing import Dict, Any

def parse_json_content(file_content: str) -> Dict[str, Any]:
    """
    Parses the given string content as JSON, including a source map for line numbers.

    Args:
        file_content: The content of the JSON file as a string.

    Returns:
        A dictionary containing the parsed data and a source map,
        or an "error" key if parsing fails.
    """
    try:
        # The json_source_map.calculate function returns a source_map
        source_map = json_source_map.calculate(file_content)
        parsed_data = json.loads(file_content)
        
        if parsed_data is None:
            return {"message": "JSON file is empty or contains only null."}
            
        return {
            "data": parsed_data,
            "source_map": source_map
        }
    except Exception as e:
        return {"error": f"An unexpected error occurred during JSON parsing: {e}"}

if __name__ == '__main__':
    # Example usage for testing the tool directly.

    valid_json = """
    {
      "name": "My App",
      "version": "1.0.0",
      "settings": {
        "debug": true,
        "port": 8080,
        "credentials": {
            "user": "admin",
            "pass": "12345"
        }
      }
    }
    """

    invalid_json = """
    {
      "name": "My App"
      "version": "1.0.0"
    }
    """
    
    result_valid = parse_json_content(valid_json)
    if "error" not in result_valid:
        import json
        print("Data:", result_valid["data"])
        # The source_map object from json-source-map is not directly serializable
        # We can inspect it manually for demonstration.
        print("Source Map (sample):")
        print("  - Path '/settings/credentials/pass' starts at line:", result_valid["source_map"]["/settings/credentials/pass"].value_start.line + 1)

    print("\n--- Testing Invalid JSON ---")
    result_invalid = parse_json_content(invalid_json)
    print(result_invalid)
