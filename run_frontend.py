#!/usr/bin/env python3
"""
Simple script to run the Chainlit frontend for the ACTIVA Code Generation Agent.
"""

import subprocess
import sys
import os

def main():
    """Run the Chainlit frontend"""
    print("🎬 Starting ACTIVA Code Generation Agent Frontend...")
    print("=" * 50)
    
    # Check if chainlit is installed
    try:
        import chainlit
        print("✅ Chainlit is installed")
    except ImportError:
        print("❌ Chainlit not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "chainlit>=1.0.0"])
        print("✅ Chainlit installed successfully")
    
    # Run the frontend
    print("\n🚀 Starting the frontend...")
    print("The app will open in your browser at http://localhost:8000")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        subprocess.run([
            sys.executable, "-m", "chainlit", "run", "frontend.py", 
            "--port", "8000", "--host", "0.0.0.0"
        ])
    except KeyboardInterrupt:
        print("\n👋 Frontend stopped. Goodbye!")

if __name__ == "__main__":
    main() 