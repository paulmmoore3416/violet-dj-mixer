#!/bin/bash
# Violet DJ Mixer - Automated GitHub Push Script
# This script handles everything needed to push your project to GitHub

set -e

echo "=========================================="
echo "🎛️  Violet DJ Mixer - GitHub Push"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if GitHub username is provided
if [ -z "$1" ]; then
    echo -e "${RED}Error: GitHub username required${NC}"
    echo "Usage: bash push-to-github.sh YOUR_GITHUB_USERNAME"
    exit 1
fi

GITHUB_USER="$1"
REPO_NAME="violet-dj-mixer"
REPO_URL="https://github.com/${GITHUB_USER}/${REPO_NAME}.git"

echo -e "${YELLOW}Configuration:${NC}"
echo "GitHub User: $GITHUB_USER"
echo "Repository: $REPO_NAME"
echo "URL: $REPO_URL"
echo ""

# Step 1: Check git status
echo -e "${YELLOW}Step 1: Checking git status...${NC}"
if [ -z "$(git status --short)" ]; then
    echo -e "${GREEN}✓ Working tree clean${NC}"
else
    echo -e "${RED}✗ Uncommitted changes detected${NC}"
    git status
    exit 1
fi
echo ""

# Step 2: Check if remote exists
echo -e "${YELLOW}Step 2: Setting up remote...${NC}"
if git remote get-url origin 2>/dev/null | grep -q "violet-dj-mixer"; then
    echo -e "${GREEN}✓ Remote already configured${NC}"
else
    echo "Adding remote origin..."
    git remote add origin "$REPO_URL"
    echo -e "${GREEN}✓ Remote added${NC}"
fi
echo ""

# Step 3: Rename branch to main
echo -e "${YELLOW}Step 3: Preparing branch...${NC}"
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT_BRANCH" = "master" ]; then
    echo "Renaming branch master → main..."
    git branch -m master main
    echo -e "${GREEN}✓ Branch renamed${NC}"
elif [ "$CURRENT_BRANCH" = "main" ]; then
    echo -e "${GREEN}✓ Already on main branch${NC}"
fi
echo ""

# Step 4: Push to GitHub
echo -e "${YELLOW}Step 4: Pushing to GitHub...${NC}"
echo "Command: git push -u origin main"
echo "Note: You may be prompted for credentials. Use your Personal Access Token as password."
echo ""

if git push -u origin main; then
    echo ""
    echo -e "${GREEN}✓ Successfully pushed to GitHub!${NC}"
else
    echo ""
    echo -e "${RED}✗ Push failed${NC}"
    echo "Possible solutions:"
    echo "1. Check internet connection"
    echo "2. Verify GitHub username is correct"
    echo "3. Ensure Personal Access Token has repo access"
    echo "4. Check that the repository doesn't exist on GitHub yet"
    exit 1
fi

echo ""
echo "=========================================="
echo -e "${GREEN}Next Steps:${NC}"
echo "=========================================="
echo "1. Go to: https://github.com/${GITHUB_USER}/${REPO_NAME}"
echo "2. Go to Settings → Pages"
echo "3. Enable GitHub Pages (Branch: main, Folder: /)"
echo "4. Your site will be at:"
echo "   https://${GITHUB_USER}.github.io/${REPO_NAME}/"
echo ""
echo "5. (Optional) Build and release .deb package:"
echo "   bash scripts/build-deb.sh"
echo ""
echo "=========================================="
echo -e "${GREEN}✓ All done! Violet DJ Mixer is on GitHub!${NC}"
echo "=========================================="
