#!/usr/bin/env python3

import os
from setuptools import setup, find_packages

# Get the long description from the README file
with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="pycodeclean",
    version="0.1.0",
    description="A tool to clean up Python code by removing print statements, debug calls, and comments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/pycodeclean",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
    ],
    keywords="code cleanup, python, print, debug, comments",
    python_requires=">=3.6",
    install_requires=[
        # No external dependencies required
    ],
    entry_points={
        "console_scripts": [
            "pycodeclean=pycodeclean.cli:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/yourusername/pycodeclean/issues",
        "Source": "https://github.com/yourusername/pycodeclean",
    },
)
