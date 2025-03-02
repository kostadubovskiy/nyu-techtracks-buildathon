#!/bin/bash

# Kill any existing processes on ports 5000 and 8000
echo "Checking for existing processes on ports 5000 and 8000..."
lsof -ti:5000 | xargs kill -9 2>/dev/null || true
lsof -ti:8000 | xargs kill -9 2>/dev/null || true

# Start FastAPI with Uvicorn in the background
echo "Starting FastAPI server on port 8000..."
uvicorn asgi:app --host 0.0.0.0 --port 8000 &
FASTAPI_PID=$!

# Start Flask with Gunicorn in the background
echo "Starting Flask server on port 5000..."
gunicorn --bind 0.0.0.0:5000 wsgi:flask_app &
FLASK_PID=$!

echo "Servers started! Press Ctrl+C to stop both servers."
echo "FastAPI server running at: http://localhost:8000"
echo "Flask server running at: http://localhost:5000"

# Handle termination
trap "echo 'Shutting down servers...'; kill $FASTAPI_PID $FLASK_PID; exit" INT TERM
wait 