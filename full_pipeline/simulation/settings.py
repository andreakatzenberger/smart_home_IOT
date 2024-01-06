import json

def load_settings(filePath='C://Users//andre//OneDrive//Documents//GitHub//smart_home_IOT//full_pipeline//simulation//settings.json'):
    with open(filePath, 'r') as f:
        return json.load(f)