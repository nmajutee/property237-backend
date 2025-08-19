import subprocess
import time
import signal
import os

def test_endpoints():
    """Test API endpoints using curl"""
    base_url = "http://127.0.0.1:8000"

    endpoints = [
        "/api/users/",
        "/api/properties/",
        "/admin/",
    ]

    for endpoint in endpoints:
        try:
            print(f"Testing {endpoint}...")
            # Use curl with timeout
            result = subprocess.run([
                'curl', '-s', '-o', '/dev/null', '-w', '%{http_code}',
                '--max-time', '5', f"{base_url}{endpoint}"
            ], capture_output=True, text=True, timeout=6)

            if result.returncode == 0:
                status_code = result.stdout.strip()
                print(f"✓ {endpoint} - Status: {status_code}")
            else:
                print(f"✗ {endpoint} - Failed to connect")

        except subprocess.TimeoutExpired:
            print(f"✗ {endpoint} - TIMEOUT (infinite loop detected)")
        except Exception as e:
            print(f"✗ {endpoint} - Error: {e}")

def check_server_running():
    """Check if Django server is running"""
    try:
        result = subprocess.run(['curl', '-s', 'http://127.0.0.1:8000/', '--max-time', '2'],
                              capture_output=True, timeout=3)
        return True
    except:
        return False

if __name__ == "__main__":
    if not check_server_running():
        print("Django server is not running. Start it with: python manage.py runserver")
    else:
        test_endpoints()