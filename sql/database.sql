-- Create databeses
CREATE TABLE domain (
    domain_id SERIAL PRIMARY KEY,
    domain_name VARCHAR(255) NOT NULL,
    registered_at TIMESTAMP NOT NULL,
    unregistered_at TIMESTAMP NULL,
    CONSTRAINT unique_active_domain UNIQUE (domain_name, unregistered_at),
    CONSTRAINT check_unregistered_time CHECK (unregistered_at IS NULL OR registered_at < unregistered_at)
);

CREATE TABLE domain_flag (
    flag_id SERIAL PRIMARY KEY,
    domain_id INT NOT NULL REFERENCES domain(domain_id),
    flag_name VARCHAR(50) NOT NULL CHECK (flag_name IN ('EXPIRED', 'OUTZONE', 'DELETE_CANDIDATE')),
    valid_from TIMESTAMP NOT NULL,
    valid_to TIMESTAMP NULL,
    CONSTRAINT check_valid_time CHECK (valid_to IS NULL OR valid_from < valid_to)
);

-- Insert data

INSERT INTO domain (domain_name, registered_at) VALUES ('example.com', '2023-01-01 00:00:00');
INSERT INTO domain (domain_name, registered_at, unregistered_at) VALUES ('test.com', '2022-05-01 00:00:00', '2023-05-01 00:00:00');

INSERT INTO domain_flag (domain_id, flag_name, valid_from) VALUES (1, 'EXPIRED', '2024-01-01 00:00:00');
INSERT INTO domain_flag (domain_id, flag_name, valid_from, valid_to) VALUES (2, 'EXPIRED', '2022-05-01 00:00:00', '2023-04-30 23:59:59');
INSERT INTO domain_flag (domain_id, flag_name, valid_from, valid_to) VALUES (2, 'OUTZONE', '2022-06-01 00:00:00', '2023-03-01 00:00:00');

-- Queries
-- Domains that are currently registered and do not have an active EXPIRED flag
SELECT d.domain_name
FROM domain d
LEFT JOIN domain_flag df
    ON d.domain_id = df.domain_id
    AND df.flag_name = 'EXPIRED'
    AND (df.valid_to IS NOT NULL OR df.valid_to >= NOW())
    AND df.valid_from <= NOW()
WHERE d.unregistered_at IS NULL
    AND df.flag_id IS NULL;

-- Domains that had EXPIRED and OUTZONE flags in the past
SELECT DISTINCT d.domain_name
FROM domain d
JOIN domain_flag df_expired
    ON d.domain_id = df_expired.domain_id
    AND df_expired.flag_name = 'EXPIRED'
    AND df_expired.valid_to IS NOT NULL
JOIN domain_flag df_outzone
    ON d.domain_id = df_outzone.domain_id
    AND df_outzone.flag_name = 'OUTZONE'
    AND df_outzone.valid_to IS NOT NULL;