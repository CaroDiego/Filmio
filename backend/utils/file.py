import csv
import json
import pandas as pd

def csv_to_json(csv_file: str, json_file: str, fieldnames: tuple[str]):
    try:
        df = pd.read_csv(csv_file, usecols=fieldnames)
        df.to_json(json_file, orient='records', indent=2) 
        return True
    except Exception as e:
        return f"An error occurred: {e}"
