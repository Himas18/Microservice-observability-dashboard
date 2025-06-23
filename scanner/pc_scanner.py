import psutil
import requests
import yaml
import os
import argparse
import time


API_URL = "http://backend:8059/status" if os.environ.get("DOCKERIZED") else "http://localhost:8059/status"

def wait_for_backend(url, retries=10, delay=3):
    for i in range(retries):
        try:
            # Ping the health endpoint, not /status directly
            response = requests.get(url.replace("/status", "/health"))
            if response.status_code == 200:
                print("✅ Backend is ready.")
                return
        except Exception:
            print(f"⏳ Waiting for backend... ({i+1}/{retries})")
        time.sleep(delay)
    print("❌ Backend not reachable after retries.")
    exit(1)

def load_filters(yaml_path="filters.yaml"):
    if not os.path.exists(yaml_path):
        print("⚠️ filters.yaml not found. Using empty filters.")
        return {"include": [], "exclude": []}
    with open(yaml_path, "r") as f:
        return yaml.safe_load(f)

def is_relevant(name, include, exclude):
    name = name.lower()
    return any(key.lower() in name for key in include) and not any(key.lower() in name for key in exclude)

def scan_and_send(verbose=False):
    filters = load_filters()
    include = filters.get("include", [])
    exclude = filters.get("exclude", [])

    print("🔍 Scanning processes...")
    found_any = False

    for proc in psutil.process_iter(attrs=["name"]):
        try:
            name = proc.info["name"]
            found_any = True

            if not is_relevant(name, include, exclude):
                continue

            response = requests.post(API_URL, json={
                "name": name,
                "status": "up",
                "dependencies": []
            })
            if verbose:
                print(f"[✓] Sent: {name} → {response.status_code}")
        except Exception as e:
            if verbose:
                print(f"[!] Error with {proc.info.get('name', 'unknown')}: {e}")

    if not found_any:
        print("⚠️ No processes found. Something might be wrong with psutil or permissions.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scan system processes and report to backend")
    parser.add_argument("--verbose", action="store_true", help="Show details while sending")
    parser.add_argument("--loop", action="store_true", help="Continuously scan every 60 seconds")
    args = parser.parse_args()

    wait_for_backend(API_URL)

    if args.loop:
        while True:
            scan_and_send(verbose=args.verbose)
            print("⏳ Waiting 60 seconds before next scan...\n")
            time.sleep(60)
    else:
        scan_and_send(verbose=args.verbose)