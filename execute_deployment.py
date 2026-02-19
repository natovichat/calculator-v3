#!/usr/bin/env python3
"""Execute the deployment script for Calculator v3"""

import subprocess
import sys
import os

def main():
    # Change to calculator-v3 directory
    os.chdir('/Users/aviad.natovich/personal/agents-system/projects/calculator-v3')
    
    print("🚀 Starting Calculator v3 deployment...")
    print("=" * 60)
    
    # Make script executable
    subprocess.run(['chmod', '+x', 'deploy_v3_now.sh'], check=True)
    
    # Execute the deployment script
    result = subprocess.run(['./deploy_v3_now.sh'], 
                          capture_output=False, 
                          text=True)
    
    if result.returncode == 0:
        print("\n✅ Deployment script completed successfully!")
        print("\n🌐 Calculator v3 should be live at:")
        print("   https://natovichat.github.io/calculator-v3/")
        return 0
    else:
        print(f"\n❌ Deployment script failed with exit code {result.returncode}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
