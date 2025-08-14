from enum import Enum


class JobStatus(Enum):
    """Enumeration for job statuses.

    Args:
        Enum (enum.Enum): The base class for all enumerations.
    """

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    KILLED = "killed"
