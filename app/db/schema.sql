CREATE TABLE IF NOT EXISTS cocktails (
    id BIGSERIAL PRIMARY KEY,
    source TEXT NOT NULL,
    source_url TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    description TEXT,
    image_url TEXT,
    glass TEXT,
    garnish TEXT,
    method TEXT,
    parse_status TEXT NOT NULL CHECK (parse_status IN ('ok', 'partial', 'failed')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ingredients (
    id BIGSERIAL PRIMARY KEY,
    cocktail_id BIGINT NOT NULL REFERENCES cocktails(id) ON DELETE CASCADE,
    position INT NOT NULL CHECK (position > 0),
    raw TEXT NOT NULL,
    amount NUMERIC CHECK (amount > 0),
    unit TEXT,
    name TEXT,
    comment TEXT,
    unresolved BOOLEAN NOT NULL DEFAULT FALSE,
    UNIQUE (cocktail_id, position)
);

