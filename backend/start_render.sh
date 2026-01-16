#!/bin/bash
# Render startup script with extended timeout

echo "Starting Nexus AI Backend on Render..."
echo "Note: First request will take 2-3 minutes for model loading"

# Start uvicorn with extended timeouts for Render
uvicorn app.main:app \
  --host 0.0.0.0 \
  --port ${PORT:-8000} \
  --timeout-keep-alive 300 \
  --timeout-graceful-shutdown 30
