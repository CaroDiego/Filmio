# batches

```sql
CREATE TABLE batches (
    id BIGSERIAL PRIMARY KEY,
    job_id BIGINT REFERENCES jobs(id),
    batch_number INT NOT NULL,
    status TEXT CHECK (status IN ('pending', 'running', 'completed', 'failed')) NOT NULL DEFAULT 'pending',
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    total_items INT DEFAULT 0,
    processed_items INT DEFAULT 0,
    successful_items INT DEFAULT 0,
    failed_items INT DEFAULT 0,
    summary JSONB, -- { "avg_time_per_result": 1.23, "error_count": 3, "processing_time": 10.5, "rows_inserted": 45 }
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```
