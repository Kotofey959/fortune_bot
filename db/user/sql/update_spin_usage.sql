UPDATE
    "user"
SET "spin_usage" = "spin_usage" + 1::integer
WHERE "telegram_id" = {{context.get("telegram_id")}}::bigint