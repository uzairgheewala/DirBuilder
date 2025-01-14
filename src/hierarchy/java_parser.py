import os
import re
from typing import List, Dict
from .base_parser import BaseParser

class JavaParser(BaseParser):
    """
    Parser for Java projects to identify classes, interfaces, and their inheritance hierarchies.
    """

    CLASS_REGEX = re.compile(r'class\s+(\w+)\s*(?:extends\s+(\w+))?\s*(?:implements\s+([\w, ]+))?{')
    INTERFACE_REGEX = re.compile(r'interface\s+(\w+)\s*(?:extends\s+([\w, ]+))?{')

    def parse_file(self, file_path: str) -> List[Dict[str, List[str]]]:
        """
        Parses a Java file to identify class and interface definitions and their relationships.

        Args:
            file_path (str): Path to the Java file.

        Returns:
            List[Dict[str, List[str]]]: List of dictionaries with 'name' and 'bases'.
        """
        entities = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            for match in self.CLASS_REGEX.finditer(content):
                class_name = match.group(1)
                extends = match.group(2)
                implements = match.group(3)
                bases = []
                if extends:
                    bases.append(extends)
                if implements:
                    bases.extend([impl.strip() for impl in implements.split(',')])
                entities.append({'name': class_name, 'bases': bases})

            for match in self.INTERFACE_REGEX.finditer(content):
                interface_name = match.group(1)
                extends = match.group(2)
                bases = []
                if extends:
                    bases.extend([ext.strip() for ext in extends.split(',')])
                entities.append({'name': interface_name, 'bases': bases})
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")

        return entities

    def get_hierarchy(self, root_dir: str) -> Dict:
        """
        Builds a hierarchical dictionary representing class and interface inheritance.

        Args:
            root_dir (str): Root directory of the Java project.

        Returns:
            Dict: Nested dictionary representing class and interface inheritance.
        """
        hierarchy = {}
        for dirpath, _, filenames in os.walk(root_dir):
            for file in filenames:
                if file.endswith('.java'):
                    file_path = os.path.join(dirpath, file)
                    entities = self.parse_file(file_path)
                    for entity in entities:
                        name = entity['name']
                        bases = entity['bases']
                        if not bases:
                            hierarchy[name] = {}
                        else:
                            for base in bases:
                                if base not in hierarchy:
                                    hierarchy[base] = {}
                                hierarchy[base][name] = {}
        return hierarchy