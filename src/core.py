import os
from typing import List, Set, Tuple

def generate_directory_tree(
    root_dir: str, 
    exclude_extensions: Set[str] = None,
    exclude_folders: Set[str] = None
) -> Tuple[List[str], List[str]]:
    """
    Generates a directory tree starting from root_dir.

    Args:
        root_dir (str): The root directory from which to start the tree.
        exclude_extensions (Set[str], optional): File extensions to exclude.
        exclude_folders (Set[str], optional): Folder names to exclude.

    Returns:
        Tuple[List[str], List[str]]: A tuple containing the directory tree lines and skipped items.
    """
    skipped_files = []
    skipped_folders = []
    tree_lines = []

    root_dir = os.path.abspath(root_dir)
    if not os.path.exists(root_dir):
        raise FileNotFoundError(f"The directory '{root_dir}' does not exist.")

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Exclude specified folders
        if exclude_folders:
            orig_dirnames = dirnames.copy()
            dirnames[:] = [d for d in dirnames if d not in exclude_folders]
            skipped = set(orig_dirnames) - set(dirnames)
            for d in skipped:
                full_path = os.path.join(dirpath, d)
                skipped_folders.append(full_path)

        # Calculate depth level
        level = dirpath.replace(root_dir, '').count(os.sep)
        indent = '    ' * level
        dir_name = os.path.basename(dirpath) if os.path.basename(dirpath) else dirpath
        tree_lines.append(f"{indent}{dir_name}/")

        # Add files
        sub_indent = '    ' * (level + 1)
        for file in sorted(filenames):
            _, ext = os.path.splitext(file)
            if exclude_extensions and ext in exclude_extensions:
                skipped_files.append(os.path.join(dirpath, file))
                continue
            tree_lines.append(f"{sub_indent}{file}")

    return tree_lines, skipped_files, skipped_folders
