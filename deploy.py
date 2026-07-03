#!/usr/bin/env python3
"""
Quick Vercel deployment script for rikka-github-stats
"""
import subprocess
import os
import sys

def run(cmd, shell=True):
    """Run command and return output"""
    result = subprocess.run(cmd, shell=shell, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return None
    return result.stdout.strip()

def main():
    vercel_token = os.getenv('VERCEL_TOKEN')
    if not vercel_token:
        print("Error: VERCEL_TOKEN env var not set")
        print("Usage: VERCEL_TOKEN=xxx python3 deploy.py")
        sys.exit(1)
    
    print("🚀 Deploying rikka-github-stats to Vercel...")
    print()
    
    # Install Vercel CLI
    print("📦 Installing Vercel CLI...")
    run("npm install -g vercel")
    
    # Deploy
    print("🌐 Deploying...")
    result = run(f"vercel --prod --token {vercel_token} --yes 2>&1")
    
    if result and "vercel.app" in result:
        # Extract URL
        for line in result.split('\n'):
            if 'vercel.app' in line:
                url = line.strip()
                print()
                print("✅ Deployment successful!")
                print(f"📍 URL: {url}")
                print()
                print("🎨 Add to your GitHub profile README:")
                print(f"![Rikka GitHub Stats]({url}/api/stats?username=rikka0x)")
                return
    
    print(result)
    print("⚠️ Deployment may have issues. Check Vercel dashboard.")

if __name__ == "__main__":
    main()
