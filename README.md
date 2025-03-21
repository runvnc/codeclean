# PyCodeClean

A Python tool to clean up code by removing specific function calls (like print statements) and comments.

## Features

- Remove function calls by name (default: `print`)
- Optionally remove all comments (while preserving docstrings)
- Process individual files or entire directories recursively
- Dry-run mode to preview changes without modifying files
- Create backups in /tmp before modifying files
- Smart handling of control blocks that become empty after removal

## Installation

### From PyPI

```bash
pip install pycodeclean
```

### From Source

```bash
git clone https://github.com/yourusername/pycodeclean.git
cd pycodeclean
pip install -e .
```

## Usage

### Basic Usage

Once installed, you can use the `pycodeclean` command:

```bash
# Remove print statements from a file
pycodeclean file.py

# Remove print statements from all Python files in a directory
pycodeclean my_project/

# Remove print statements and comments from files in a directory and subdirectories
pycodeclean my_project/ --remove-comments --recursive
```

### Command-line Options

```
pycodeclean [-h] [--functions FUNCTIONS] [--remove-comments] [--recursive] 
            [--dry-run] [--no-backup] [--empty-blocks {pass,remove,keep}] path
```

- `path`: Path to Python file or directory to clean
- `--functions, -f`: Comma-separated list of function names to remove (default: print)
- `--remove-comments, -c`: Also remove all comments from the code (preserves docstrings)
- `--recursive, -r`: Process directories recursively
- `--dry-run, -d`: Don't actually modify files, just show what would be done
- `--no-backup, -n`: Don't create backups in /tmp before modifying files
- `--empty-blocks, -e`: How to handle blocks that become empty (pass, remove, keep)

### Empty Block Handling

When removing function calls, control structures (if/for/while) may become empty. PyCodeClean provides three options:

- `pass` (default): Add a `pass` statement to empty blocks
- `remove`: Remove the entire empty control structure
- `keep`: Keep the empty block as-is (not recommended, may cause syntax errors)

### Examples

```bash
# Remove print, debug, and logging.info calls
pycodeclean my_project/ -f "print,debug,logging.info" -r

# Preview what would be removed without changing files
pycodeclean my_project/ -d -c

# Remove print statements and remove any resulting empty control blocks
pycodeclean my_project/ --empty-blocks remove

# Remove print statements without creating backups
pycodeclean my_project/ --no-backup
```

## Backup System

By default, PyCodeClean creates backups of all modified files in the `/tmp` directory with timestamped filenames. For example, a file named `script.py` would be backed up as `/tmp/script_20250316_153000.py` before modification.

To disable backups, use the `--no-backup` flag.

## How It Works

PyCodeClean uses Python's Abstract Syntax Tree (AST) to parse and transform code, ensuring that only the specified function calls are removed while preserving the overall structure of the code. 

For comment removal, it uses regex patterns to identify and remove comment lines while preserving docstrings.

## Example Results

Before:
```python
def process_data(data):
    # Process the input data
    if debug_mode:
        print("Processing data:", data)  # Debug info
        return data  # Just return in debug mode
    
    # Actual processing
    result = data * 2
    return result
```

After (with print removal and `--empty-blocks pass`):
```python
def process_data(data):
    # Process the input data
    if debug_mode:
        pass
        return data  # Just return in debug mode
    
    # Actual processing
    result = data * 2
    return result
```

After (with print removal and `--empty-blocks remove`):
```python
def process_data(data):
    # Process the input data
    # Actual processing
    result = data * 2
    return result
```

After (with print and comment removal):
```python
def process_data(data):
    result = data * 2
    return result
```

## Publishing to PyPI

To publish this package to PyPI, follow these steps:

1. Update the project information in `setup.py` and `pyproject.toml` with your details
2. Install build and twine:
   ```bash
   pip install build twine
   ```
3. Build the package:
   ```bash
   python -m build
   ```
4. Upload to PyPI:
   ```bash
   python -m twine upload dist/*
   ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
