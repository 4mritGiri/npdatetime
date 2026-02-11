#!/bin/bash

# Build script to copy static assets from JavaScript bindings to Django package
# Run this script whenever you update the date picker JavaScript or CSS

set -e  # Exit on error

echo "📦 Building Django package assets..."

# Define paths
JS_SOURCE="../javascript"
DJANGO_STATIC="npdt/static/npdt"

# Create directories if they don't exist
mkdir -p "$DJANGO_STATIC/js"
mkdir -p "$DJANGO_STATIC/css"

# Copy JavaScript files
echo "   Copying JavaScript files..."
cp "$JS_SOURCE/picker.js" "$DJANGO_STATIC/js/picker.min.js"

# Copy CSS files
echo "   Copying CSS files..."
cp "$JS_SOURCE/picker.css" "$DJANGO_STATIC/css/picker.css"

# Copy WASM package
echo "   Copying WASM bindings..."
if [ -d "$JS_SOURCE/pkg" ]; then
    cp -r "$JS_SOURCE/pkg" "$DJANGO_STATIC/js/"
    echo "   ✓ WASM bindings copied"
else
    echo "   ⚠ Warning: WASM pkg directory not found. Run 'wasm-pack build' first."
fi

echo "✅ Assets built successfully!"
echo ""
echo "📝 Summary:"
echo "   - picker.js → picker.min.js"
echo "   - picker.css → picker.css"
echo "   - pkg/ → js/pkg/"
echo ""
echo "💡 Tip: Run './build_assets.sh' whenever you update the JavaScript/CSS files"
