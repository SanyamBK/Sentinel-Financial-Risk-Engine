import pandas as pd
import json
import os

def get_data_paths():
    """Returns the paths for data files relative to this script."""
    # Get the directory where this script is located (dashboard/)
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    # Data dir is sibling to dashboard/ -> ../data
    DATA_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "data")
    OUTPUT_FILE = os.path.join(DATA_DIR, "sentinel_output.jsonl")
    return OUTPUT_FILE

def load_data(output_file):
    """Loads the Sentinel output data from JSONL."""
    if not os.path.exists(output_file):
        return pd.DataFrame()
    
    data = []
    try:
        with open(output_file, 'r') as f:
            for line in f:
                try:
                    data.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    except Exception:
        return pd.DataFrame()
        
    if not data:
        return pd.DataFrame()
        
    df = pd.DataFrame(data)
    return df
