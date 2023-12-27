SELECT
    "user_id", "message_id"
FROM
    "messages"
WHERE
    "forwarded_message_id"::integer = {{forwarded_message_id}}::integer