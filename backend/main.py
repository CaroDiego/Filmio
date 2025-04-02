import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
import zipfile
import io
import os
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from utils.zip import zip_validator


class Test(BaseModel):
    test: str


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



@app.post("/uploadfile")
async def create_upload_file(file: UploadFile = File(...)):

    is_valid = await zip_validator(file)
    
    if is_valid is not True:
        raise HTTPException(status_code=400, detail=is_valid)
    
    return {"file_name": file.filename, "file_size": file.size}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)