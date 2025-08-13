import json
import os
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

from jobs_structure.orchestrator import orchestrator
from supabase_client.config.job_type import JobType


class Test(BaseModel):
    test: str


test_router = APIRouter()


@test_router.get("/test")
async def root():
    items = orchestrator(JobType.TMDB_FILM_DATA.value)
    return {"items": items}

@test_router.get("/test2")
async def root2():
    """
    This is a test endpoint to see how to read an specific key from a specific object from an array in a JSON file.
    """
    file_path = "temp/letterboxd_data/final.json"

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            object = data[0]
        return {"data": object["Name"]}
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
