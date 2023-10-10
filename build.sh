#!/bin/bash

# Note: Make sure you run `chmod a+x` on this script before attempting to run it.

# Set the directory where the Jupyter book is built
BUILD_DIR="./_build/html"

# Function to display an error message and exit
error_exit() {
    echo "$1" >&2  # Display error message to stderr
    exit "${2:-1}" # Exit with passed in status or default to 1
}

# Ensure we're in a git repository
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    error_exit "Not inside a Git repository."
fi

# Switch to the main branch
git checkout main || error_exit "Failed to switch to main branch."

# Build the Jupyter book
jupyter-book build --all . || error_exit "Failed to build Jupyter book."

# Ensure the build directory exists
if [[ ! -d "$BUILD_DIR" ]]; then
    error_exit "Build directory does not exist: $BUILD_DIR"
fi

# Import the book and push to the gh-pages branch
ghp-import -n -p -f "$BUILD_DIR" || error_exit "Failed to import and push to gh-pages."

echo "Build script completed successfully!"
