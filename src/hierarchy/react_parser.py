import os
import re
from typing import List, Dict
from .base_parser import BaseParser

class ReactParser(BaseParser):
    """
    Parser for React projects to identify components and their parent-child relationships.
    """

    COMPONENT_REGEX = re.compile(r'class\s+(\w+)\s+extends\s+React\.Component|function\s+(\w+)\s*\(')
    IMPORT_REGEX = re.compile(r'import\s+(\w+)\s+from\s+["\'](.+)["\'];')

    def parse_file(self, file_path: str) -> Dict[str, List[str]]:
        """
        Parses a React file to identify component definitions and their child components.

        Args:
            file_path (str): Path to the React file.

        Returns:
            Dict[str, List[str]]: Dictionary with component names as keys and list of child components as values.
        """
        components = {}
        current_component = None
        imported_components = {}

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # First pass: Identify imports
            for line in lines:
                import_match = self.IMPORT_REGEX.match(line)
                if import_match:
                    component_name, import_path = import_match.groups()
                    imported_components[component_name] = import_path

            # Second pass: Identify components and their children
            for line in lines:
                component_match = self.COMPONENT_REGEX.search(line)
                if component_match:
                    class_component, func_component = component_match.groups()
                    component_name = class_component if class_component else func_component
                    current_component = component_name
                    components[current_component] = []
                elif current_component:
                    # Identify JSX tags representing child components
                    jsx_matches = re.findall(r'<(\w+)', line)
                    for tag in jsx_matches:
                        if tag in imported_components and tag != current_component:
                            components[current_component].append(tag)
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")

        return components

    def get_hierarchy(self, root_dir: str) -> Dict:
        """
        Builds a hierarchical dictionary representing React component relationships.

        Args:
            root_dir (str): Root directory of the React project.

        Returns:
            Dict: Nested dictionary representing component hierarchy.
        """
        hierarchy = {}
        component_dependencies = {}

        for dirpath, _, filenames in os.walk(root_dir):
            for file in filenames:
                if file.endswith('.jsx') or file.endswith('.js'):
                    file_path = os.path.join(dirpath, file)
                    components = self.parse_file(file_path)
                    for parent, children in components.items():
                        if parent not in component_dependencies:
                            component_dependencies[parent] = set()
                        component_dependencies[parent].update(children)

        # Build the hierarchy
        for parent, children in component_dependencies.items():
            if parent not in hierarchy:
                hierarchy[parent] = {}
            for child in children:
                hierarchy[parent][child] = {}

        return hierarchy
