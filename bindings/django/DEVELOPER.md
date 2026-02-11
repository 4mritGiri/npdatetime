# Developer Guide - Django NPDateTime

## For Package Maintainers

### Project Structure

The Django package lives in `bindings/django/` but depends on assets from `bindings/javascript/`:

```
npdatetime/
├── bindings/
│   ├── javascript/              # Source of truth for UI
│   │   ├── picker.js      # Main date picker
│   │   ├── picker.css     # Styles
│   │   └── pkg/                # WASM bindings
│   │
│   └── django/                 # Django package
│       ├── build_assets.py     # Asset sync script ⭐
│       ├── npdt/
│       │   └── static/npdt/
│       │       ├── js/
│       │       │   ├── picker.min.js  # Copied from ../javascript/
│       │       │   └── pkg/                # Copied from ../javascript/
│       │       └── css/
│       │           └── picker.css     # Copied from ../javascript/
```

## Important: Single Source of Truth

**DO NOT edit files in `npdt/static/` directly!**

These files are **copied** from `bindings/javascript/`. If you edit them directly, your changes will be overwritten.

### Workflow When Updating JavaScript/CSS

1. **Edit the source files** in `bindings/javascript/`:
   - `picker.js`
   - `picker.css`

2. **Run the build script** to sync to Django:
   ```bash
   cd bindings/django
   python3 build_assets.py
   # or
   ./build_assets.sh
   ```

3. **Test the Django package**:
   ```bash
   pip install -e .  # Install in development mode
   # Test in a Django project
   ```

4. **Commit both locations** if needed:
   ```bash
   git add bindings/javascript/picker.js
   git add bindings/django/npdt/static/npdt/js/picker.min.js
   git commit -m "Update date picker UI"
   ```

## Build Assets Script

### What It Does

The `build_assets.py` script:
- Copies `picker.js` → `static/npdt/js/picker.min.js`
- Copies `picker.css` → `static/npdt/css/picker.css`
- Copies `pkg/` directory → `static/npdt/js/pkg/`

### When to Run It

Run the build script whenever you:
- Update the JavaScript date picker code
- Update the CSS styles
- Rebuild the WASM bindings
- Before publishing a new version

### Usage

```bash
# Python version (cross-platform)
python3 build_assets.py

# Bash version (Linux/Mac)
./build_assets.sh
```

## Development Setup

### 1. Install the Package in Development Mode

```bash
cd bindings/django
pip install -e .
```

This creates a symlink so changes are reflected immediately.

### 2. Create a Test Django Project

```bash
django-admin startproject testproject
cd testproject

# Add to settings.py
INSTALLED_APPS = [
    ...
    'npdt',
]

# Create test app
python manage.py startapp testapp
```

### 3. Test the Package

Create test models, forms, and views using the package components.

## Publishing Workflow

### 1. Update Version

Update version in:
- `setup.py`
- `pyproject.toml`
- `npdt/__init__.py`
- `CHANGELOG.md`

### 2. Build Assets

```bash
python3 build_assets.py
```

### 3. Build Package

```bash
python setup.py sdist bdist_wheel
```

### 4. Test on TestPyPI (Optional)

```bash
pip install twine
twine upload --repository testpypi dist/*
```

### 5. Publish to PyPI

```bash
twine upload dist/*
```

## Common Tasks

### Update JavaScript Only

```bash
# 1. Edit bindings/javascript/picker.js
# 2. Run build script
cd bindings/django
python3 build_assets.py
```

### Update WASM Bindings

```bash
# 1. Rebuild WASM
cd bindings/javascript
wasm-pack build

# 2. Sync to Django
cd ../django
python3 build_assets.py
```

### Update CSS Styles

```bash
# 1. Edit bindings/javascript/picker.css
# 2. Run build script
cd bindings/django
python3 build_assets.py
```

## Testing Checklist

Before publishing a new version:

- [ ] Run `build_assets.py` to sync latest changes
- [ ] Test in a fresh Django project
- [ ] Test model fields (create, read, update, delete)
- [ ] Test form widgets in regular forms
- [ ] Test form widgets in Django admin
- [ ] Test all template tags and filters
- [ ] Test BS ↔ AD conversion
- [ ] Test both English and Nepali languages
- [ ] Test all three themes (auto, light, dark)
- [ ] Check that WASM files load correctly
- [ ] Verify static files are included in package
- [ ] Update CHANGELOG.md
- [ ] Tag release in git

## File Organization

### Python Files (Edit Freely)
- `npdt/__init__.py`
- `npdt/models.py`
- `npdt/forms.py`
- `npdt/widgets.py`
- `npdt/utils.py`
- `npdt/templatetags/nepali_date.py`

### Template Files (Edit Freely)
- `npdt/templates/`

### Static Files (DO NOT EDIT - Run build script)
- `npdt/static/` ← Copied from `../javascript/`

### Configuration Files (Edit When Needed)
- `setup.py` - Package metadata
- `pyproject.toml` - Modern packaging config
- `MANIFEST.in` - Package data inclusion

## Troubleshooting

### Static Files Not Loading

1. Check that `build_assets.py` ran successfully
2. Verify files exist in `static/npdt/`
3. Run `python manage.py collectstatic` in test project
4. Check browser console for 404 errors

### WASM Not Loading

1. Ensure `pkg/` directory was copied
2. Check WASM MIME type in web server config
3. Verify CORS headers if serving from CDN

### Changes Not Reflected

1. Clear browser cache
2. Restart Django development server
3. Check that you ran `build_assets.py`
4. Verify you're editing source files, not copies

## Questions?

- Check the [main README](README.md)
- Review [example code](example/)
- Open an issue on GitHub
