import psutil
import requests
import argparse
from filters import load_filters, is_relevant_process 

API_URL = "http://localhost:8001/status"

def main(verbose=False):
    filters = load_filters()

    for proc in psutil.process_iter(['name']):
        try:
            name = proc.info['name']
            if not is_relevant_process(name, filters.get("include"), filters.get("exclude")):
                continue

            data = {
                "name": name,
                "status": "up",
                "dependencies": []
            }
            res = requests.post(API_URL, json=data)
            if verbose:
                print(f"Sent: {data['name']} → {res.status_code}")
        except Exception as e:
            if verbose:
                print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process Scanner with Optional Verbosity")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    args = parser.parse_args()

    main(verbose=args.verbose)