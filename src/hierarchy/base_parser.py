from abc import ABC, abstractmethod
from typing import List, Dict

class BaseParser(ABC):
    """
    Abstract base class for hierarchy parsers.
    """

    @abstractmethod
    def parse_file(self, file_path: str) -> List[str]:
        """
        Parses a file to identify hierarchical elements (e.g., submodules, classes).

        Args:
            file_path (str): Path to the file to parse.

        Returns:
            List[str]: List of identified hierarchical elements.
        """
        pass

    @abstractmethod
    def get_hierarchy(self, root_dir: str) -> Dict:
        """
        Builds a hierarchical representation of the project.

        Args:
            root_dir (str): Root directory of the project.

        Returns:
            Dict: Nested dictionary representing the hierarchy.
        """
        pass
