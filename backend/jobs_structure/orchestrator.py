from supabase_client.config.create_jobs_config import (
    create_if_not_exist_film_job_config,
)
from supabase_client.config.job_type import JobType
from jobs_structure.status.job_status import JobStatus
from supabase_client.db import get_supabase

# TODO add error handling


def orchestrator(jobType):
    # Create job config if not exist
    create_if_not_exist_job_config(jobType)
    supabase = get_supabase()

    # Get job config
    config = get_job_type(jobType)

    # Insert the config to the job and get the jobId
    jobId = insert_config_id_to_job(config["id"])

    # Get items to process
    items = get_item_list(jobType)

    print("[Orchestrator]", len(items), "items to process")

    # Divide items into batches
    batches = []
    for i in range(0, len(items), config["batch_size"]):
        batches.append(items[i : i + config["batch_size"]])

    print(
        f"[Orchestrator] Created {len(batches)} batches of {config['batch_size']} items each"
    )

    # Update job with batch information
    supabase.table("jobs").update(
        {
            "status": JobStatus.RUNNING.value,
            "total_batches": len(batches),
            "total_items": len(items),
        }
    ).eq("id", jobId).execute()

    # Launch inital batches
    initial_batch_count = min(config["max_concurrency"], len(batches))
    for i in range(0, initial_batch_count):
        launch_batch(jobId, i, batches[i], config)
        
    return "success"


def create_if_not_exist_job_config(jobType):
    """Creates a job of the specified type if it does not already exist.

    Args:
        jobType: The type of job to create, typically an enum value from JobType.
    """
    if jobType == JobType.TMDB_FILM_DATA.value:
        create_if_not_exist_film_job_config()


def get_job_type(jobType):
    """Retrieves the job configuration for a specific job type.

    Args:
        jobType: The type of job to retrieve configuration for.

    Returns:
        dict: The job configuration for the specified job type.
    """
    supabase = get_supabase()
    jobType = (
        supabase.table("jobs_config").select("*").eq("job_type", jobType).execute()
    )
    return jobType.data[0]


def insert_config_id_to_job(config_id):
    """Inserts the job configuration ID into the job record.

    Args:
        config_id (str): The ID of the job configuration to insert.

    Returns:
        str: The ID of the job record that was updated.
    """
    supabase = get_supabase()
    response = supabase.table("jobs").insert({"job_config_id": config_id}).execute()
    return response.data[0]["id"]


def get_item_list(jobType):
    """Retrieves a list of items to process for a specific job type.

    Args:
        jobType: The type of job to retrieve items for.

    Returns:
        list: A list of items to process for the specified job type.
    """
    supabase = get_supabase()
    item_list = []
    if jobType == JobType.TMDB_FILM_DATA.value:
        item_list = supabase.table("films").select("id", "name", "year").execute()

    return item_list.data


def launch_batch(jobId, batchIndex, items, config):
    print("successsss" + str(batchIndex))