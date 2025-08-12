# Films

 Holds unique film entries

```sql
-- Table for unique films
CREATE TABLE films (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name text NOT NULL,
    year int,
    created_at timestamptz DEFAULT now() NOT NULL,
    updated_at timestamptz DEFAULT now() NOT NULL
);

-- Trigger function to update updated_at timestamp on update
CREATE OR REPLACE FUNCTION update_films_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_films_updated_at
BEFORE UPDATE ON films
FOR EACH ROW
EXECUTE FUNCTION update_films_updated_at();
```
