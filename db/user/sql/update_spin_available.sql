UPDATE
    "user"
SET "spin_available" = "spin_available" + {{context.get("count_spin")}}::integer
WHERE "telegram_id" = {{context.get("telegram_id")}}::bigint
