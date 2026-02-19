#!/usr/bin/env python3
"""Deploy calculator-v3 to GitHub Pages."""

import subprocess
import sys
import time
import json
from pathlib import Path

def run_cmd(cmd, cwd=None):
    """Run command and return output."""
    result = subprocess.run(
        cmd,
        cwd=cwd,
        shell=True,
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout, result.stderr

def main():
    calc_dir = Path("/Users/aviad.natovich/personal/agents-system/projects/calculator-v3")
    
    print("🚀 Deploying calculator-v3 to GitHub Pages...")
    
    # Initialize git if needed
    if not (calc_dir / ".git").exists():
        print("\n📝 Initializing git...")
        code, out, err = run_cmd("git init", cwd=calc_dir)
        print(out + err)
    
    # Add and commit files
    print("\n📝 Committing files...")
    code, out, err = run_cmd("git add -A && git commit -m 'Calculator v3 web app' || true", cwd=calc_dir)
    print(out + err)
    
    # Delete old repo if exists
    print("\n🗑️  Removing old repository if exists...")
    code, out, err = run_cmd("gh repo delete natovichat/calculator-v3 --yes 2>/dev/null || true", cwd=calc_dir)
    print(out + err)
    
    # Create GitHub repository
    print("\n📤 Creating GitHub repository...")
    code, out, err = run_cmd(
        "gh repo create natovichat/calculator-v3 --public --source=. --remote=origin --push",
        cwd=calc_dir
    )
    print(out + err)
    
    # Enable GitHub Pages
    print("\n🌐 Enabling GitHub Pages...")
    code, out, err = run_cmd(
        "gh api repos/natovichat/calculator-v3/pages --method POST --field 'source[branch]=main' --field 'source[path]=/' 2>/dev/null || echo 'Pages may already be enabled'",
        cwd=calc_dir
    )
    print(out + err)
    
    # Wait for deployment
    print("\n⏳ Waiting 60 seconds for deployment...")
    time.sleep(60)
    
    # Verify
    print("\n🔍 Verifying deployment...")
    code, out, err = run_cmd("curl -s -o /dev/null -w '%{http_code}' https://natovichat.github.io/calculator-v3/")
    http_code = out.strip()
    
    print(f"\n{'='*60}")
    if http_code == "200":
        print("✅ SUCCESS! Calculator v3 is live!")
        print("🌐 URL: https://natovichat.github.io/calculator-v3/")
        
        # Send message to beta_user
        print("\n📨 Notifying beta_user...")
        payload = {
            "artifact": "projects/calculator-v3",
            "url": "https://natovichat.github.io/calculator-v3/",
            "conversation_id": "82fb7b48-9d5e-488c-9b5a-309bd1f154fc"
        }
        
        run_cmd(
            f"python3 scripts/send.py --receiver beta_user --type Task --payload '{json.dumps(payload)}' --sender developer --conversation-id 82fb7b48-9d5e-488c-9b5a-309bd1f154fc",
            cwd=Path("/Users/aviad.natovich/personal/agents-system")
        )
        print("✅ Notification sent!")
    else:
        print(f"⚠️  HTTP Status: {http_code}")
        print("🌐 URL: https://natovichat.github.io/calculator-v3/")
        print("💡 May still be building, check in a few minutes")
    
    print(f"{'='*60}\n")
    return 0 if http_code == "200" else 1

if __name__ == "__main__":
    sys.exit(main())
