#!/bin/bash

echo "Deploying Calculator v3 to GitHub Pages..."

# Navigate to project directory
cd "$(dirname "$0")"

# Delete existing repo if it exists
echo "Cleaning up old repository..."
gh repo delete natovichat/calculator-v3 --yes 2>/dev/null || echo "No existing repo to delete"

# Initialize git if needed
if [ ! -d .git ]; then
    git init
fi

# Add only the necessary files
git add index.html style.css script.js README.md 2>/dev/null || true

# Commit
git add -A
git commit -m "Deploy Calculator v3 web app" 2>/dev/null || echo "Nothing new to commit"

# Create GitHub repository and push
echo "Creating GitHub repository..."
gh repo create natovichat/calculator-v3 --public --source=. --remote=origin --push

# Enable GitHub Pages
echo "Enabling GitHub Pages..."
gh api repos/natovichat/calculator-v3/pages --method POST \
  --field 'source[branch]=main' --field 'source[path]=/' 2>/dev/null || \
gh api repos/natovichat/calculator-v3/pages --method POST \
  --field 'source[branch]=master' --field 'source[path]=/'

echo "Waiting for GitHub Pages to deploy (60 seconds)..."
sleep 60

# Check deployment status
echo "Checking deployment..."
STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://natovichat.github.io/calculator-v3/)
echo "HTTP Status: $STATUS"

if [ "$STATUS" = "200" ]; then
    echo "✅ Deployment successful!"
    echo "🌐 Live URL: https://natovichat.github.io/calculator-v3/"
else
    echo "⚠️  Deployment pending... Status: $STATUS"
    echo "URL will be available at: https://natovichat.github.io/calculator-v3/"
fi
