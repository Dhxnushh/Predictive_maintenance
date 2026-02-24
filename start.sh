#!/bin/sh
# Startup script for Railway/Heroku/Render

# Get PORT from environment or use default
PORT=${PORT:-8000}

echo "========================================="
echo "  Predictive Maintenance API"
echo "  Port: $PORT"
echo "========================================="

# Start uvicorn
exec uvicorn app:app --host 0.0.0.0 --port "$PORT" --log-level info
