SELECT
    "id", "telegram_id", "spin_available", "spin_usage", "ref_link"
FROM
    "user"
{% if params %}
WHERE
    {% for name, value in params.items() %}
        {% if name == "id" %}
        "id"::integer = {{value}}::integer
        {% endif %}
        {% if name == "telegram_id" %}
        "telegram_id" = {{value}}
        {% endif %}
        {% if name == "ref_link" %}
        "ref_link"::text = '{{value}}'::text
        {% endif %}
        {% if not loop.last %} AND {% endif -%}
    {% endfor %}
{% endif %}
