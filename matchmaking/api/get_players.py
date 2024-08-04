import requests
from requests import Response
from logging import Logger

def get_request(uri: str, port: str, cur_test_ind: int, cur_epoch:int , logger: Logger) -> Response:
    """Вернёт json игроков, ожидающих матча по тесту и эпохе"""

    try:
        response = requests.get(
            f'{uri}:{port}/matchmaking/users?test_name=test_{cur_test_ind}&epoch={cur_epoch}')
    except Exception as e:
        logger.exception(e)
    
    return response