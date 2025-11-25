from ruamel.yaml import YAML
from typing import Dict, Any, Tuple

def _build_line_map_recursive(data: Any, source_map: Dict[str, int], path: str = ""):
    """Recursively builds a map of `value_path` to `line_number`."""
    if isinstance(data, dict):
        for key, value in data.items():
            new_path = f"{path}.{key}" if path else key
            # ruamel.yaml gives line numbers for keys
            source_map[new_path] = data.lc.data.get(key, (None, None))[0] or data.lc.line
            _build_line_map_recursive(value, source_map, new_path)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            new_path = f"{path}[{i}]"
            # Line number for list items is usually inherited from the parent
            source_map[new_path] = data.lc.data[i][0] if data.lc.data and i < len(data.lc.data) and data.lc.data[i] else data.lc.line
            _build_line_map_recursive(item, source_map, new_path)

def parse_yaml_content(file_content: str) -> Dict[str, Any]:
    """
    Parses the given string content as YAML, including a source map for line numbers.

    Args:
        file_content: The content of the YAML file as a string.

    Returns:
        A dictionary containing the parsed data and a source map,
        or an "error" key if parsing fails.
    """
    try:
        yaml = YAML()
        parsed_data = yaml.load(file_content)
        if parsed_data is None:
            return {"message": "YAML file is empty or contains only comments."}
        
        if not isinstance(parsed_data, (dict, list)):
            return {"error": "YAML content is not a dictionary or a list, which is required for structured scanning."}
        
        source_map = {}
        _build_line_map_recursive(parsed_data, source_map)
        
        return {
            "data": parsed_data,
            "source_map": source_map
        }
        
    except Exception as e:
        return {"error": f"An unexpected error occurred during YAML parsing: {e}"}

if __name__ == '__main__':
    # Example usage for testing the tool directly.

    valid_yaml = """
    name: My App
    version: 1.0.0
    settings:
      debug: true
      port: 8080
      credentials:
        - user: admin
        - pass: "12345"
    """

    invalid_yaml = """
    name: My App
      version: 1.0.0
    """
    
    print("--- Testing Valid YAML ---")
    result_valid = parse_yaml_content(valid_yaml)
    if "error" not in result_valid:
        import json
        print("Data:", result_valid["data"])
        print("Source Map:", json.dumps(result_valid["source_map"], indent=2))

    print("\n--- Testing Invalid YAML ---")
    result_invalid = parse_yaml_content(invalid_yaml)
    print(result_invalid)
