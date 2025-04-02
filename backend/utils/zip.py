import zipfile
from fastapi import UploadFile
import io

async def zip_validator(file: UploadFile):
    try:

        file_bytes = await file.read()
        file_buffer = io.BytesIO(file_bytes)

        with zipfile.ZipFile(file_buffer, "r") as z:
            if z.testzip() is None:
                return True
            return "Corrupt zip file"
    except zipfile.LargeZipFile:
        return "File is too large"
    except zipfile.BadZipFile:
        return  "Invalid zip file"
    except FileNotFoundError:
        return "File not found"

