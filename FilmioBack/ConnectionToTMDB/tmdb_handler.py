import requests
import urllib.parse

from FilmioBack.ConnectionToTMDB.Key import HEADER
from FilmioBack.logger_config import tmdb_logger


class TmbdHandler:
    """
    Class to handle requests to the TMDB API.
    Attributes:
        BASE_URL: str
            Base URL of the TMDB API.
        HEADERS: dict
            Header of  the request to the TMDB API.
    """
    BASE_URL = "https://api.themoviedb.org/3"
    HEADERS = {
        "accept": "application/json",
        "Authorization": f"Bearer {HEADER}",
    }

    @staticmethod
    def format_movie_name(name):
        """
        Format the movie name to be used in an url request.
        :param name: name to format
        :return: the name formatted to be used in a request
        """
        return urllib.parse.quote(name)

    @classmethod
    def get_movie_info(cls, name, year):
        """
        Get the movie information from the TMDB API.
        Search with the movie name and year.
        :param name:
        :param year:
        :return: The json with all the information of the movie
        """
        if not name or not year:
            tmdb_logger.error("Name and year are required")
            return None
        encoded_name = cls.format_movie_name(name)
        url = f"{cls.BASE_URL}/search/movie?query={encoded_name}&include_adult=false&language=en-US&page=1&year={year}"

        try:
            response = requests.get(url, headers=cls.HEADERS)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            tmdb_logger.error(f"Error in request to TMDB API: {e}")
            return None

    @classmethod
    def get_genre(cls):
        """
        Get the list of genres from the TMDB API.
        :return:  The json with the list of genres
        """
        url = f"{cls.BASE_URL}/genre/movie/list?language=en"

        try:
            response = requests.get(url, headers=cls.HEADERS)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            tmdb_logger.error(f"Error in request to TMDB API: {e}")
            return None

    @classmethod
    def get_movie_images(cls, movie_id):
        """
        Get the images of a movie from the TMDB API.
        :param movie_id: The id of the movie
        :return: The json with the images of the movie
        """
        url = f"{cls.BASE_URL}/movie/{movie_id}/images"

        try:
            response = requests.get(url, headers=cls.HEADERS)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            tmdb_logger.error(f"Error in request to TMDB API: {e}")
            return None

    @classmethod
    def get_movie_credits(cls, movie_id):
        """
        Get the credits of a movie from the TMDB API.
        :param movie_id: The id of the movie
        :return: The json with the credits of the movie
        """
        url = f"{cls.BASE_URL}/movie/{movie_id}/credits?language=en-US"

        try:
            response = requests.get(url, headers=cls.HEADERS)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            tmdb_logger.error(f"Error in request to TMDB API: {e}")
            return None

    @classmethod
    def get_person_info(cls, person_id):
        """
        Get the person information from the TMDB API.
        Search with the person id.
        :param name:
        :return: The json with all the information of the person
        """
        url = f"{cls.BASE_URL}/person/{person_id}?language=en-US"

        try:
            response = requests.get(url, headers=cls.HEADERS)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            tmdb_logger.error(f"Error in request to TMDB API: {e}")
            return None
