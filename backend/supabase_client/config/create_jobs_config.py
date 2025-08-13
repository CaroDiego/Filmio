from supabase_client.config.job_type import JobType
from supabase_client.db import get_supabase


def create_if_not_exist_film_job():
    supabase = get_supabase()

    existing = (
        supabase.table("jobs_config")
        .select("*")
        .eq("job_type", JobType.TMDB_FILM_DATA.value)
        .execute()
    )
    if not existing.data:
        supabase.table("jobs_config").insert(
            {
                "job_type": JobType.TMDB_FILM_DATA.value,
                "batch_size": 10,
                "max_concurrency": 5,
                "max_retries": 3,
                "retry_delay_ms": 3000,
            }
        ).execute()
