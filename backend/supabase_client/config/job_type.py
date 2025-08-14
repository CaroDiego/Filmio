from enum import Enum


class JobType(Enum):
    """Enumeration for job types.

    Args:
        Enum (enum.Enum): The base class for all enumerations.
    """

    TMDB_FILM_DATA = "tmdb_film_data"
