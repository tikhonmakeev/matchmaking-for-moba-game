from itertools import groupby


def get_groups_by_rank(players: list) -> list:
    sorted_userId_by_mmr = sorted(list(players), key=lambda x: x.mmr)
    grouped_userId_by_mmr = groupby(sorted_userId_by_mmr, lambda x: x.mmr // 400)

    groups = [list(x[1]) for x in grouped_userId_by_mmr]

    return groups