import requests
from requests.exceptions import JSONDecodeError
from logging import Logger


def post_matches(uri: str, port: str, cur_test_ind: int, cur_epoch: int, matches: list, logger: Logger):
    """Передаст составы матчей в проверяющую систему
    
    Если вернул `None`, значит от серва пришел не json"""

    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(
            f'{uri}:{port}/matchmaking/match?test_name=test_{cur_test_ind}&epoch={cur_epoch}',
            headers=headers,
            json=matches)
    except Exception as e:
        logger.exception(e)

    try:
        response.json()
    except JSONDecodeError as e:
        print("Поймал не json`чик")
        logger.exception(e)
        return None
    
    return response