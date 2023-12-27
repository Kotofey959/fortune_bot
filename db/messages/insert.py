"""
Добавление записи в таблицу User.
"""

from db.messages.sql import MessagesTemplate


def get_insert_template(
        user_id: int,
        message_id: int,
        forwarded_message_id: int,
):
    template = MessagesTemplate.insert
    context = {"user_id": user_id,
               "message_id": message_id,
               "forwarded_message_id": forwarded_message_id}

    return template.render(context)
