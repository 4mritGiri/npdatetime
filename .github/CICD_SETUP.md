# GitHub Actions CI/CD Setup Guide

## 🚀 Automated Publishing on Git Tag

Your repository is now configured to automatically build and publish **all packages** when you push a version tag to GitHub.

## 📋 Prerequisites - Setup Required Secrets

Before the workflows can publish, you need to add these secrets to your GitHub repository:

### 1. Go to Repository Settings
```
https://github.com/4mritGiri/npdatetime-rust/settings/secrets/actions
```

### 2. Add These Secrets

#### `CARGO_TOKEN` (for crates.io)
1. Go to https://crates.io/me
2. Click "New Token"
3. Name it "GitHub Actions"
4. Copy the token
5. Add as secret: `CARGO_TOKEN`

#### `NPM_TOKEN` (for npmjs.com)
1. Go to https://www.npmjs.com/settings/YOUR_USERNAME/tokens
2. Click "Generate New Token" → "Classic Token"
3. Select "Automation" type
4. Copy the token
5. Add as secret: `NPM_TOKEN`

#### `PYPI_TOKEN` (for pypi.org)
1. Go to https://pypi.org/manage/account/token/
2. Click "Add API token"
3. Name: "GitHub Actions"
4. Scope: "Entire account" (or specific project)
5. Copy the token (starts with `pypi-`)
6. Add as secret: `PYPI_TOKEN`

## 📦 How to Publish All Packages

### Method 1: Using Git Tags (Recommended)

```bash
# 1. Update version in all package files
#    - Cargo.toml
#    - bindings/python/Cargo.toml
#    - bindings/javascript/package.json
#    - bindings/django/setup.py
#    - bindings/django/pyproject.toml

# 2. Update CHANGELOG.md

# 3. Commit changes
git add .
git commit -m "chore: bump version to 0.1.0"

# 4. Create and push tag
git tag v0.1.0
git push origin v0.1.0

# 5. GitHub Actions will automatically:
#    ✅ Publish Rust crate to crates.io
#    ✅ Publish WASM/JS to npm
#    ✅ Publish Python package to PyPI
#    ✅ Publish Django package to PyPI
#    ✅ Create GitHub Release
```

### Method 2: Manual Trigger

1. Go to Actions tab on GitHub
2. Select "Publish All Packages" workflow
3. Click "Run workflow"
4. Select branch and run

## 🔄 Workflow Overview

### `publish.yml` - Publish All Packages
**Trigger:** Push tag `v*.*.*` (e.g., `v0.1.0`)

**Jobs:**
1. **publish-rust** → crates.io
2. **publish-wasm** → npmjs.com
3. **publish-python** → PyPI (wheels for all platforms)
4. **publish-django** → PyPI
5. **create-release** → GitHub Release with links

### `ci.yml` - Test Rust Crate
**Trigger:** Push/PR to main/develop

**Jobs:**
- Test on Linux, macOS, Windows
- Test with stable and beta Rust
- Run clippy, rustfmt, benchmarks
- Build documentation

### `test-bindings.yml` - Test Python & Django
**Trigger:** Push/PR to main/develop

**Jobs:**
- Test Python package (3.8-3.12, all platforms)
- Test Django package (Django 3.2-5.0, Python 3.8-3.12)
- Import tests for all components

## 📝 Version Update Checklist

Before creating a release tag:

- [ ] Update version in `Cargo.toml`
- [ ] Update version in `bindings/python/Cargo.toml`
- [ ] Update version in `bindings/python/pyproject.toml`
- [ ] Update version in `bindings/javascript/package.json`
- [ ] Update version in `bindings/django/setup.py`
- [ ] Update version in `bindings/django/pyproject.toml`
- [ ] Update version in `bindings/django/npdatetime_django/__init__.py`
- [ ] Update `CHANGELOG.md`
- [ ] Update `bindings/django/CHANGELOG.md`
- [ ] Run `cd bindings/django && python3 build_assets.py`
- [ ] Test all packages locally
- [ ] Commit with message: `chore: bump version to X.Y.Z`
- [ ] Create tag: `git tag vX.Y.Z`
- [ ] Push: `git push && git push --tags`

## 🎯 What Gets Published

| Package | Registry | Name | Documentation |
|---------|----------|------|---------------|
| Rust | crates.io | `npdatetime` | https://docs.rs/npdatetime |
| Python | PyPI | `npdatetime` | https://pypi.org/project/npdatetime |
| JavaScript/WASM | npm | `npdatetime` | https://npmjs.com/package/npdatetime |
| Django | PyPI | `django-npdatetime` | https://pypi.org/project/django-npdatetime |

## 🔍 Monitoring Workflows

### View Workflow Runs
```
https://github.com/4mritGiri/npdatetime-rust/actions
```

### Check Package Status
- Crates.io: https://crates.io/crates/npdatetime
- PyPI (Python): https://pypi.org/project/npdatetime
- PyPI (Django): https://pypi.org/project/django-npdatetime
- npm: https://npmjs.com/package/npdatetime

## 🐛 Troubleshooting

### Workflow fails with "no such file"
- Run `cd bindings/django && python3 build_assets.py` before tagging
- Ensure WASM is built: `cd bindings/javascript && wasm-pack build`

### "Package already published"
- This is expected and workflow continues (set to `continue-on-error: true`)
- Update version number for new releases

### Token errors
- Verify secrets are set correctly in GitHub repository settings
- Check token hasn't expired
- Ensure token has correct permissions

## 💡 Tips

1. **Test before publishing:** Always test packages locally before tagging
2. **Semantic versioning:** Follow semver (MAJOR.MINOR.PATCH)
3. **CHANGELOG:** Keep it updated for each release
4. **Pre-releases:** Use tags like `v0.1.0-beta.1` for testing
5. **Rollback:** If needed, yank bad versions:
   ```bash
   cargo yank --version X.Y.Z  # Rust
   pip uninstall package        # Can't un-publish Python
   npm unpublish pkg@version    # npm (within 72 hours)
   ```

## 🎉 Your Workflow is Ready!

Everything is set up! Just:
1. Add the three secrets to GitHub
2. Update versions
3. Push a tag
4. Watch the magic happen! ✨
