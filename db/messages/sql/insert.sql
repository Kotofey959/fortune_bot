INSERT INTO
    "messages" ("user_id", "message_id", "forwarded_message_id")
VALUES
    ({{ user_id }}::bigint,
     {{ message_id }}::integer,
     {{ forwarded_message_id }}::integer
    )