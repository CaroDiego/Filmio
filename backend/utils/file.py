import pandas as pd
import os
from fastapi import HTTPException


def csv_to_json(csv_file: str, json_file: str, fieldnames: tuple[str]):
    try:
        df = pd.read_csv(csv_file, usecols=fieldnames)
        df.to_json(json_file, orient='records', indent=2) 
        return True
    except Exception as e:
        return f"An error occurred: {e}"


def validate_path(file_path: str):
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")