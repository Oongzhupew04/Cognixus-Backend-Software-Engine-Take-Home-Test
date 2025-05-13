import os
import subprocess
import time
import requests

NGROK_AUTHTOKEN = "2x014ZpW1aAm1enxcLunUlHeLoy_6SY5Pe73o5keLWFDSbAVg"  # Use environment variable for security
NGROK_PORT = 5000  # The port your Flask app is running on

def start_ngrok():
    print("Starting Ngrok...")

    # Set the Ngrok authtoken (only needed once)
    if NGROK_AUTHTOKEN:
        subprocess.run(["ngrok", "config", "add-authtoken", NGROK_AUTHTOKEN], check=True)
    else:
        print("Ngrok Authtoken not found. Please set NGROK_AUTHTOKEN environment variable.")
        return None

    # Start Ngrok with HTTP (HTTPS is auto-provided by Ngrok)
    ngrok_process = subprocess.Popen(["ngrok", "http", str(NGROK_PORT)], stdout=subprocess.PIPE)
    time.sleep(5)  # Give it some time to start

    # Debug: Print Ngrok API Response
    try:
        response = requests.get("http://localhost:4040/api/tunnels")
        print(f"Ngrok API Response: {response.text}")  # Debug line
        response.raise_for_status()
        tunnels = response.json().get("tunnels")
        if tunnels:
            for tunnel in tunnels:
                print(f"Tunnel Found: {tunnel}")  # Debug line
                if tunnel.get("public_url").startswith("https"):
                    public_url = tunnel.get("public_url")
                    print(f"Ngrok Public HTTPS URL: {public_url}")
                    return public_url
            print("No HTTPS Ngrok tunnel found.")
        else:
            print("No Ngrok tunnels found.")
    except requests.RequestException as e:
        print(f"Error getting Ngrok URL: {e}")
    
    return None

if __name__ == "__main__":
    print("Starting Flask Server and Ngrok...")
    
    # Start Flask in a separate process (no shell=True for safety)
    flask_process = subprocess.Popen(["flask", "run", "--host=0.0.0.0", "--port=5000"])

    # Start Ngrok
    ngrok_url = start_ngrok()
    
    if ngrok_url:
        print(f"Use this HTTPS URL for OAuth Providers: {ngrok_url}")
    else:
        print("Ngrok failed to start.")

    try:
        # Keep the Flask process running
        flask_process.wait()
    except KeyboardInterrupt:
        print("\nShutting down Flask and Ngrok...")
        flask_process.terminate()
        ngrok_process.terminate()
