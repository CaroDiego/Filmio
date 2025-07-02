import json
from fastapi import APIRouter
import pandas as pd

from tmdb_data.get_info import get_movie_list


tmdb_data_router = APIRouter()

@tmdb_data_router.get("/tmdbdata")
async def tmdb_data():
    
    try:
        file_path = "temp/letterboxd_data/final.json"
        df = pd.read_json(file_path)

        results = []
        for _, row in df.iterrows():
            name = row.get('Name')
            year = row.get('Year')
            movie_info = get_movie_list(name=name, year=year)
            results.append(movie_info)
        return results

    except Exception as e:
        return {"error": str(e)}