# jobs_config

```sql
CREATE TABLE jobs_config (
    id BIGSERIAL PRIMARY KEY,
    job_type TEXT NOT NULL,
    batch_size INT NOT NULL DEFAULT 50,
    max_concurrency INT NOT NULL DEFAULT 4,
    max_retries INT NOT NULL DEFAULT 3,
    retry_delay_ms INT NOT NULL DEFAULT 5000,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```
