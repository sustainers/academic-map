#!/bin/bash

# Local check and build script
# Deploys only happen through the GitHub Action in .github/workflows/deploy-book.yml,
# which publishes to curioss.org/academic-map. To deploy without pushing to main,
# run that workflow by hand from the repository's Actions tab.

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

echo "Build completed successfully! Open $BUILD_DIR/index.html to view it."
