# src/hierarchy/python_parser.py

import ast
import os
from typing import List, Dict
from .base_parser import BaseParser

class PythonParser(BaseParser):
    """
    Parser for Python projects to identify classes and their inheritance hierarchies.
    """

    def parse_file(self, file_path: str) -> List[str]:
        """
        Parses a Python file to identify class definitions and their base classes.

        Args:
            file_path (str): Path to the Python file.

        Returns:
            List[str]: List of tuples (ClassName, [BaseClasses]).
        """
        class_hierarchy = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                node = ast.parse(f.read(), filename=file_path)
            
            for class_def in [n for n in node.body if isinstance(n, ast.ClassDef)]:
                base_classes = [base.id if isinstance(base, ast.Name) else
                                base.attr if isinstance(base, ast.Attribute) else
                                'Unknown' for base in class_def.bases]
                class_hierarchy.append((class_def.name, base_classes))
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
        
        return class_hierarchy

    def get_hierarchy(self, root_dir: str) -> Dict:
        """
        Builds a hierarchical dictionary representing class inheritance.

        Args:
            root_dir (str): Root directory of the Python project.

        Returns:
            Dict: Nested dictionary representing class inheritance.
        """
        hierarchy = {}
        for dirpath, _, filenames in os.walk(root_dir):
            for file in filenames:
                if file.endswith('.py') and not file.startswith('__'):
                    file_path = os.path.join(dirpath, file)
                    classes = self.parse_file(file_path)
                    for class_name, bases in classes:
                        if not bases:
                            hierarchy[class_name] = {}
                        else:
                            for base in bases:
                                if base not in hierarchy:
                                    hierarchy[base] = {}
                                hierarchy[base][class_name] = {}
        return hierarchy
