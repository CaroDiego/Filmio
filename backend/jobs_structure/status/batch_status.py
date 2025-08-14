from enum import Enum


class BatchStatus(Enum):
    """Enumeration for batch statuses.

    Args:
        Enum (enum.Enum): The base class for all enumerations.
    """
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
