#!/usr/bin/env python3
"""
Core functionality for the CodeCleaner tool.
"""

import os
import re
import ast
import shutil
import datetime
from pathlib import Path
from typing import List, Set, Union, Optional


class FunctionCallRemover(ast.NodeTransformer):
    """AST NodeTransformer to remove specified function calls and handle empty blocks."""
    
    def __init__(self, function_names: Set[str], handle_empty_blocks: str = 'pass'):
        self.function_names = function_names
        self.removed_count = 0
        self.handle_empty_blocks = handle_empty_blocks  # 'pass', 'remove', or 'keep'
    
    def visit_Expr(self, node):
        """Visit expression nodes and remove if they are calls to specified functions."""
        # Check if this is a function call expression
        if isinstance(node.value, ast.Call):
            # For simple function calls like print(...)
            if isinstance(node.value.func, ast.Name) and node.value.func.id in self.function_names:
                self.removed_count += 1
                return None  # Remove the node
            
            # For attribute function calls like logging.debug(...)
            elif isinstance(node.value.func, ast.Attribute):
                full_name = self._get_full_name(node.value.func)
                if full_name in self.function_names:
                    self.removed_count += 1
                    return None  # Remove the node
        
        # Otherwise, continue with the default behavior
        return self.generic_visit(node)
    
    def _get_full_name(self, node):
        """Extract the full name of an attribute node (e.g., 'logging.debug')."""
        if isinstance(node.value, ast.Name):
            return f"{node.value.id}.{node.attr}"
        elif isinstance(node.value, ast.Attribute):
            return f"{self._get_full_name(node.value)}.{node.attr}"
        return node.attr
    
    def visit_If(self, node):
        """Handle if statements, potentially removing empty blocks."""
        self.generic_visit(node)  # First process any function calls inside
        
        # Check if the body became empty
        if not node.body and self.handle_empty_blocks != 'keep':
            if self.handle_empty_blocks == 'pass':
                node.body = [ast.Pass()]
            else:  # 'remove'
                return None  # Remove the entire if statement
        
        # Check if the else block became empty
        if hasattr(node, 'orelse') and not node.orelse and self.handle_empty_blocks != 'keep':
            if self.handle_empty_blocks == 'pass':
                if isinstance(node.orelse, list):
                    node.orelse = [ast.Pass()]
            else:  # 'remove'
                node.orelse = []  # Remove the else part
        
        return node
    
    def visit_For(self, node):
        """Handle for loops, potentially removing empty blocks."""
        self.generic_visit(node)  # First process any function calls inside
        
        # Check if the body became empty
        if not node.body and self.handle_empty_blocks != 'keep':
            if self.handle_empty_blocks == 'pass':
                node.body = [ast.Pass()]
            else:  # 'remove'
                return None  # Remove the entire for loop
        
        # Check if the else block became empty
        if hasattr(node, 'orelse') and not node.orelse and self.handle_empty_blocks != 'keep':
            if self.handle_empty_blocks == 'pass':
                if isinstance(node.orelse, list):
                    node.orelse = [ast.Pass()]
            else:  # 'remove'
                node.orelse = []  # Remove the else part
        
        return node
    
    def visit_While(self, node):
        """Handle while loops, potentially removing empty blocks."""
        self.generic_visit(node)  # First process any function calls inside
        
        # Check if the body became empty
        if not node.body and self.handle_empty_blocks != 'keep':
            if self.handle_empty_blocks == 'pass':
                node.body = [ast.Pass()]
            else:  # 'remove'
                return None  # Remove the entire while loop
        
        # Check if the else block became empty
        if hasattr(node, 'orelse') and not node.orelse and self.handle_empty_blocks != 'keep':
            if self.handle_empty_blocks == 'pass':
                if isinstance(node.orelse, list):
                    node.orelse = [ast.Pass()]
            else:  # 'remove'
                node.orelse = []  # Remove the else part
        
        return node
    
    def visit_Try(self, node):
        """Handle try blocks, potentially removing empty blocks."""
        self.generic_visit(node)  # First process any function calls inside
        
        # Check if the body became empty
        if not node.body and self.handle_empty_blocks != 'keep':
            if self.handle_empty_blocks == 'pass':
                node.body = [ast.Pass()]
            else:  # 'remove'
                return None  # Remove the entire try block
        
        # Check handlers
        handlers_to_keep = []
        for handler in node.handlers:
            if not handler.body and self.handle_empty_blocks != 'keep':
                if self.handle_empty_blocks == 'pass':
                    handler.body = [ast.Pass()]
                    handlers_to_keep.append(handler)
                # If 'remove', skip adding this handler
            else:
                handlers_to_keep.append(handler)
        
        node.handlers = handlers_to_keep
        
        # Check if finalbody became empty
        if hasattr(node, 'finalbody') and not node.finalbody and self.handle_empty_blocks != 'keep':
            if self.handle_empty_blocks == 'pass':
                node.finalbody = [ast.Pass()]
            else:  # 'remove'
                node.finalbody = []  # Remove the finally part
        
        return node


