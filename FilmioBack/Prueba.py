import os
import pandas as pd
from datetime import datetime
import shutil  # Para copiar archivos

#TODO 1: Hacer el scripting entero en python
#TODO 2: Hacer una clase para los logs
#TODO 3: La Carpeta Temp no existe, se tiene que crear en el script
#TODO 4: Descomprimir -> Crear Temp -> Procesar -> Crear Carpeta en Csv_Data -> Mover archivos a la carpeta


# Definición de rutas
diary_path = 'FilmioBack/Data/Temp/diary.csv'
likes_path = 'FilmioBack/Data/Temp/likes/films.csv'
csv_data_path = 'FilmioBack/Data/Csv_Data'
watchlist_source_path = 'FilmioBack/Data/Temp/watchlist.csv'

# Obtener la fecha actual en formato YYYY-MM-DD
current_date = datetime.now().strftime('%Y-%m-%d')
dated_folder_path = os.path.join(csv_data_path, current_date)

# Crear la carpeta con la fecha actual si no existe
os.makedirs(dated_folder_path, exist_ok=True)

# Ruta de guardado para rated_films.csv y watchlist.csv
rated_films_path = os.path.join(dated_folder_path, 'rated_films.csv')
watchlist_dest_path = os.path.join(csv_data_path, 'watchlist.csv')  # Cambiar a la ruta correcta

# Carga de datos condicional
if os.path.exists(diary_path) and os.path.exists(likes_path):
    diary = pd.read_csv(diary_path)
    likes = pd.read_csv(likes_path)
else:
    raise FileNotFoundError("Uno o más archivos requeridos no existen.")

def read_diary():
    # Filtra las filas con calificación
    filtered_diary = diary.dropna(subset=['Rating'])
    return filtered_diary

def get_liked(rated_films):
    # Marca como 'Like' si el filme está en el listado de 'likes'
    liked_films = rated_films.merge(
        likes[['Name', 'Year']], 
        on=['Name', 'Year'], 
        how='left', 
        indicator=True
    )
    rated_films['Like'] = liked_films['_merge'] == 'both'  # True si el film está en likes
    return rated_films

# Ejecuta funciones para procesar datos
rated_films = read_diary()
rated_films = get_liked(rated_films)

# Guardado de rated_films.csv en la carpeta con la fecha actual
rated_films.to_csv(rated_films_path, index=False)

# Copiar watchlist.csv al mismo directorio con la fecha actual
shutil.copy(watchlist_source_path, watchlist_dest_path)

# Mostrar información de rated_films
print(rated_films.info())


