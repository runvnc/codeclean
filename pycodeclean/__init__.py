"""
PyCodeClean - A tool to clean up Python code by removing specific function calls and comments

This tool can:
1. Remove function calls by name (e.g., print, debug, etc.)
2. Optionally remove all comments from the code
3. Process individual files or entire directories recursively
4. Create backups of modified files in /tmp
5. Handle dangling control structures (empty if/for/while blocks)
"""

__version__ = '0.1.0'
__author__ = 'Your Name'
__email__ = 'your.email@example.com'
__license__ = 'MIT'

from .core import (
    FunctionCallRemover,
    create_backup,
    remove_comments,
    clean_file,
    clean_directory,
)

from .cli import main

__all__ = [
    'FunctionCallRemover',
    'create_backup',
    'remove_comments',
    'clean_file',
    'clean_directory',
    'main',
]
