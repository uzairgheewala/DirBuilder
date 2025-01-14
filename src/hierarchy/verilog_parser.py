import os
import re
from typing import List, Dict
from .base_parser import BaseParser
import shutil
import numpy as np

class VerilogParser(BaseParser):
    """
    Parser for Verilog projects to identify modules and their submodules.
    """

    MODULE_DECLARATION_REGEX = re.compile(r'^\s*module\s+(\w+)', re.MULTILINE)
    MODULE_INSTANCING_REGEX = re.compile(r'\b(\w+)\s+(\w+)\s*\(', re.MULTILINE)

    def parse_file(self, file_path: str) -> List[str]:
        """
        Parses a Verilog file to identify submodules.

        Args:
            file_path (str): Path to the Verilog file.

        Returns:
            List[str]: List of submodule names.
        """
        submodule_names = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Find all module declarations in the file
            declared_modules = self.MODULE_DECLARATION_REGEX.findall(content)

            # Find all module instantiations (submodules)
            instantiations = self.MODULE_INSTANCING_REGEX.findall(content)
            instantiated_modules = [match[0] for match in instantiations]

            # Exclude self-instantiations
            current_module = os.path.splitext(os.path.basename(file_path))[0]
            for submodule in instantiated_modules:
                if submodule != current_module and submodule in declared_modules:
                    submodule_names.append(submodule)
                elif submodule != current_module and submodule not in declared_modules:
                    submodule_names.append(submodule)

            # Remove duplicates
            submodule_names = list(np.unique(submodule_names))
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")

        return submodule_names

    def get_hierarchy(self, root_dir: str) -> Dict:
        """
        Builds a hierarchical dictionary representing modules and submodules.

        Args:
            root_dir (str): Root directory of the Verilog project.

        Returns:
            Dict: Nested dictionary representing module hierarchy.
        """
        hierarchy = {}
        visited = set()

        def traverse(module_name: str, current_dir: str):
            if module_name in visited:
                return
            visited.add(module_name)

            module_file = self.find_module_file(module_name, current_dir)
            if not module_file:
                print(f"Module file for '{module_name}' not found in '{current_dir}'.")
                hierarchy[module_name] = {}
                return

            submodules = self.parse_file(module_file)
            hierarchy[module_name] = {}

            for submodule in submodules:
                # Assume submodules are located in the 'src' directory or subdirectories
                submodule_file = self.find_module_file(submodule, root_dir)
                if submodule_file:
                    traverse(submodule, os.path.dirname(submodule_file))
                else:
                    hierarchy[module_name][submodule] = {}

        # Start traversal from the top-level modules
        for dirpath, _, filenames in os.walk(root_dir):
            for file in filenames:
                if file.endswith('.v'):
                    module_name = os.path.splitext(file)[0]
                    traverse(module_name, dirpath)

        return hierarchy

    def find_module_file(self, module_name: str, search_dir: str) -> str:
        """
        Searches for the Verilog file corresponding to the module name within a directory.

        Args:
            module_name (str): Name of the module.
            search_dir (str): Directory to search in.

        Returns:
            str: Path to the Verilog file if found, else an empty string.
        """
        for root, _, files in os.walk(search_dir):
            for file in files:
                if file == f"{module_name}.v":
                    return os.path.join(root, file)
        return ""