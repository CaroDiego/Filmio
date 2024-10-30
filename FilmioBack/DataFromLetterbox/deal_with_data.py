print("Script is starting")

import os

from FilmioBack.DataFromLetterbox.data_handler import DataHandler
from FilmioBack.DataFromLetterbox.zip_handler import ZipHandler
from FilmioBack.logger_config import lbox_logger

print("Starting decompression")
os.chdir("/Users/dicaf/Filmio/FilmioBack")
if not os.path.exists("Logs"):
    os.mkdir("Logs")
directName = "Data"
zip_handler = ZipHandler()
data_handler = DataHandler()

if os.path.exists(directName):
    lbox_logger.info("Directories structure already exists" + directName)
    zip_handler.process_zip()
else:
    os.mkdir(directName)
    os.mkdir(f"{directName}/Backup")
    os.mkdir(f"{directName}/Csv_Data")
    os.mkdir(f"{directName}/Temp")
    lbox_logger.info("Directories structure has been created" + directName)
    zip_handler.process_zip()

print("Processing data")
data_handler.process_data()
print("End of script")
