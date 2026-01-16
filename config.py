import os
import json

# Define file paths
base_dir = os.path.dirname(os.path.abspath(__file__))
data_file_path = os.path.join(base_dir, 'data.json')
events_file_path = os.path.join(base_dir, 'events.json')

# Ensure `data.json` exists
if not os.path.exists(data_file_path):
    with open(data_file_path, 'w') as file:
        json.dump({"items": [], "staff": []}, file, indent=4)

# Ensure `events.json` exists
if not os.path.exists(events_file_path):
    with open(events_file_path, 'w') as file:
        json.dump({}, file, indent=4)