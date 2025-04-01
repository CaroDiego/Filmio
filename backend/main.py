import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
import zipfile
import io
import os
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List


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
    try:
        contents = await file.read()
        zip_bytes = io.BytesIO(contents)

        with zipfile.ZipFile(zip_bytes, "r") as z:
            file_list = z.namelist()

    except zipfile.BadZipFile:
        raise HTTPException(status_code=400, detail="Invalid zip file")
    
    return {"file_name": file.filename, "file_list": file_list, "file_size": file.size}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)