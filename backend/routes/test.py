from pydantic import BaseModel
from fastapi import APIRouter


class Test(BaseModel):
    test: str

test_router = APIRouter()

@test_router.get("/test")
async def root():
    return Test(test="Server is up and running")

@test_router.get("/test2")
async def root2():
    return Test(test="Server is up and running 2")