from supabase_client.config.create_jobs_config import create_if_not_exist_film_job
from supabase_client.config.job_type import JobType
from supabase_client.db import get_supabase

# TODO add error handling

def orchestrator(jobType):
    create_if_not_exist_job(jobType)
    supabase = get_supabase()

    jobType_info = get_job_type(jobType)

    supabase.table("jobs").insert({"job_config_id": jobType_info["id"]}).execute()

    items = get_item_list(jobType)

    print("[Orchestrator]", len(items), "items to process")

    return items

def create_if_not_exist_job(jobType):
    if jobType == JobType.TMDB_FILM_DATA.value:
        create_if_not_exist_film_job()


def get_job_type(jobType):
    supabase = get_supabase()
    jobType = (
        supabase.table("jobs_config")
        .select("*")
        .eq("job_type", jobType)
        .execute()
    )
    return jobType.data[0]


def get_item_list(jobType):
    supabase = get_supabase()
    item_list = []
    if jobType == JobType.TMDB_FILM_DATA.value:
        item_list = supabase.table("films").select("id", "name", "year").execute()

    return item_list.data
