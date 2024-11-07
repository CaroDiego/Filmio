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

directories = [
    directName,
    f"{directName}/Backup",
    f"{directName}/Csv_Data",
    f"{directName}/Csv_Data/Rated",
    f"{directName}/Csv_Data/Watchlist",
    f"{directName}/Temp"
]

for directory in directories:
    if not os.path.exists(directory):
        os.mkdir(directory)
        lbox_logger.info(f"Directory created: {directory}")

zip_handler.process_zip()

print("Processing data")
data_handler.process_data()
print("End of script")

#TODO Despues de hacer el request a la API de letterbox guardar en un archivo las peliculas
#TODO Antes de hacer el request a la API de letterbox comparar el archivo con el archivo nuevo
#TODO hacer el request a la API de letterbox solo de las peliculas nuevas

