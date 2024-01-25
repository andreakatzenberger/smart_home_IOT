import json

def load_settings(filePath='settingspi1.json'):
    with open(filePath, 'r') as f:
        return json.load(f)