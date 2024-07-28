from itertools import groupby


def get_groups_by_rank(players: list) -> list:
    """Распределяет игроков в очереди на `ранги` по 400 единиц рейтинга на каждый"""

    # Сортирует игроков
    sorted_userId_by_mmr = sorted(list(players), key=lambda x: x.mmr)
    # Группирует на 'ранги'
    grouped_userId_by_mmr = groupby(sorted_userId_by_mmr, lambda x: x.mmr // 400)

    groups = [list(x[1]) for x in grouped_userId_by_mmr]

    return groups