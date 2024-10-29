import os
import argparse

from FilmioBack.DataFromLetterbox.DataHandler import DataHandler
from FilmioBack.DataFromLetterbox.ZipHandler import ZipHandler

os.getcwd()
directName = "Data"
zip_handler = ZipHandler()
data_handler = DataHandler()

if os.path.exists(directName):
    zip_handler.process_zip()

else:
    os.mkdir(directName)
    os.mkdir(f"{directName}/Backup")
    os.mkdir(f"{directName}/Csv_Data")
    os.mkdir(f"{directName}/Logs")
    os.mkdir(f"{directName}/Temp")
    zip_handler.process_zip()

data_handler.process_data()
