from itertools import groupby


def get_groups_by_rank(players: list) -> list:
    sorted_userId_by_mmr = sorted(list(players), key=lambda x: x.mmr)
    grouped_userId_by_mmr = groupby(sorted_userId_by_mmr, lambda x: x.mmr // 500)
    # grouped_userId_by_mmr = groupby(players, lambda x: int(x["mmr"]) // ((sorted_userId_by_mmr[-1]["mmr"] - sorted_userId_by_mmr[0]["mmr"]) // 20))

    groups = [list(x[1]) for x in grouped_userId_by_mmr]

    return groups