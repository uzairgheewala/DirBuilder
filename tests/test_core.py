import unittest
import os
import shutil
from src.core import generate_directory_tree

class TestCoreModule(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory structure for testing
        self.test_dir = 'test_root'
        os.makedirs(self.test_dir, exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, 'subdir1'), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, 'subdir2', '__pycache__'), exist_ok=True)

        with open(os.path.join(self.test_dir, 'file1.py'), 'w') as f:
            f.write("# Sample Python file")

        with open(os.path.join(self.test_dir, 'file2.txt'), 'w') as f:
            f.write("Sample text file")

        with open(os.path.join(self.test_dir, 'subdir1', 'file3.pyc'), 'w') as f:
            f.write("Compiled Python file")

    def tearDown(self):
        # Remove the temporary directory after tests
        shutil.rmtree(self.test_dir)

    def test_generate_directory_tree(self):
        exclude_extensions = {'.pyc'}
        exclude_folders = {'__pycache__'}
        tree, skipped_files, skipped_folders = generate_directory_tree(
            root_dir=self.test_dir,
            exclude_extensions=exclude_extensions,
            exclude_folders=exclude_folders
        )

        expected_tree = [
            'test_root/',
            '    file1.py',
            '    file2.txt',
            '    subdir1/',
            '        file3.pyc',
            '    subdir2/'
        ]

        self.assertEqual(tree, expected_tree)
        self.assertIn(os.path.join(self.test_dir, 'subdir1', 'file3.pyc'), skipped_files)
        self.assertIn(os.path.join(self.test_dir, 'subdir2', '__pycache__'), skipped_folders)

if __name__ == '__main__':
    unittest.main()
