# 📋 Summary: Django Package Workflow

## The Key Point

**JavaScript/CSS files have ONE source location:**
- ✅ Source: `bindings/javascript/picker.js`
- ✅ Source: `bindings/javascript/picker.css`
- ❌ Copy: `bindings/django/npdt/static/.../picker.min.js`
- ❌ Copy: `bindings/django/npdt/static/.../picker.css`

## Your Workflow

### When You Update JavaScript/CSS:

```bash
# 1. Edit the source files
vim bindings/javascript/picker.js
vim bindings/javascript/picker.css

# 2. Sync to Django package
cd bindings/django
python3 build_assets.py

# 3. Test (if in development mode)
# Changes are automatically reflected

# 4. Commit (if satisfied)
git add bindings/javascript/picker.js
git add bindings/django/npdt/static/...
git commit -m "Update date picker"
```

### What `build_assets.py` Does:

```python
# Copies these files:
../javascript/picker.js    → static/.../js/picker.min.js
../javascript/picker.css   → static/.../css/picker.css
../javascript/pkg/*             → static/.../js/pkg/*
```

## Publishing

All packages are published via GitHub Actions when a version tag is pushed. The `Makefile` provides convenience targets:

### Bump Version

```bash
# Bump version across all packages (Cargo.toml, pyproject.toml, setup.py, etc.)
make publish-bump VERSION=0.3.0
# Commits with [skip ci] to avoid triggering CI
```

### Publish

```bash
# Tag current version and push to GitHub — triggers CI to publish all packages
make publish

# Dry run — show what would happen without pushing
make publish-dry
```

### Clean a Tag

```bash
# Delete a version tag locally and remotely
make publish-clean VERSION=0.2.5
```

### What CI Publishes

When a `v*.*.*` tag is pushed, the `publish.yml` workflow publishes:

| Package | Target |
|---------|--------|
| 🦀 Rust crate | crates.io |
| 🐍 Python package | PyPI |
| 🌐 WASM package | npm (`@4mritgiri/npdatetime`) |
| 🎯 Django package | PyPI (`django-npdt`) |
| 🐘 PHP package | GitHub release assets |

Monitor: https://github.com/4mritGiri/npdatetime/actions

## Why This Approach?

✅ **Single source of truth** - No confusion about which file to edit
✅ **Automatic sync** - Script handles copying
✅ **Version control** - Both locations tracked
✅ **Clear workflow** - Edit source, run script, test

## Quick Reference

| Task | Command |
|------|---------|
| Update JavaScript | Edit `bindings/javascript/picker.js` |
| Update CSS | Edit `bindings/javascript/picker.css` |
| Sync to Django | `python3 build_assets.py` |
| Install for dev | `pip install -e .` |
| Build package | `python setup.py sdist bdist_wheel` |
| Bump version | `make publish-bump VERSION=X.Y.Z` |
| Publish | `make publish` |
| Publish dry run | `make publish-dry` |
| Clean tag | `make publish-clean VERSION=X.Y.Z` |

## Files Created

1. **Build Scripts:**
   - [build_assets.py](file:///media/amrit/SSDAmrit/Builds/Packages/npdatetime-rust/bindings/django/build_assets.py) - Python version (cross-platform)
   - [build_assets.sh](file:///media/amrit/SSDAmrit/Builds/Packages/npdatetime-rust/bindings/django/build_assets.sh) - Bash version

2. **Documentation:**
   - [DEVELOPER.md](file:///media/amrit/SSDAmrit/Builds/Packages/npdatetime-rust/bindings/django/DEVELOPER.md) - Complete developer guide
   - [README.md](file:///media/amrit/SSDAmrit/Builds/Packages/npdatetime-rust/bindings/django/README.md) - Updated with workflow note

That's it! Now you have a clean workflow with no duplication confusion. 🎉
