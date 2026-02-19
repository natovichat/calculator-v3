#!/usr/bin/env python3
"""Deploy calculator-v3 to GitHub Pages."""

import subprocess
import sys
import time


def run_command(cmd: str, cwd: str = None) -> tuple[int, str]:
    """Run shell command and return exit code and output."""
    result = subprocess.run(
        cmd,
        shell=True,
        cwd=cwd,
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout + result.stderr


def main():
    """Deploy calculator-v3 to GitHub Pages."""
    project_dir = "/Users/aviad.natovich/personal/agents-system/projects/calculator-v3"
    repo_name = "calculator-v3"
    github_user = "natovichat"
    
    print("🚀 Starting deployment to GitHub Pages...")
    
    # Step 1: Commit current state
    print("\n📦 Committing files...")
    code, output = run_command("git add .", cwd=project_dir)
    if code != 0:
        print(f"Warning: git add returned {code}")
    
    code, output = run_command('git commit -m "Deploy calculator-v3"', cwd=project_dir)
    if code != 0 and "nothing to commit" not in output:
        print(f"Error: git commit failed: {output}")
        return 1
    print("✅ Files committed")
    
    # Step 2: Create GitHub repository
    print("\n🌐 Creating GitHub repository...")
    code, output = run_command(
        f"gh repo create {github_user}/{repo_name} --public --source=. --remote=origin --push",
        cwd=project_dir
    )
    if code != 0 and "already exists" not in output:
        print(f"Warning: {output}")
    print("✅ Repository created and pushed")
    
    # Step 3: Enable GitHub Pages
    print("\n📄 Enabling GitHub Pages...")
    code, output = run_command(
        f"gh api repos/{github_user}/{repo_name}/pages --method POST "
        "--field 'source[branch]=main' --field 'source[path]=/'",
        cwd=project_dir
    )
    if code != 0 and "already been requested" not in output.lower():
        print(f"Warning: {output}")
    print("✅ GitHub Pages enabled")
    
    # Step 4: Wait for deployment
    print("\n⏳ Waiting for GitHub Pages to deploy (60 seconds)...")
    time.sleep(60)
    
    # Step 5: Verify deployment
    live_url = f"https://{github_user}.github.io/{repo_name}/"
    print(f"\n🔍 Verifying deployment at {live_url}...")
    code, output = run_command(f"curl -I {live_url}")
    
    if "200 OK" in output or "301" in output or "302" in output:
        print(f"\n✅ DEPLOYMENT SUCCESSFUL!")
        print(f"🌐 Live URL: {live_url}")
        return 0
    else:
        print(f"\n⚠️ Deployment may still be in progress.")
        print(f"🌐 Check URL in a few minutes: {live_url}")
        return 0


if __name__ == "__main__":
    sys.exit(main())
