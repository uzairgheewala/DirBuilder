# src/hierarchy/parser_factory.py

from typing import Optional
from .base_parser import BaseParser
from .verilog_parser import VerilogParser
from .python_parser import PythonParser
from .java_parser import JavaParser
from typing import Dict

class ParserFactory:
    """
    Factory to create hierarchy parsers based on project type.
    """

    @staticmethod
    def get_parser(project_type: str) -> Optional[BaseParser]:
        """
        Returns an instance of the parser corresponding to the project type.

        Args:
            project_type (str): Type of the project (e.g., 'verilog', 'python').

        Returns:
            BaseParser: Instance of the appropriate parser or None if not found.
        """
        parsers = {
            'verilog': VerilogParser(),
            'python': PythonParser(),
            'java': JavaParser(),
            # Add other built-in project types and their parsers here
        }

        # Load custom parsers from plugins
        ParserFactory.load_custom_parsers(parsers)

        return parsers.get(project_type.lower(), None)

    @staticmethod
    def load_custom_parsers(parsers: dict):
        """
        Dynamically loads custom parsers from the 'plugins' directory.

        Args:
            parsers (dict): Existing parsers dictionary to update with custom parsers.
        """
        plugins_package = 'plugins'
        try:
            plugins = importlib.import_module(plugins_package)
            for _, name, _ in pkgutil.iter_modules(plugins.__path__):
                module = importlib.import_module(f"{plugins_package}.{name}")
                for attr in dir(module):
                    obj = getattr(module, attr)
                    if isinstance(obj, type) and issubclass(obj, BaseParser) and obj is not BaseParser:
                        parser_instance = obj()
                        parsers[name.lower()] = parser_instance
        except ModuleNotFoundError:
            # No plugins directory found; proceed without custom parsers
            pass
    
    def build_project_hierarchy(self, root_dir: str, project_type: str) -> Dict:
        """
        Builds the project hierarchy using the appropriate parser.

        Args:
            root_dir (str): Root directory of the project.
            project_type (str): Type of the project (e.g., 'verilog', 'python').

        Returns:
            Dict: Hierarchical dictionary representing the project structure.
        """
        parser: BaseParser = ParserFactory.get_parser(project_type)
        if not parser:
            raise ValueError(f"No parser available for project type '{project_type}'.")
        
        return parser.get_hierarchy(root_dir)
