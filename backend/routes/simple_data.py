import os
from fastapi import APIRouter, HTTPException
import json
import pandas as pd

from utils.file import validate_path


simple_data_router = APIRouter()

@simple_data_router.get("/simpledata")
async def simple_data():
    file_path = "temp/letterboxd_data/final.json"
    
    validate_path(file_path)

    try:
        with open(file_path, "r") as file:
            data = json.load(file)

        return {"data": data}
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
@simple_data_router.get("/simpledata/{stat}")
async def simple_data_stat(stat: str):
    file_path = "temp/letterboxd_data/final.json"
    
    validate_path(file_path)

    try:
        df = pd.read_json(file_path)
        
        if stat not in df.columns:
            raise KeyError
        
        result = df[stat].value_counts().tolist()
        object = df[stat].value_counts().index.tolist()
        array = []
        for i in range(len(object)):
            item = {"key": object[i], "value": result[i]}
            array.append(item)
        
        array.sort(key=lambda x: x["key"])
        
        return {"stat": stat, "data": array}
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Stat '{stat}' not found")