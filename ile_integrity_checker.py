import hashlib
import json
import os

# Path to store the known hashes
HASH_DB_FILE = "file_hashes.json"

def calculate_hash(file_path, algorithm='sha256'):
    """
    Calculate the hash of a file.
    """
    h = hashlib.new(algorithm)
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                h.update(chunk)
        return h.hexdigest()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None

def load_known_hashes():
    """
    Load previously stored hashes from the JSON file.
    """
    if os.path.exists(HASH_DB_FILE):
        with open(HASH_DB_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_known_hashes(hashes):
    """
    Save the hashes dictionary to the JSON file.
    """
    with open(HASH_DB_FILE, 'w') as f:
        json.dump(hashes, f, indent=4)

def monitor_files(file_paths):
    """
    Monitor given files for changes by comparing hashes.
    """
    known_hashes = load_known_hashes()
    current_hashes = {}

    for file_path in file_paths:
        hash_value = calculate_hash(file_path)
        if hash_value:
            current_hashes[file_path] = hash_value

            # Compare with known hash
            if file_path in known_hashes:
                if known_hashes[file_path] != hash_value:
                    print(f"[ALERT] File changed: {file_path}")
                else:
                    print(f"[OK] File unchanged: {file_path}")
            else:
                print(f"[NEW] New file added: {file_path}")
        else:
            print(f"[ERROR] Could not read file: {file_path}")

    # Update the stored hashes
    save_known_hashes(current_hashes)

if __name__ == "__main__":
 
    files_to_check = [
        r"C:\Users\thara\OneDrive\Documents\file_integrity_checker.py\example.txt.txt",
        r"C:\Users\thara\OneDrive\Documents\file_integrity_checker.py\data.csv.txt",
        r"C:\Users\thara\OneDrive\Documents\file_integrity_checker.py\script.py.txt"

    ]
    monitor_files(files_to_check)
