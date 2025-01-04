#!/bin/bash

# Ensure that the script stops on errors
set -e

# Step 1: Clean the old build files
echo "Cleaning old build files..."
rm -rf dist/ build/ *.egg-info

# Step 2: Build the package
echo "Building the package..."
python -m build

# Step 3: Upload to PyPI
echo "Uploading the package to PyPI..."
twine upload dist/*

# Step 4: Tag the release in git (optional)
# You should pass the version number as an argument to the script
if [ -z "$1" ]; then
   echo "Error: No version provided for the tag."
   echo "Usage: ./build.sh <version>"
   exit 1
fi

echo "Creating Git tag for version $1..."
git tag -a "v$1" -m "Release version $1"
git push origin "v$1"

echo "Build and upload process completed successfully!"
