import logging
import os

os.mkdir("/Users/dicaf/Filmio/FilmioBack/Logs/") if not os.path.exists("/Users/dicaf/Filmio/FilmioBack/Logs/") else None
LOG_PATH = '/Users/dicaf/Filmio/FilmioBack/Logs/app.log'

logging.basicConfig(level=logging.DEBUG, filename=LOG_PATH,
                    format="%(asctime)s  - %(threadName)s - %(processName)s - %(levelname)s : %(message)s",
                    filemode="a")

lbox_logger = logging.getLogger("DataFromLetterbox")
