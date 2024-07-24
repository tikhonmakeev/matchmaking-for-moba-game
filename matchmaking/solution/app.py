import logging
import requests

logger = logging.getLogger(__name__)

# При локальном запуске http://server:8000 --> http://0.0.0.0:8000
if __name__ == "__main__":
    # Вызов, который вернёт игроков, ожидающих матча
    response = requests.get(
        'http://server:8000/matchmaking/users?test_name=test_0&epoch=00000000-0000-0000-0000-000000000000')
    logger.info(response.text)

    # Вызов, который передаст составы матчей в проверяющую систему
    headers = {'Content-Type': 'application/json'}
    response = requests.post(
        'http://server:8000/matchmaking/match?test_name=test_0&epoch=00000000-0000-0000-0000-000000000000',
        headers=headers,
        json={"example": "data"})
    logger.info(response.text)
