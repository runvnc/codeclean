#!/usr/bin/env python3
"""
Command-line interface for the CodeCleaner tool.
"""

import argparse
from pathlib import Path
from typing import Set

from .core import clean_file, clean_directory


def main():
    """Command-line interface entry point for the code cleaner tool."""
    parser = argparse.ArgumentParser(description='Clean Python code by removing specific function calls and comments.')
    
    parser.add_argument('path', help='Path to Python file or directory to clean')
    parser.add_argument(
        '--functions', '-f', 
        help='Comma-separated list of function names to remove (default: print)',
        default='print'
    )
    parser.add_argument(
        '--remove-comments', '-c', 
        action='store_true', 
        help='Also remove all comments from the code'
    )
    parser.add_argument(
        '--recursive', '-r', 
        action='store_true', 
        help='Process directories recursively'
    )
    parser.add_argument(
        '--dry-run', '-d', 
        action='store_true', 
        help="Don't actually modify files, just show what would be done"
    )
    parser.add_argument(
        '--no-backup', '-n',
        action='store_true',
        help="Don't create backups in /tmp before modifying files"
    )
    parser.add_argument(
        '--empty-blocks', '-e',
        choices=['pass', 'remove', 'keep'],
        default='pass',
        help="How to handle blocks that become empty after removing function calls: "
             "add 'pass' statement (default), remove the block, or keep it empty"
    )
    
    args = parser.parse_args()
    
    # Convert function names to a set
    function_names = {name.strip() for name in args.functions.split(',') if name.strip()}
    
    path = Path(args.path)
    
    # Handle directory or file
    if path.is_dir():
        print(f"Processing directory: {path}")
        stats = clean_directory(
            path, 
            function_names, 
            args.remove_comments, 
            args.recursive,
            args.dry_run,
            not args.no_backup,
            args.empty_blocks
        )
        
        # Print summary
        total_calls_removed = sum(s['function_calls_removed'] for s in stats)
        total_files_with_comments_removed = sum(1 for s in stats if s['comments_removed'])
        total_files_modified = sum(1 for s in stats if s['function_calls_removed'] > 0 or s['comments_removed'])
        
        print("\nSummary:")
        print(f"Files processed: {len(stats)}")
        print(f"Files modified: {total_files_modified}")
        print(f"Function calls removed: {total_calls_removed}")
        print(f"Files with comments removed: {total_files_with_comments_removed}")
        
        if not args.no_backup and not args.dry_run:
            print(f"Backups created in /tmp for all modified files")
        
        if args.dry_run:
            print("\nThis was a dry run. No files were modified.")
    
    elif path.is_file():
        print(f"Processing file: {path}")
        stats = clean_file(
            path, 
            function_names, 
            args.remove_comments,
            args.dry_run,
            not args.no_backup,
            args.empty_blocks
        )
        
        print("\nResults:")
        print(f"Function calls removed: {stats['function_calls_removed']}")
        print(f"Comments removed: {stats['comments_removed']}")
        
        if stats['backup_path']:
            print(f"Backup created at: {stats['backup_path']}")
        
        if args.dry_run:
            print("\nThis was a dry run. No files were modified.")
    
    else:
        print(f"Error: {path} does not exist")
        return 1
    
    return 0


if __name__ == '__main__':
    main()
