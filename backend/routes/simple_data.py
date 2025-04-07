import os
from fastapi import APIRouter, HTTPException
import json


simple_data_router = APIRouter()

@simple_data_router.get("/simpledata")
async def simple_data():
    file_path = "temp/letterboxd_data/final.json"
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    try:
        with open(file_path, "r") as file:
            data = json.load(file)

        return {"data": data}
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))