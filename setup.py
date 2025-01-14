# setup.py

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="DirBuilder",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool to generate and visualize directory structures with multiple output formats.",
    long_description_content_type="text/markdown",
    url="https://github.com/uzairgheewala/DirBuilder",
    packages=find_packages(where='src'),
    package_dir={"": "src"},
    install_requires=[
        "python-docx",
        "fpdf",
        "PyYAML"
    ],
    entry_points={
        'console_scripts': [
            'dirgen=cli:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Update based on chosen license
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
