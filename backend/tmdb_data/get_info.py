

import os
import urllib
from dotenv import load_dotenv

import requests

load_dotenv()

def format_movie_name(name):
    return urllib.parse.quote(name)


def get_movie_list(name, year):
    
    HEADER = os.getenv("TMDB_HEADER")
    HEADERS = {
        "accept": "application/json",
        "Authorization": f"Bearer {HEADER}",
    }
    URL = os.getenv("TMDB_URL")
    
    if not name or not year:
        return {"error": "Name and year are required"}
    
    formatted_name = format_movie_name(name)
    url = f"{URL}/search/movie?query={formatted_name}&include_adult=false&language=en-US&page=1&year={year}"

    try:
        
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        # list = response.json().get("results", [])
        list = response.json().get("results", [])
        movie = get_movie_info(list, name)
        return movie    
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    


def get_movie_info(list, name):
    try:
        exact_match = next((item for item in list if item["title"].lower() == name.lower()), None)
        
        if exact_match:
            return {
                "matched": True,
                "tmbd_title": exact_match["title"],
                "original_title": exact_match["original_title"],
                "id": exact_match["id"],
                "overview": exact_match["overview"],
            }
        else:
            movie = list[0] if list else None
            return {
                "matched": False,
                "tmbd_title": movie["title"],
                "original_title": movie["original_title"],
                "id": movie["id"],
                "overview": movie["overview"],
            }
    except (IndexError, KeyError) as e:
        return {"error": f"Error processing movie list: {str(e)}"}