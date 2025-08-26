# src/data/data_loader.py
import json
from typing import List, Dict

def load_employees(file_path: str) -> List[Dict]:
    """Load employee data from a JSON file."""
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
            return data.get("employees", [])
    except FileNotFoundError:
        raise Exception(f"Employee data file not found at {file_path}")
    except json.JSONDecodeError:
        raise Exception("Invalid JSON format in employee data file")