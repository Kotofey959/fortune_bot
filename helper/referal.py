"""
Вспомогательные реферальные методы

"""


def split_ref_link(link: str) -> str or None:
    """
    Разбиваем реферальную строку

    :param link:
    :return:
    """
    if not link:
        return
    return link.split("t.me/+")[1]


def build_ref_link(bd_link: str) -> str or None:
    """
    Собираем строку для отправки пользователю
    :param bd_link:
    :return:
    """
    if not bd_link:
        return
    return f"https://t.me/+{bd_link}"
