import os
import argparse
from FilmioBack.DataFromLetterbox.DealWithZip import zip_file, unzip, copy_zip

os.getcwd()
directName = "Data"

if os.path.exists(directName):
    # Asks for the zip file
    parser = argparse.ArgumentParser(description="Decompress a .zip file.")
    parser.add_argument("file", type=zip_file, help=".zip path file")
    args = parser.parse_args()
    # Decompress the file in Temp
    unzip(args.file)
    # Copy zip to Backups
    copy_zip(args.file)


else:
    os.mkdir(directName)
    os.mkdir(f"{directName}/Backup")
    os.mkdir(f"{directName}/Csv_Data")
    os.mkdir(f"{directName}/Logs")
    os.mkdir(f"{directName}/Temp")
