import os
import shutil
from datetime import datetime, timezone

import pandas as pd
from FilmioBack.logger_config import lbox_logger


class DataHandler:
    """
    Class to handle data operations, such as reading and processing data.
    Attributes:
        DIARY_PATH: str
            Path to the diary file.
        LIKES_PATH: str
            Path to the likes file.
        RATED_PATH: str
            Path to the csv data directory.
        WATCHLIST_SOURCE_PATH: str
            Path to the watchlist file.
    """
    DIARY_PATH = 'C:/Users/dicaf/Filmio/FilmioBack/Data/Temp/diary.csv'
    LIKES_PATH = 'C:/Users/dicaf/Filmio/FilmioBack/Data/Temp/likes/films.csv'
    RATED_PATH = 'C:/Users/dicaf/Filmio/FilmioBack/Data/Csv_Data/Rated'
    WATCHLIST_PATH = 'C:/Users/dicaf/Filmio/FilmioBack/Data/Csv_Data/Watchlist'
    WATCHLIST_SOURCE_PATH = 'C:/Users/dicaf/Filmio/FilmioBack/Data/Temp/watchlist.csv'

    def __init__(self, diary_path=DIARY_PATH, likes_path=LIKES_PATH,
                 rated_path=RATED_PATH, watchlist_path=WATCHLIST_PATH, watchlist_source_path=WATCHLIST_SOURCE_PATH,
                 current_date=None):
        self.diary_path = diary_path
        self.likes_path = likes_path
        self.rated_path = rated_path
        self.watchlist_path = watchlist_path
        self.watchlist_source_path = watchlist_source_path
        self.current_date = current_date or datetime.now().strftime('%Y-%m-%d')
        self.diary = pd.read_csv(self.diary_path) if os.path.exists(self.diary_path) else None
        self.likes = pd.read_csv(self.likes_path) if os.path.exists(self.likes_path) else None
        self.watchlist = pd.read_csv(self.watchlist_source_path) if os.path.exists(self.watchlist_source_path) else None

    def get_rated(self):
        """
        Read the diary file and return the rows with a rating.
        :return: The diary file with the rows with a rating.
        """
        if self.diary is not None:
            return self.diary.dropna(subset=['Rating'])
        else:
            lbox_logger.critical("Diary file not found")
            return pd.DataFrame()



    def get_liked(self, rated_films):
        """
        Merge the rated films with the likes file to get the liked films.
        :param rated_films:
        :return:  The rated films with a column indicating if the film is liked.
        """
        if self.likes is not None:
            liked_films = rated_films.merge(
                self.likes[['Name', 'Year']],
                on=['Name', 'Year'],
                how='left',
                indicator=True
            )
            rated_films['Like'] = liked_films['_merge'] == 'both'
            return rated_films
        else:
            lbox_logger.critical("Likes file not found")
            return rated_films

    def get_recent_files(self, directory):
        files = [f for f  in os.listdir(directory)]
        files.sort()


    def process_data(self):
        """
        Read the diary file, get the liked films and save the rated films and the watchlist.

        Logs messages to indicate the process.
        """
        # Get rated films
        print("Getting Rated films")
        rated_films = self.get_rated()

        # Get liked films
        print("Getting Liked films")
        rated_films = self.get_liked(rated_films)

        # Save rated films
        rated_films_path = os.path.join(self.rated_path, f"{self.current_date}_rated_films.csv")
        rated_films.to_csv(rated_films_path, index=False)
        lbox_logger.info(f"Saved rated films to {rated_films_path}")

        # Save watchlist
        watchlist_path = os.path.join(self.watchlist_path, f"{self.current_date}_watchlist.csv")
        shutil.copy(self.watchlist_source_path, watchlist_path)
        lbox_logger.info(f"Saved watchlist to {self.watchlist_path}")