def create_backup(file_path: Union[str, Path]) -> str:
    """
    Create a backup of the file in /tmp directory with timestamp.
    
    Args:
        file_path: Path to the file to back up
        
    Returns:
        str: Path to the backup file
    """
    file_path = Path(file_path)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
    backup_path = Path("/tmp") / backup_name
    
    try:
        shutil.copy2(file_path, backup_path)
        return str(backup_path)
    except Exception as e:
        print(f"Warning: Failed to create backup for {file_path}: {e}")
        return ""


def remove_comments(source: str) -> str:
    """
    Remove comments from Python source code.
    This uses regex to remove # comments while preserving docstrings.
    Note: This is a simple approach and may not handle all edge cases perfectly.
    """
    # Pattern to match comments but not docstrings
    pattern = r'(?<!\'|\")#[^\n]*'
    return re.sub(pattern, '', source)


def clean_file(
    file_path: Union[str, Path], 
    function_names: Set[str] = None, 
    remove_comments_flag: bool = False,
    dry_run: bool = False,
    create_backup_flag: bool = True,
    handle_empty_blocks: str = 'pass'
) -> dict:
    """
    Clean a single Python file by removing specified function calls and optionally comments.
    
    Args:
        file_path: Path to the Python file
        function_names: Set of function names to remove (e.g., {'print', 'debug'})
        remove_comments_flag: Whether to remove comments
        dry_run: If True, don't actually modify files, just report
        create_backup_flag: Whether to create a backup in /tmp before modifying
        handle_empty_blocks: How to handle blocks that become empty ('pass', 'remove', or 'keep')
        
    Returns:
        dict: Statistics about what would be/was removed
    """
    if function_names is None:
        function_names = {'print'}
    
    file_path = Path(file_path)
    stats = {
        'file': str(file_path),
        'function_calls_removed': 0,
        'comments_removed': False,
        'backup_path': ""
    }
    
    # Check if it's a Python file
    if not file_path.name.endswith('.py'):
        return stats
    
    # Read the file content
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return stats
    
    original_size = len(source)
    modified_source = source
    
    # Remove function calls using AST
    try:
        tree = ast.parse(source)
        transformer = FunctionCallRemover(function_names, handle_empty_blocks)
        transformed_tree = transformer.visit(tree)
        ast.fix_missing_locations(transformed_tree)
        
        # Generate new source code from AST
        from ast import unparse
        transformed_source = unparse(transformed_tree)
        
        stats['function_calls_removed'] = transformer.removed_count
        if transformer.removed_count > 0:
            modified_source = transformed_source
    except Exception as e:
        print(f"Error transforming AST for {file_path}: {e}")
        # Continue with comment removal even if AST transformation fails
    
    # Remove comments if requested
    if remove_comments_flag:
        source_without_comments = remove_comments(modified_source)
        if source_without_comments != modified_source:
            modified_source = source_without_comments
            stats['comments_removed'] = True
    
    # Write back to file if changes were made and not a dry run
    if not dry_run and (stats['function_calls_removed'] > 0 or stats['comments_removed']):
        try:
            # Create backup before modifying
            if create_backup_flag:
                backup_path = create_backup(file_path)
                stats['backup_path'] = backup_path
                if backup_path:
                    print(f"Backup created at: {backup_path}")
            
            # Write the modified content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(modified_source)
            stats['bytes_removed'] = original_size - len(modified_source)
        except Exception as e:
            print(f"Error writing to {file_path}: {e}")
    elif dry_run:
        stats['bytes_would_remove'] = original_size - len(modified_source)
    
    return stats


def clean_directory(
    directory_path: Union[str, Path], 
    function_names: Set[str] = None, 
    remove_comments_flag: bool = False,
    recursive: bool = True,
    dry_run: bool = False,
    create_backup_flag: bool = True,
    handle_empty_blocks: str = 'pass'
) -> List[dict]:
    """
    Clean all Python files in a directory by removing specified function calls and optionally comments.
    
    Args:
        directory_path: Path to the directory
        function_names: Set of function names to remove (e.g., {'print', 'debug'})
        remove_comments_flag: Whether to remove comments
        recursive: Whether to process subdirectories recursively
        dry_run: If True, don't actually modify files, just report
        create_backup_flag: Whether to create a backup in /tmp before modifying
        handle_empty_blocks: How to handle blocks that become empty ('pass', 'remove', or 'keep')
        
    Returns:
        List[dict]: Statistics about each file processed
    """
    if function_names is None:
        function_names = {'print'}
    
    directory_path = Path(directory_path)
    all_stats = []
    
    # Get all files in the directory
    if recursive:
        python_files = list(directory_path.glob('**/*.py'))
    else:
        python_files = list(directory_path.glob('*.py'))
    
    # Process each file
    for file_path in python_files:
        stats = clean_file(
            file_path, 
            function_names, 
            remove_comments_flag, 
            dry_run,
            create_backup_flag,
            handle_empty_blocks
        )
        all_stats.append(stats)
    
    return all_stats
