#!/bin/bash
# Script to update version across all packages

set -e

if [ -z "$1" ]; then
    echo "Usage: ./update-version.sh <version>"
    echo "Example: ./update-version.sh 0.2.0"
    exit 1
fi

VERSION=$1
echo "📦 Updating version to $VERSION across all packages..."

# Update Rust crate
echo "   Updating Cargo.toml..."
sed -i.bak "s/^version = \".*\"/version = \"$VERSION\"/" Cargo.toml
rm Cargo.toml.bak

# Update Python bindings
echo "   Updating Python bindings..."
sed -i.bak "s/^version = \".*\"/version = \"$VERSION\"/" bindings/python/Cargo.toml
sed -i.bak "s/version = \".*\"/version = \"$VERSION\"/" bindings/python/pyproject.toml
rm bindings/python/Cargo.toml.bak bindings/python/pyproject.toml.bak

# Update JavaScript/WASM
echo "   Updating JavaScript package..."
cd bindings/javascript
npm version $VERSION --no-git-tag-version
cd ../..

# Update Django package
echo "   Updating Django package..."
sed -i.bak "s/version='.*'/version='$VERSION'/" bindings/django/setup.py
sed -i.bak "s/version = \".*\"/version = \"$VERSION\"/" bindings/django/pyproject.toml
sed -i.bak "s/__version__ = '.*'/__version__ = '$VERSION'/" bindings/django/npdatetime_django/__init__.py
rm bindings/django/setup.py.bak bindings/django/pyproject.toml.bak bindings/django/npdatetime_django/__init__.py.bak

echo "✅ Version updated to $VERSION in all packages!"
echo ""
echo "Next steps:"
echo "1. Update CHANGELOG.md files"
echo "2. Run: cd bindings/django && python3 build_assets.py"
echo "3. Test all packages"
echo "4. Commit: git add . && git commit -m 'chore: bump version to $VERSION'"
echo "5. Tag: git tag v$VERSION"
echo "6. Push: git push && git push --tags"
