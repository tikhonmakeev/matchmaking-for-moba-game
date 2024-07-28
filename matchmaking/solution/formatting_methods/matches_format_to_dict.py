from classes_with_methods.classes_description import Match


def matches_format_to_dict(matches: list) -> list:
    """Представляет объекты класса Match словарями нужного для api формата"""

    return list(map(Match.asdict, matches))
