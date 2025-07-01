import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.simple_data import simple_data_router
from routes.upload_file import upload_file_router
from routes.test import test_router

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

app.include_router(test_router)
app.include_router(simple_data_router)
app.include_router(upload_file_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)