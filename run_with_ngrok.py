from pyngrok import ngrok
import os
import subprocess
import sys
import atexit

# Start Flask app in background
print("Starting the Flask application...")
flask_process = subprocess.Popen(
    [sys.executable, "-c", "from app.main import flask_app; flask_app.run(host='0.0.0.0', port=5000)"],
    stdout=subprocess.PIPE
)

# Register cleanup function
def cleanup():
    print("Shutting down the application...")
    flask_process.terminate()
    for tunnel in ngrok.get_tunnels():
        ngrok.disconnect(tunnel.public_url)

atexit.register(cleanup)

# Start ngrok tunnel
print("Starting ngrok tunnel...")
public_url = ngrok.connect(5000).public_url
print(f"Your application is publicly available at: {public_url}")

# Keep the script running
try:
    while True:
        # Display some output from the Flask process
        output = flask_process.stdout.readline()
        if output:
            print(output.decode().strip())
except KeyboardInterrupt:
    print("Shutting down...") 