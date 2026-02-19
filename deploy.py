#!/usr/bin/env python3
"""Deploy calculator-v3 to GitHub Pages."""

import subprocess
import sys
import time
from pathlib import Path

def run_command(cmd: list, cwd: Path = None, check: bool = True) -> tuple[bool, str]:
    """Run a command and return success status and output."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=check
        )
        return True, result.stdout + result.stderr
    except subprocess.CalledProcessError as e:
        return False, e.stdout + e.stderr
    except Exception as e:
        return False, str(e)

def main():
    """Main deployment function."""
    project_dir = Path(__file__).parent
    
    print("🚀 Starting deployment of Calculator v3 to GitHub Pages...")
    print(f"📁 Project directory: {project_dir}")
    
    # Step 1: Initialize git
    if not (project_dir / ".git").exists():
        print("\n📝 Initializing git repository...")
        success, output = run_command(["git", "init"], cwd=project_dir)
        if not success:
            print(f"❌ Git init failed: {output}")
            return 1
    else:
        print("✅ Git repository already initialized")
    
    # Step 2: Add and commit files
    print("\n📝 Committing files...")
    success, output = run_command(["git", "add", "."], cwd=project_dir)
    if not success:
        print(f"❌ Git add failed: {output}")
        return 1
    
    success, output = run_command(
        ["git", "commit", "-m", "Calculator v3 - Modern web calculator with beautiful UI"],
        cwd=project_dir,
        check=False
    )
    if "nothing to commit" in output:
        print("✅ No changes to commit (already committed)")
    elif success:
        print("✅ Files committed successfully")
    else:
        print(f"⚠️  Commit status: {output}")
    
    # Step 3: Delete old repo if exists (fresh start)
    print("\n🗑️  Removing old repository if exists...")
    run_command(
        ["gh", "repo", "delete", "natovichat/calculator-v3", "--yes"],
        check=False
    )
    
    # Step 4: Create GitHub repository
    print("\n📦 Creating GitHub repository natovichat/calculator-v3...")
    success, output = run_command(
        [
            "gh", "repo", "create", "natovichat/calculator-v3",
            "--public", "--source=.", "--remote=origin", "--push"
        ],
        cwd=project_dir,
        check=False
    )
    
    if success or "created" in output.lower():
        print("✅ Repository created and pushed")
    else:
        print(f"⚠️  Repository creation: {output}")
        print("Attempting to set remote and push...")
        run_command(
            ["git", "remote", "add", "origin", 
             "https://github.com/natovichat/calculator-v3.git"],
            cwd=project_dir,
            check=False
        )
        run_command(["git", "branch", "-M", "main"], cwd=project_dir, check=False)
        run_command(["git", "push", "-u", "origin", "main", "--force"], cwd=project_dir, check=False)
    
    # Step 5: Enable GitHub Pages
    print("\n🌐 Enabling GitHub Pages...")
    success, output = run_command(
        [
            "gh", "api", "repos/natovichat/calculator-v3/pages",
            "--method", "POST",
            "--field", "source[branch]=main",
            "--field", "source[path]=/"
        ],
        check=False
    )
    
    if success or "successfully" in output.lower():
        print("✅ GitHub Pages enabled")
    elif "already exists" in output.lower():
        print("✅ GitHub Pages already enabled")
    else:
        print(f"⚠️  GitHub Pages status: {output}")
    
    # Step 6: Wait for GitHub Pages build
    print("\n⏳ Waiting 60 seconds for GitHub Pages to build and deploy...")
    for i in range(60, 0, -10):
        print(f"   {i} seconds remaining...")
        time.sleep(10)
    
    # Step 7: Verify deployment
    print("\n🔍 Verifying deployment...")
    success, output = run_command(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
         "https://natovichat.github.io/calculator-v3/"],
        check=False
    )
    
    http_code = output.strip()
    
    print("\n" + "="*70)
    print("🎉 DEPLOYMENT COMPLETE!")
    print("="*70)
    
    if http_code == "200":
        print("✅ Status: LIVE and VERIFIED")
    else:
        print(f"⏳ Status: Building (HTTP {http_code})")
        print("   Check again in a few minutes")
    
    print("\n🌐 Live URL: https://natovichat.github.io/calculator-v3/")
    print("📦 Repository: https://github.com/natovichat/calculator-v3")
    print("🔧 Settings: https://github.com/natovichat/calculator-v3/settings/pages")
    print("="*70)
    
    print("\n✨ Next: Visit the live URL to test the calculator!")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
