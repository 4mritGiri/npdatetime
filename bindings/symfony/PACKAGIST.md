# Publishing to Packagist

This guide explains how to publish the `4mritgiri/npdatetime-bundle` to Packagist.

## Prerequisites

1. A GitHub account
2. A Packagist account (https://packagist.org)
3. The bundle pushed to GitHub repository

## One-Time Setup

### 1. Register on Packagist

1. Go to https://packagist.org
2. Sign in with your GitHub account
3. Click "Submit" in the top navigation

### 2. Submit Your Package

1. Enter your GitHub repository URL: `https://github.com/4mritGiri/npdatetime`
2. Click "Check"
3. Packagist will detect the `bindings/symfony/composer.json`
4. Click "Submit"

### 3. Configure GitHub Webhook (Automatic Updates)

Packagist will show you a webhook URL. To configure automatic updates:

1. Go to your GitHub repository settings
2. Navigate to "Webhooks"
3. Click "Add webhook"
4. Paste the Packagist webhook URL
5. Set Content type to `application/json`
6. Select "Just the push event"
7. Click "Add webhook"

## How It Works

- **Automatic Updates**: When you push a new git tag (e.g., `v0.2.2`), GitHub notifies Packagist
- **Version Detection**: Packagist reads your `composer.json` and git tags
- **No Manual Publishing**: Unlike PyPI/npm, no GitHub Actions workflow needed!

## Publishing a New Version

1. Update version in files (if needed)
2. Commit changes
3. Create and push a git tag:
   ```bash
   git tag v0.2.2
   git push origin v0.2.2
   ```
4. Packagist automatically detects the new version (within minutes)

## Manual Update

If automatic webhook isn't configured, you can manually trigger updates:

1. Go to https://packagist.org/packages/4mritgiri/npdatetime-bundle
2. Click "Update" button

## Installation for Users

Once published, users install via Composer:

```bash
composer require 4mritgiri/npdatetime-bundle
```

## Notes

- **Package Name**: Must match `name` in `composer.json` (`4mritgiri/npdatetime-bundle`)
- **Type**: Set to `symfony-bundle` for proper Flex integration
- **Minimum Stability**: Packagist respects semver tags (v1.0.0, v0.2.2, etc.)
- **No Tokens Required**: Packagist pulls from public GitHub - no authentication needed
