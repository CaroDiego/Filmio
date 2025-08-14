# jobs

```sql
CREATE TABLE jobs (
    id BIGSERIAL PRIMARY KEY,
    job_config_id BIGINT REFERENCES jobs_config(id),
    is_killed BOOLEAN DEFAULT FALSE,
    status TEXT CHECK (status IN ('pending', 'running', 'completed', 'failed', 'killed')) NOT NULL DEFAULT 'pending',
    total_batches INT DEFAULT 0,
    active_batches INT DEFAULT 0,
    completed_batches INT DEFAULT 0,
    failed_batches INT DEFAULT 0,
    total_items INT DEFAULT 0,
    successful_items INT DEFAULT 0,
    failed_items INT DEFAULT 0,
    processed_items INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
)
```
