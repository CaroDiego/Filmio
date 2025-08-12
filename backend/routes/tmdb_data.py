import asyncio
from concurrent.futures import ThreadPoolExecutor
import json
from fastapi import APIRouter
import httpx
import pandas as pd

from tmdb_data.get_info import get_movie_list
from utils.file import validate_path


tmdb_data_router = APIRouter()

@tmdb_data_router.get("/tmdbdata")
async def tmdb_data():
    
    file_path = "temp/letterboxd_data/final.json"
    validate_path(file_path)

    try:
        df = pd.read_json(file_path)

        def fetch_movie(row):
            name = getattr(row, 'Name', None)
            year = getattr(row, 'Year', None)
            return get_movie_list(name=name, year=year)
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(fetch_movie, df.itertuples(index=False)))
            
        return results
        
            
    except Exception as e:
        return {"error": str(e)}