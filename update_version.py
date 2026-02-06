#!/usr/bin/env python3
"""
Script to update version across all packages in the npdatetime-rust project.

Usage:
    python update_version.py <version>
    python update_version.py 0.2.0
"""

import sys
import re
from pathlib import Path
import io

# Force UTF-8 encoding for stdout to avoid issues on Windows CI
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def update_file(file_path: Path, pattern: str, replacement: str, description: str):
    """Update version in a single file."""
    if not file_path.exists():
        print(f"   ⚠ Warning: {file_path} not found, skipping")
        return False
    
    content = file_path.read_text()
    new_content = re.sub(pattern, replacement, content)
    
    if content != new_content:
        file_path.write_text(new_content)
        print(f"   ✓ Updated {description}")
        return True
    else:
        print(f"   ℹ No changes needed in {description}")
        return False


def update_version(version: str):
    """Update version across all package files."""
    print(f"📦 Updating version to {version} across all packages...\n")
    
    root = Path(__file__).parent
    
    updates = [
        # Rust crate
        (
            root / "Cargo.toml",
            r'^version = ".*"',
            f'version = "{version}"',
            "Cargo.toml"
        ),
        
        # Python bindings
        (
            root / "bindings/python/Cargo.toml",
            r'^version = ".*"',
            f'version = "{version}"',
            "Python Cargo.toml"
        ),
        (
            root / "bindings/python/pyproject.toml",
            r'version = ".*"',
            f'version = "{version}"',
            "Python pyproject.toml"
        ),
        
        # JavaScript/WASM
        (
            root / "bindings/javascript/package.json",
            r'"version": ".*"',
            f'"version": "{version}"',
            "JavaScript package.json"
        ),
        
        # Django package
        (
            root / "bindings/django/setup.py",
            r"version='.*'",
            f"version='{version}'",
            "Django setup.py"
        ),
        (
            root / "bindings/django/pyproject.toml",
            r'version = ".*"',
            f'version = "{version}"',
            "Django pyproject.toml"
        ),
        (
            root / "bindings/django/npdatetime_django/__init__.py",
            r"__version__ = '.*'",
            f"__version__ = '{version}'",
            "Django __init__.py"
        ),
    ]
    
    success_count = 0
    for file_path, pattern, replacement, desc in updates:
        if update_file(file_path, pattern, replacement, desc):
            success_count += 1
    
    print(f"\n✅ Version updated to {version} in {success_count} file(s)!")
    print("\nNext steps:")
    print("1. Update CHANGELOG.md files")
    print("2. Run: cd bindings/django && python3 build_assets.py")
    print("3. Test all packages")
    print(f"4. Commit: git add . && git commit -m 'chore: bump version to {version}'")
    print(f"5. Tag: git tag v{version}")
    print("6. Push: git push && git push --tags")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python update_version.py <version>")
        print("Example: python update_version.py 0.2.0")
        sys.exit(1)
    
    version = sys.argv[1]
    
    # Validate version format (basic semver check)
    if not re.match(r'^\d+\.\d+\.\d+(-[a-zA-Z0-9.]+)?$', version):
        print(f"Error: Invalid version format: {version}")
        print("Expected format: X.Y.Z or X.Y.Z-suffix (e.g., 1.0.0 or 1.0.0-beta.1)")
        sys.exit(1)
    
    update_version(version)
