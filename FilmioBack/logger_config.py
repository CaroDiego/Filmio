import logging
import os
from pathlib import Path

log_dir = Path("/Users/dicaf/Filmio/FilmioBack/Logs")
log_file = log_dir / "app.log"

log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(level=logging.DEBUG, filename=log_file,
                    format="%(asctime)s - %(name)s - %(threadName)s - %(processName)s - %(levelname)s : %(message)s",
                    filemode="a")

lbox_logger = logging.getLogger("DataFromLetterbox")
tmdb_logger = logging.getLogger("ConnectionToTMDB")
