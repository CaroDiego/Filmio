import os

from supabase import create_client, Client

from FilmioBack.ConnectionToSupabase.key import SUPABASE_KEY, SUPABASE_URL, SERVICE_KEY


class SupabaseHandler:
    url: str = SUPABASE_URL
    key: str = SERVICE_KEY
    supabase: Client = create_client(url, key)

    @classmethod
    def insert_genres(cls, genres_json):
        """
        Insert genres into the genre table.
        :param genres_json: JSON containing genres with id and name
        """
        genres = genres_json.get('genres', [])
        for genre in genres:
            cls.supabase.table('genre').insert({'id': genre['id'], 'name': genre['name']}).execute()

    def get_genres(cls):
        response = cls.supabase.table("genre").select("*").execute()
        return response