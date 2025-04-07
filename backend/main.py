import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
import zipfile
import io
import os
import json
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from letterboxd_data.extract_info import check_csv_columns, merge_csv_files
from utils.file import csv_to_json
from utils.zip import extract_zip, zip_validator


class Test(BaseModel):
    test: str


files_to_keep = {
    "diary.csv": ["Name", "Year", "Rating", "Watched Date"],
    "likes/films.csv": ["Name", "Year"]
}

app = FastAPI()

origins = [
    "http://localhost:5173", #*Development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/test")
async def root():
    return Test(test="Server is up and running")


@app.get("/simpledata")
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

@app.post("/uploadfile")
async def create_upload_file(file: UploadFile = File(...)):
    file_bytes = await file.read()

    is_valid = await zip_validator(file_bytes)
    
    if is_valid is not True:
        raise HTTPException(status_code=400, detail=is_valid)
    
    
    
    letterboxd_format = check_csv_columns(file, files_to_keep)
    
    if letterboxd_format is not True:
        raise HTTPException(status_code=400, detail=letterboxd_format)
    
    
    extraction = await extract_zip(file_bytes, "temp/letterboxd_data", files_to_keep)
    if extraction is not True:
        raise HTTPException(status_code=400, detail=extraction)
    
    merged = merge_csv_files("temp/letterboxd_data/likes/films.csv", "temp/letterboxd_data/diary.csv")
    
    if merged is not True:
         raise HTTPException(status_code=400, detail=merged)

    json = csv_to_json("temp/letterboxd_data/final.csv", "temp/letterboxd_data/final.json", ("Name", "Year", "Rating", "Watched Date", "Like"))

    if json is not True:
        raise HTTPException(status_code=400, detail="Error processing files")
    
    return {"file_name": file.filename, "file_size": file.size}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)