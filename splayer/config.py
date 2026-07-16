import os
import json

APP_DIR = os.path.join(os.getenv("APPDATA"), "splayer")
CONFIG_FILE = os.path.join(APP_DIR, "config.json")
TOKEN_FILE = os.path.join(APP_DIR, "token.cache")

def ensure_dir():
    if not os.path.exists(APP_DIR):
        os.makedirs(APP_DIR)

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {}

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(data):
    ensure_dir()

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
        

def update_config(data):
    config = load_config()
    config.update(data)
    save_config(config)