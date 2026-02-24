#!/usr/bin/env python3
"""
Railway Deployment Debug Script
Run this to check if everything is ready for deployment
"""
import os
import sys

def check_environment():
    print("=" * 60)
    print("🔍 Railway Deployment Check")
    print("=" * 60)
    
    # Check Python version
    print(f"\n✓ Python Version: {sys.version}")
    
    # Check environment variables
    print(f"\n📍 Environment Variables:")
    print(f"  PORT: {os.getenv('PORT', 'Not set (will use 8000)')}")
    print(f"  ENV: {os.getenv('ENV', 'development')}")
    
    # Check required files
    print(f"\n📁 Required Files:")
    required_files = [
        'app.py',
        'config.py',
        'requirements.txt',
        'Dockerfile',
        'nixpacks.toml',
        'Procfile'
    ]
    
    for file in required_files:
        exists = "✓" if os.path.exists(file) else "✗"
        print(f"  {exists} {file}")
    
    # Check models directory
    print(f"\n🤖 Models Directory:")
    if os.path.exists('models'):
        model_files = os.listdir('models')
        for file in model_files:
            print(f"  ✓ models/{file}")
    else:
        print("  ✗ models/ directory not found")
    
    # Try importing main modules
    print(f"\n📦 Module Imports:")
    try:
        import fastapi
        print(f"  ✓ fastapi {fastapi.__version__}")
    except ImportError as e:
        print(f"  ✗ fastapi: {e}")
    
    try:
        import uvicorn
        print(f"  ✓ uvicorn")
    except ImportError as e:
        print(f"  ✗ uvicorn: {e}")
    
    try:
        import xgboost
        print(f"  ✓ xgboost {xgboost.__version__}")
    except ImportError as e:
        print(f"  ✗ xgboost: {e}")
    
    # Try loading config
    print(f"\n⚙️  Configuration:")
    try:
        import config
        print(f"  ✓ API_HOST: {config.API_HOST}")
        print(f"  ✓ API_PORT: {config.API_PORT}")
        print(f"  ✓ ENV: {config.ENV}")
    except Exception as e:
        print(f"  ✗ Error loading config: {e}")
    
    print("\n" + "=" * 60)
    print("✓ Check complete!")
    print("=" * 60)

if __name__ == "__main__":
    check_environment()
