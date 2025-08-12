from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
from supabase_client.db import get_supabase
from utils.zip import zip_validator, extract_zip
from letterboxd_data.extract_info import check_csv_columns, merge_csv_files
from utils.file import csv_to_json, validate_path
import json
import time


upload_file_router = APIRouter()

files_to_keep = {
    "diary.csv": ["Name", "Year", "Rating", "Watched Date"],
    "likes/films.csv": ["Name", "Year"],
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

    merged = merge_csv_files(
        "temp/letterboxd_data/likes/films.csv", "temp/letterboxd_data/diary.csv"
    )

    if merged is not True:
        raise HTTPException(status_code=400, detail=merged)

    json_file = "temp/letterboxd_data/final.json"
    json = csv_to_json(
        "temp/letterboxd_data/final.csv",
        json_file,
        ("Name", "Year", "Rating", "Watched Date", "Like"),
    )

    upload_films(json_file)

    if json is not True:
        raise HTTPException(status_code=400, detail="Error processing files")

    return {"file_name": file.filename, "file_size": file.size}


def upload_films(file):
    start = time.time()
    print("Starting to upload films")
    supabase = get_supabase()

    validate_path(file)

    films = pd.read_json(file)

    for _, film in films.iterrows():
        name = film["Name"]
        year = film["Year"]
        rating = film["Rating"]
        watched_date = film["Watched Date"]
        liked = film["Like"]

        existing = (
            supabase.table("films")
            .select("id")
            .eq("name", name)
            .eq("year", year)
            .limit(1)
            .execute()
        )

        if existing.data and len(existing.data) > 0:
            film_id = existing.data[0]["id"]

        else:
            inserted = (
                supabase.table("films").insert({"name": name, "year": year}).execute()
            )
            film_id = inserted.data[0]["id"]

        existing_viewing = (
            supabase.table("viewings")
            .select("id")
            .eq("film_id", film_id)
            .eq("watched_date", watched_date)
            .eq("rating", rating)
            .limit(1)
            .execute()
        )

        if not existing_viewing.data:
            supabase.table("viewings").insert(
                {
                    "film_id": film_id,
                    "rating": rating,
                    "watched_date": watched_date,
                    "liked": liked,
                }
            ).execute()

    print("All movies uploaded successfully")
    end = time.time()
    elapsed = end - start
    print(f"Time taken to upload movies: {elapsed:.2f} seconds")