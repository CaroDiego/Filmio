import math
from jobs_structure.status.batch_status import BatchStatus
from supabase_client.config.create_jobs_config import (
    create_if_not_exist_film_job_config,
)
from supabase_client.config.job_type import JobType
from jobs_structure.status.job_status import JobStatus
from supabase_client.db import get_supabase
from datetime import datetime, timezone

# TODO add error handling


def orchestrator(jobType):
    """Creates a new job of the specified type, divide items into batches and manage batch processing.

    Args:
        jobType (str): The type of job to create, typically an enum value from JobType.
    """
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


def launch_batch(jobId, batchNumber, items, config):
    supabase = get_supabase()
    jobDoc = supabase.table("jobs").select("*").eq("id", jobId).execute()
    jobData = jobDoc.data[0]

    if jobData["is_killed"]:
        print("[Orchestrator] Job was killed, won't trigger new batches")
        supabase.table("jobs").update(
            {
                "status": JobStatus.KILLED.value,
                "stopped_at": datetime.now(timezone.utc).isoformat(),
            }
        ).eq("id", jobId).execute()
    else:
        # Create Batch
        newBatch = (
            supabase.table("batches")
            .insert(
                {
                    "job_id": jobId,
                    "batch_number": batchNumber,
                    "status": BatchStatus.RUNNING.value,
                    "total_items": len(items),
                }
            )
            .execute()
        )

        batchId = newBatch.data[0]["id"]

        supabase.table("jobs").update(
            {
                "active_batches": jobData["active_batches"] + 1,
            }
        ).eq("id", jobId).execute()

        totalBatches = math.ceil(len(items) / config["batch_size"])
        processChildTask(jobId, batchId, batchNumber, totalBatches, items, config)

        print(
            f"[Orchestrator] Launched batch {batchNumber + 1}/{totalBatches} for job {jobId}"
        )
