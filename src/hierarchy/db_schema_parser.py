import os
import re
from typing import List, Dict
from .base_parser import BaseParser

class DatabaseSchemaParser(BaseParser):
    """
    Parser for database schema projects to identify tables and their relationships.
    """

    TABLE_REGEX = re.compile(r'CREATE TABLE (\w+) \(')
    FOREIGN_KEY_REGEX = re.compile(r'FOREIGN KEY \((\w+)\) REFERENCES (\w+)\((\w+)\)')

    def parse_file(self, file_path: str) -> Dict[str, List[str]]:
        """
        Parses a SQL file to identify tables and their foreign key relationships.

        Args:
            file_path (str): Path to the SQL file.

        Returns:
            Dict[str, List[str]]: Dictionary with table names as keys and list of referenced tables as values.
        """
        relationships = {}
        current_table = None

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            for line in lines:
                table_match = self.TABLE_REGEX.search(line)
                if table_match:
                    current_table = table_match.group(1)
                    relationships[current_table] = []
                elif current_table:
                    fk_match = self.FOREIGN_KEY_REGEX.search(line)
                    if fk_match:
                        referenced_table = fk_match.group(2)
                        relationships[current_table].append(referenced_table)
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")

        return relationships

    def get_hierarchy(self, root_dir: str) -> Dict:
        """
        Builds a hierarchical dictionary representing table relationships.

        Args:
            root_dir (str): Root directory of the database schema project.

        Returns:
            Dict: Nested dictionary representing table relationships.
        """
        hierarchy = {}
        table_dependencies = {}

        for dirpath, _, filenames in os.walk(root_dir):
            for file in filenames:
                if file.endswith('.sql'):
                    file_path = os.path.join(dirpath, file)
                    relationships = self.parse_file(file_path)
                    for table, references in relationships.items():
                        if table not in table_dependencies:
                            table_dependencies[table] = set()
                        table_dependencies[table].update(references)

        # Build the hierarchy
        for table, references in table_dependencies.items():
            if table not in hierarchy:
                hierarchy[table] = {}
            for ref in references:
                hierarchy[table][ref] = {}

        return hierarchy
