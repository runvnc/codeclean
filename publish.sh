#!/bin/bash

echo "=== pycodeclean PyPI Publication Script ==="
echo ""

# Step 1: Make sure build tools are installed
echo "Installing build tools..."
pip install --upgrade pip build twine
echo ""

# Step 2: Clean previous builds
echo "Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info
echo ""

# Step 3: Build the package
echo "Building package..."
python -m build
echo ""

# Step 4: Check the build
echo "Checking distribution package..."
twine check dist/*
echo ""

# Step 5: Ask for confirmation before uploading
read -p "Ready to upload to PyPI? (y/n): " confirm
if [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]]; then
	echo "Uploading to PyPI..."
	python -m twine upload dist/*
	echo ""
	echo "Package published to PyPI!"
	echo "Users can now install with: pip install pycodeclean"
else
	echo "Upload canceled."
	echo "To upload later, run: python -m twine upload dist/*"
fi
