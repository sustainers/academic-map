#!/bin/bash

# Local build and deploy script
# Note: For production deploys, the GitHub Action in .github/workflows/deploy-book.yml is used
# This script is for manual local deployments only

# Make sure you run `chmod +x scripts/build.sh` before attempting to run it.

set -e  # Exit on any error

BUILD_DIR="./_build/html"

echo "Running lint checks..."
npm run lint

echo "Running link checks..."
npm run links-ci

echo "Checking TOC completeness..."
npm run check-toc

echo "Building Jupyter book..."
jupyter-book build --all .

echo "Deploying to gh-pages branch..."
ghp-import -n -p -f "$BUILD_DIR"

echo "Build and deploy completed successfully!"
