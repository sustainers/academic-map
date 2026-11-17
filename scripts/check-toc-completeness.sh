#!/bin/bash

# Check if all markdown files are included in _toc.yml and vice versa
# Also checks if index.md files are up to date

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ERRORS=0

# Files to ignore (intentionally not in TOC)
IGNORE_FILES=(
    "organizations/example.md"
)

echo "Checking TOC completeness..."
echo ""

# Directories to check
DIRS=("universities" "organizations" "research-institutions" "service-providers")

for DIR in "${DIRS[@]}"; do
    echo "=== Checking $DIR ==="
    
    # Get all markdown files except index.md
    FILES=($(find "$DIR" -maxdepth 1 -name "*.md" ! -name "index.md" -type f | sort))
    
    # Extract entries from _toc.yml for this directory
    TOC_ENTRIES=($(grep -A 1000 "file: $DIR/index.md" _toc.yml | grep "  - file: $DIR/" | sed "s/.*file: //" | sed "s/\.md//" | sort))
    
    # Convert FILES to just the relative paths without extension
    FILE_PATHS=()
    for file in "${FILES[@]}"; do
        FILE_PATHS+=("${file%.md}")
    done
    
    # Check for files not in TOC
    echo "Files not in _toc.yml:"
    FOUND_MISSING=false
    for file in "${FILE_PATHS[@]}"; do
        # Skip ignored files
        if [[ " ${IGNORE_FILES[@]} " =~ " ${file}.md " ]]; then
            continue
        fi
        if [[ ! " ${TOC_ENTRIES[@]} " =~ " ${file} " ]]; then
            echo -e "  ${RED}✗${NC} $file.md"
            FOUND_MISSING=true
            ERRORS=$((ERRORS + 1))
        fi
    done
    if [ "$FOUND_MISSING" = false ]; then
        echo -e "  ${GREEN}✓${NC} All files are in _toc.yml"
    fi
    
    # Check for TOC entries not in files
    echo "TOC entries without files:"
    FOUND_MISSING=false
    for entry in "${TOC_ENTRIES[@]}"; do
        if [[ ! " ${FILE_PATHS[@]} " =~ " ${entry} " ]]; then
            echo -e "  ${RED}✗${NC} $entry.md"
            FOUND_MISSING=true
            ERRORS=$((ERRORS + 1))
        fi
    done
    if [ "$FOUND_MISSING" = false ]; then
        echo -e "  ${GREEN}✓${NC} All TOC entries have files"
    fi
    
    # Check if index.md lists all files
    if [ -f "$DIR/index.md" ]; then
        echo "Checking $DIR/index.md references:"
        FOUND_MISSING=false
        for file in "${FILE_PATHS[@]}"; do
            # Path relative to the folder, e.g. "apereo" or "nsf-grants/pose"
            relpath="${file#$DIR/}"
            # Skip ignored files
            if [[ " ${IGNORE_FILES[@]} " =~ " ${file}.md " ]]; then
                continue
            fi
            # Check that index.md links the file itself, not just mentions its name
            # (e.g. "apereo" also appears in the URL www.apereo.org)
            if ! grep -qF "(./$relpath.md)" "$DIR/index.md" && ! grep -qF "($relpath.md)" "$DIR/index.md"; then
                echo -e "  ${RED}✗${NC} $relpath.md not linked from $DIR/index.md"
                FOUND_MISSING=true
                ERRORS=$((ERRORS + 1))
            fi
        done
        if [ "$FOUND_MISSING" = false ]; then
            echo -e "  ${GREEN}✓${NC} All files mentioned in index.md"
        fi
    fi
    
    echo ""
done

# Organizations whose page keeps a member list, as "Link text:page".
# Any entry whose "Member of" line links [Link text] must be linked from that page.
MEMBERSHIP_LISTS=(
    "CURIOSS:organizations/curioss.md"
)

for PAIR in "${MEMBERSHIP_LISTS[@]}"; do
    ORG="${PAIR%%:*}"
    ORG_PAGE="${PAIR#*:}"
    echo "=== Checking $ORG members in $ORG_PAGE ==="
    FOUND_MISSING=false
    for DIR in "${DIRS[@]}"; do
        for file in $(find "$DIR" -maxdepth 1 -name "*.md" ! -name "index.md" -type f | sort); do
            if [[ " ${IGNORE_FILES[@]} " =~ " ${file} " ]]; then
                continue
            fi
            # Matches both "*Member of*:" and "*Member* of:"
            if grep -qiE "^- \*member(\*)? of(\*)?:.*\[$ORG\]" "$file"; then
                if ! grep -qF "$(basename "$file")" "$ORG_PAGE"; then
                    echo -e "  ${RED}✗${NC} $file says it is a member of $ORG but is not listed in $ORG_PAGE"
                    FOUND_MISSING=true
                    ERRORS=$((ERRORS + 1))
                fi
            fi
        done
    done
    if [ "$FOUND_MISSING" = false ]; then
        echo -e "  ${GREEN}✓${NC} All $ORG members are listed"
    fi
    echo ""
done

if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed!${NC}"
    exit 0
else
    echo -e "${RED}✗ Found $ERRORS error(s)${NC}"
    exit 1
fi
