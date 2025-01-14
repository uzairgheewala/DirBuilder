import os
import json
import yaml
from typing import Optional, Dict, Any

def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Loads configuration from a YAML or JSON file. If no path is provided, returns default config.

    Args:
        config_path (str, optional): Path to the configuration file.

    Returns:
        Dict[str, Any]: Configuration dictionary.
    """
    default_config = {
        "exclude_extensions": [".pyc", ".pyo", ".pyd", ".git", ".svn", ".DS_Store"],
        "exclude_folders": ["__pycache__", ".git", ".svn", "node_modules", "venv", ".env", ".idea", ".vscode"],
        "output_formats": ["txt", "json"],
        "hierarchy": {
            "enable": False,
            "project_type": "verilog",  # Default project type
            "parser": "default"  # Placeholder for custom parsers
        }
    }

    if config_path:
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file '{config_path}' does not exist.")
        
        _, ext = os.path.splitext(config_path)
        try:
            with open(config_path, 'r') as f:
                if ext.lower() in ['.yaml', '.yml']:
                    user_config = yaml.safe_load(f)
                elif ext.lower() == '.json':
                    user_config = json.load(f)
                else:
                    raise ValueError("Unsupported configuration file format. Use YAML or JSON.")
        except Exception as e:
            raise ValueError(f"Error parsing configuration file: {e}")
        
        # Merge user_config into default_config
        merged_config = merge_configs(default_config, user_config)
        return merged_config

    return default_config

def merge_configs(default: Dict[str, Any], user: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recursively merges user configuration into the default configuration.

    Args:
        default (Dict[str, Any]): Default configuration.
        user (Dict[str, Any]): User-provided configuration.

    Returns:
        Dict[str, Any]: Merged configuration.
    """
    for key, value in user.items():
        if key in default and isinstance(default[key], dict) and isinstance(value, dict):
            default[key] = merge_configs(default[key], value)
        else:
            default[key] = value
    return default
