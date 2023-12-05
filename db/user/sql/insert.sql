INSERT INTO
    "user" ("telegram_id", "spin_available", "spin_usage", "ref_link")
VALUES
    ({{ telegram_id }}::bigint,
     {{ spin_available }}::integer,
     {{ spin_usage }},
     '{{ ref_link }}'::text
    )
ON CONFLICT ("telegram_id") DO NOTHING
RETURNING
    "id"