# batch_results

```sql
CREATE TABLE batch_results (
    id BIGSERIAL PRIMARY KEY,
    batch_id BIGINT REFERENCES batches(id),
    result_id BIGINT, -- FK a films u otra entidad
    status TEXT CHECK (status IN ('success', 'failed')) NOT NULL,
    error_message TEXT,
    processing_time_ms INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```
