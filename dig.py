import readline
import os
import json
import subprocess
from urllib.parse import urlparse

# Enable tab completion
readline.parse_and_bind("tab: complete")

def complete_path(text, state):
    # Expand ~ for home directory
    text = os.path.expanduser(text)
    return [x for x in os.listdir(os.path.dirname(text) or ".") if x.startswith(os.path.basename(text))][state]

readline.set_completer(complete_path)

# Ask for JSON file path
json_file = input("Enter the path to your JSON file: ")
json_file = os.path.expanduser(json_file)  # Expand ~

# Load JSON file
try:
    with open(json_file, "r") as f:
        data = json.load(f)
except Exception as e:
    print(f"Error reading JSON file: {e}")
    exit(1)

# Iterate over each entry
for entry in data:
    url = entry.get("subdomain")
    if not url:
        continue
    
    hostname = urlparse(url).netloc or url
    print(f"\n=== Digging: {hostname} ===")
    
    try:
        result = subprocess.run(["dig", hostname], capture_output=True, text=True)
        print(result.stdout)
    except Exception as e:
        print(f"Error running dig on {hostname}: {e}")
