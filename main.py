from fritzconnection.lib.fritzstatus import FritzStatus
from datetime import datetime
import json
import os

# Define filepath
filepath = os.path.join(os.getcwd(), 'data.json')

# Try to open file and read past JSON-data. If file does not exist, create dictionary with keys but no values.
try:
    with open(filepath, 'r', encoding='utf-8') as f:
        past_data = json.load(f)
except FileNotFoundError:
    past_data = {"datetime": "", "public_ip": ""}

# Get current public ip-address
public_ip = FritzStatus(address='192.168.178.1').external_ip

# Create current data
current_data = {"datetime": str(datetime.now()), "public_ip": public_ip}

# Compare past data with current data and output the result
if past_data['public_ip'] == current_data['public_ip']:
    print('Same IP')
else:
    print('Different IP')

# Save current-data as JSON-data to filepath
with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(current_data, f, ensure_ascii=False, indent=4)

# Print out current-data from filepath
with open(filepath, 'r', encoding='utf-8') as f:
    raw_data2 = json.load(f)
    print(raw_data2)
