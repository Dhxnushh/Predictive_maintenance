#!/usr/bin/env python3
"""
Entrypoint for production deployment
Handles PORT environment variable properly
"""
import os
import sys

def main():
    # Get port from environment or use default
    port = int(os.getenv('PORT', 8000))
    host = os.getenv('HOST', '0.0.0.0')
    
    print("=" * 50)
    print("🚀 Starting Predictive Maintenance API")
    print("=" * 50)
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"Environment: {os.getenv('ENV', 'production')}")
    print("=" * 50)
    
    # Import and run
    try:
        import uvicorn
        from app import app
        
        uvicorn.run(
            app,
            host=host,
            port=port,
            log_level="info",
            access_log=True
        )
    except Exception as e:
        print(f"❌ Failed to start: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
