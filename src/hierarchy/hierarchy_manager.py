from typing import Dict
from .parser_factory import ParserFactory

def build_project_hierarchy(root_dir: str, project_type: str) -> Dict:
    """
    Builds the project hierarchy using the appropriate parser.

    Args:
        root_dir (str): Root directory of the project.
        project_type (str): Type of the project (e.g., 'verilog', 'python').

    Returns:
        Dict: Hierarchical dictionary representing the project structure.
    """
    parser = ParserFactory.get_parser(project_type)
    if not parser:
        raise ValueError(f"No parser available for project type '{project_type}'.")
    
    hierarchy = parser.get_hierarchy(root_dir)
    return hierarchy
