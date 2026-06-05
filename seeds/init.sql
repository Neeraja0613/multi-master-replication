CREATE TABLE product_catalog (
    id UUID PRIMARY KEY,
    name VARCHAR(255),
    price NUMERIC,
    vector_clock JSONB,
    last_updated_by VARCHAR(10),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE conflict_log (
    log_id SERIAL PRIMARY KEY,
    product_id UUID,
    winning_version JSONB,
    losing_version JSONB,
    resolved_by_node VARCHAR(10),
    detected_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO product_catalog VALUES
('11111111-1111-1111-1111-111111111111', 'Laptop', 500,
 '{"us":1,"eu":0,"apac":0}', 'us', NOW());