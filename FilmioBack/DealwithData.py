from symtable import Class

import pandas as pd

diary = pd.read_csv('Data/Temp/diary.csv')
likes = pd.read_csv('Data/Temp/likes/films.csv')
rated_films = pd.read_csv('Data/Csv_Data/rated_films.csv')


def read_diary():
    rated_films = diary.dropna(subset=['Rating'])
    rated_films.to_csv('rated_films.csv', index=False)
    return rated_films


def get_liked(rated_films):
    rated_films['Like'] = rated_films.apply(
        lambda row: any((row['Name'] == like['Name'] and row['Year'] == like['Year']) for _, like in likes.iterrows()),
        axis=1
    )
    rated_films.to_csv('rated_films.csv', index=False)
    print(rated_films.info())
    return rated_films

rated_films = read_diary()
rated_films = get_liked(rated_films)