# batches

```sql
CREATE TABLE batches (
    id BIGSERIAL PRIMARY KEY,
    job_id BIGINT REFERENCES jobs(id),
    batch_number INT NOT NULL,
    status TEXT CHECK (status IN ('pending', 'running', 'completed', 'failed')) NOT NULL DEFAULT 'pending',
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP,
    total_items INT DEFAULT 0,
    processed_items INT DEFAULT 0,
    successful_items INT DEFAULT 0,
    failed_items INT DEFAULT 0,
    summary JSONB, -- { "avg_time_per_result": 1.23, "error_count": 3, "processing_time": 10.5, "rows_inserted": 45 }
    updated_at timestamptz DEFAULT now() NOT NULL
)


-- Trigger function to update updated_at timestamp on update
CREATE OR REPLACE FUNCTION update_batches_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_batches_updated_at
BEFORE UPDATE ON batches
FOR EACH ROW
EXECUTE FUNCTION update_batches_updated_at();
```
