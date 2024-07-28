from logging import Logger
from requests import Response

from formatting_methods import players_format, matches_format_to_dict
from classes_with_methods import ten_player_match
from algorithm.rating_assignment import get_groups_by_rank


def compute_new_matches(get_response: Response, players_in_queue: list, logger: Logger):
    players_in_queue.extend(players_format(get_response, logger))
    res_epoch_matches = []

    # Пока в эпохе можно создать матч -- создаем
    for group in get_groups_by_rank(players_in_queue):

        while len(group) >= 10:
            players_for_match = group[:10]
            res_epoch_matches.append(ten_player_match(players_for_match))
            group = group[10:]

            for used_player in players_for_match:
                players_in_queue.remove(used_player)

    while len(players_in_queue) >= 10:
        players_for_match = players_in_queue[:10]
        res_epoch_matches.append(ten_player_match(players_for_match))
        players_in_queue = players_in_queue[10:]

    # ЗДЕСЬ ВАЖНО обработать случай, когда в моем "ранге" не хватает игроков на матч
    # думаю норм поискать игроков снизу, пока не взятых


    return matches_format_to_dict(res_epoch_matches)