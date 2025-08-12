
# Viewings

Logs watch records, its linked to films

```sql
-- Table for each viewing of a film
CREATE TABLE viewings (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    film_id bigint NOT NULL REFERENCES films(id) ON DELETE CASCADE,
    rating numeric(2,1) CHECK (
        rating >= 0.5 AND rating <= 5.0 AND (rating * 2) = floor(rating * 2)
    ),
    watched_date date NOT NULL,
    liked boolean DEFAULT false,
    created_at timestamptz DEFAULT now() NOT NULL
);
```
