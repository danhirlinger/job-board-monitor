import requests
import hashlib
import os
import sys
from datetime import datetime

# Configuration
JOB_BOARD_URL = "https://jobs.gusto.com/boards/switchyards-inc-53b85507-2487-42ff-87a2-196907c98839"
HASH_FILE = "job_board_hash.txt"

def fetch_job_board():
    """Fetch the job board HTML content"""
    try:
        response = requests.get(JOB_BOARD_URL, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching job board: {e}")
        sys.exit(1)

def get_content_hash(content):
    """Generate SHA256 hash of content"""
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def load_previous_hash():
    """Load the previously stored hash"""
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, 'r') as f:
            return f.read().strip()
    return None

def save_hash(content_hash):
    """Save the current hash"""
    with open(HASH_FILE, 'w') as f:
        f.write(content_hash)

def main():
    print(f"[{datetime.now()}] Checking job board for changes...")
    
    # Fetch current content
    current_content = fetch_job_board()
    current_hash = get_content_hash(current_content)
    
    # Load previous hash
    previous_hash = load_previous_hash()
    
    if previous_hash is None:
        print("First run - storing initial hash")
        save_hash(current_hash)
        print("✓ Baseline established")
        sys.exit(0)
    
    if current_hash != previous_hash:
        print("🚨 CHANGE DETECTED!")
        print(f"Previous hash: {previous_hash[:16]}...")
        print(f"Current hash:  {current_hash[:16]}...")
        save_hash(current_hash)
        
        # Exit with code 1 to trigger CI notification
        sys.exit(1)
    else:
        print("✓ No changes detected")
        sys.exit(0)

if __name__ == "__main__":
    main()
