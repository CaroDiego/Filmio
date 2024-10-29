import os
import shutil
from datetime import datetime

import pandas as pd


class DataHandler:
    # Variables de clase para rutas predeterminadas
    DIARY_PATH = 'FilmioBack/Data/Temp/diary.csv'
    LIKES_PATH = 'FilmioBack/Data/Temp/likes/films.csv'
    CSV_DATA_PATH = 'FilmioBack/Data/Csv_Data'
    WATCHLIST_SOURCE_PATH = 'FilmioBack/Data/Temp/watchlist.csv'

    def __init__(self, diary_path=DIARY_PATH, likes_path=LIKES_PATH,
                 csv_data_path=CSV_DATA_PATH, watchlist_source_path=WATCHLIST_SOURCE_PATH,
                 current_date=None,
                 diary=None, likes=None, watchlist=None
                 ):
        self.diary_path = diary_path
        self.likes_path = likes_path
        self.csv_data_path = csv_data_path
        self.watchlist_source_path = watchlist_source_path
        self.current_date = current_date or datetime.now().strftime('%Y-%m-%d')
        self.diary = pd.read_csv(self.diary_path) if os.path.exists(self.diary_path) else None
        self.likes = pd.read_csv(self.likes_path) if os.path.exists(self.likes_path) else None
        self.watchlist = pd.read_csv(self.watchlist_source_path) if os.path.exists(self.watchlist_source_path) else None

    def read_diary(self):
        filtered_diary = self.diary.dropna(subset=['Rating'])
        return filtered_diary

    def get_liked(self, rated_films):
        liked_films = rated_films.merge(
            self.likes[['Name', 'Year']],
            on=['Name', 'Year'],
            how='left',
            indicator=True
        )
        rated_films['Like'] = liked_films['_merge'] == 'both'
        return rated_films

    def process_data(self):
        rated_films = self.read_diary()
        rated_films = self.get_liked(rated_films)
        rated_films_path = os.path.join(self.csv_data_path, f"{self.current_date}_rated_films.csv")
        rated_films.to_csv(rated_films_path, index=False)
        shutil.copy(self.watchlist_source_path, os.path.join(self.csv_data_path, "watchlist.csv"))
