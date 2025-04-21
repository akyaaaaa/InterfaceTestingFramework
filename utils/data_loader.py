import json
import os

# DATA_DIR = "data"
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")


def load_json(file_name, modelname=''):
    file_path = os.path.join(os.path.join(DATA_DIR, modelname), file_name)
    with open(file_path, "r", encoding='utf-8') as f:
        return json.load(f)
