from requests import Response
from requests.exceptions import JSONDecodeError
from logging import Logger

from classes_with_methods.classes_description import Player


def players_format(response: Response, logger: Logger) -> list:
    """Из Response делает список объектов класса Player"""

    # Сначала убедимся, что пришел корректный json
    try:
        response.json()
    except JSONDecodeError as e:
        print("Поймал не json`чик")
        logger.exception(e)
        return []
    
    players_instances = []
    for player in response.json():
        if not isinstance(player, dict):
            print("Выброс игрока, скип")
            continue
        player_instance = Player(player["user_id"], int(player["mmr"]), player["roles"], int(player["waitingTime"]))
        players_instances.append(player_instance)

    return players_instances
