#!/usr/bin/env python3
"""
Build script to copy static assets from JavaScript bindings to Django package.
Run this script whenever you update the date picker JavaScript or CSS.

Usage:
    python build_assets.py
"""

import os
import shutil
from pathlib import Path


def main():
    print("📦 Building Django package assets...")
    
    # Define paths
    script_dir = Path(__file__).parent
    js_source = script_dir.parent / "javascript"
    django_static = script_dir / "npdatetime_django" / "static" / "npdatetime_django"
    
    # Create directories if they don't exist
    (django_static / "js").mkdir(parents=True, exist_ok=True)
    (django_static / "css").mkdir(parents=True, exist_ok=True)
    
    # Copy JavaScript files
    print("   Copying JavaScript files...")
    js_file = js_source / "picker.js"
    if js_file.exists():
        shutil.copy2(js_file, django_static / "js" / "picker.min.js")
        print(f"   ✓ {js_file.name} → picker.min.js")
    else:
        print(f"   ⚠ Warning: {js_file} not found")
    
    # Copy CSS files
    print("   Copying CSS files...")
    css_file = js_source / "picker.css"
    if css_file.exists():
        shutil.copy2(css_file, django_static / "css" / "picker.css")
        print(f"   ✓ {css_file.name} → picker.css")
    else:
        print(f"   ⚠ Warning: {css_file} not found")
    
    # Copy WASM package
    print("   Copying WASM bindings...")
    pkg_dir = js_source / "pkg"
    if pkg_dir.exists() and pkg_dir.is_dir():
        dest_pkg = django_static / "js" / "pkg"
        if dest_pkg.exists():
            shutil.rmtree(dest_pkg)
        shutil.copytree(pkg_dir, dest_pkg)
        print("   ✓ WASM bindings copied")
    else:
        print("   ⚠ Warning: WASM pkg directory not found. Run 'wasm-pack build' first.")
    
    print("\n✅ Assets built successfully!")
    print("\n📝 Summary:")
    print("   - picker.js → picker.min.js")
    print("   - picker.css → picker.css")
    print("   - pkg/ → js/pkg/")
    print("\n💡 Tip: Run 'python build_assets.py' whenever you update the JavaScript/CSS files")


if __name__ == "__main__":
    main()
