import zipfile
from fastapi import UploadFile
import io
import os
import tempfile
import pandas as pd

async def zip_validator(file: bytes):
    """
    Validates if a given file is a valid ZIP archive.
    Args:
        file (bytes): The file content in bytes.
    Returns:
        bool: True if the file is a valid ZIP archive, otherwise an error message.
    Raises: 
        zipfile.BadZipFile: If the provided file is not a valid ZIP file.
        zipfile.LargeZipFile: If the ZIP file is too large.
        FileNotFoundError: If the file is not found.
    """
    try:

        file_buffer = io.BytesIO(file)

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


async def extract_zip(file: bytes, extract_path: str, files_to_check: dict[str, list[str]]):
    """
    Extracts specific files from a ZIP archive, filters their contents based on
    provided column names, and saves the filtered data to the specified extraction path.
    Args:
        file (bytes): The ZIP file content in bytes.
        extract_path (str): The directory path where the extracted and processed 
            files will be saved.
        files_to_check (dict[str, list[str]]): A dictionary where keys are the 
            names of files to extract from the ZIP archive, and values are lists 
            of column names to retain in the extracted files.
    Returns:
        str: An error message if the ZIP file is invalid, a required file is 
            missing, or specified columns are not found in a file.
        bool: True if all specified files are successfully processed and saved.
    Raises:
        zipfile.BadZipFile: If the provided file is not a valid ZIP file.
        Exception: For any other unexpected errors during processing.
    """
    try:
        file_buffer = io.BytesIO(file)

        with zipfile.ZipFile(file_buffer, "r") as z:
            #For each file keeps only the columns specified in the dictionary
            for file_name, columns_to_keep in files_to_check.items(): 
                if file_name in z.namelist(): #Check if the file is in the zip
                    with z.open(file_name) as csv_file:
                        df = pd.read_csv(csv_file)
                        if not all(col in df.columns for col in columns_to_keep): # Check if the columns are in the file
                            return f"Some specified columns are not present in '{file_name}'."
                        filtered_df = df[columns_to_keep]
                        output_path = os.path.join(extract_path, file_name)
                        os.makedirs(os.path.dirname(output_path), exist_ok=True)
                        filtered_df.to_csv(output_path, index=False)
                else:
                    return f"File '{file_name}' not found in the ZIP archive."
                
        return True
    except zipfile.BadZipFile:
        return "The provided file is not a valid ZIP file."
    except Exception as e:
        return str(e)