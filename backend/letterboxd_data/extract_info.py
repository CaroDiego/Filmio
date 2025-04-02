from fastapi import UploadFile
import zipfile
import pandas as pd
import os 

def check_csv_columns(zip: UploadFile, files_to_check: dict):
    """
    Check if the zip contains the specified files and their columns.
    Args:
        zip (UploadFile): The uploaded zip file.
        files_to_check (dict): A dictionary where keys are the names of files to check,
            and values are lists of column names to verify.
    Returns:
        bool: True if all specified files and columns are present, otherwise an error message.
    """
    with zipfile.ZipFile(zip.file, 'r') as z:
        for file_name, required_columns in files_to_check.items():
            if file_name in z.namelist():
                with z.open(file_name) as f:
                    df = pd.read_csv(f)
                    
                    if not set(required_columns).issubset(df.columns):
                        return f"Missing columns in {file_name}: {set(required_columns) - set(df.columns)}"
            else:
                return f"{file_name} not found in the zip file."
    return True


def merge_csv_files(likes, diary):
    """
    Put on a file the films that are liked and has been watched.
    Args:
        likes (str): Path to the likes CSV file.
        diary (str): Path to the diary CSV file.
    Returns:
        bool: True if the merge was successful, 
            otherwise an error message.
    Raises:
        Exception: For any unexpected errors during processing.
    """
    try:
        likes_df = pd.read_csv(likes)
        diary_df = pd.read_csv(diary)
        
        diary_df.dropna(subset=['Rating'], inplace=True)
        diary_df.reset_index(drop=True, inplace=True)
        
        merged_df = diary_df.merge(
            likes_df[['Name', 'Year']],
            on=['Name', 'Year'],
            how='left',
            indicator=True
        )
        
        final = diary_df.copy()
        final['Like'] = merged_df['_merge'] == 'both'
        final.to_csv("temp/letterboxd_data/final.csv", index=False)
        os.remove(likes)
        os.remove(diary)
        os.rmdir(os.path.dirname(likes))
    
        return True
    except Exception as e:
        return f"Error merging CSV files: {e}"
    
    