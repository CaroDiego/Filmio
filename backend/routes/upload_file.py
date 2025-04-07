from fastapi import APIRouter, UploadFile, File, HTTPException
from utils.zip import zip_validator, extract_zip
from letterboxd_data.extract_info import check_csv_columns, merge_csv_files
from utils.file import csv_to_json

upload_file_router = APIRouter()

files_to_keep = {
    "diary.csv": ["Name", "Year", "Rating", "Watched Date"],
    "likes/films.csv": ["Name", "Year"]
}

@upload_file_router.post("/uploadfile")
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