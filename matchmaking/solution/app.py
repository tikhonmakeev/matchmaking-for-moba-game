import logging
import requests

from pprint import pprint
from itertools import groupby

from match_methods import match_creator, create_Player_instances, formatting_multiple_matches_as_dict


logger = logging.getLogger(__name__)

# При локальном запуске http://server:8000 --> http://0.0.0.0:8000
if __name__ == "__main__":
    NUMBER_OF_TESTS = 20


    for cur_test_ind in range(NUMBER_OF_TESTS):
        is_last_epoch = last_epoch_finished = False
        cur_epoch = "00000000-0000-0000-0000-000000000000"
        players_in_queue_with_time = {}
        players_in_queue = []


        while not last_epoch_finished:
            # Вызов, который вернёт игроков, ожидающих матча
            response = requests.get(
                # Тут поменял название теста и порт на тестовый, вернуть перед пушем
                f'http://server:8000/matchmaking/users?test_name=test_{cur_test_ind}&epoch={cur_epoch}')
            logger.info(response.text)

            # Добавляем в очередь игроков сразу объектами класса Player
            players_in_queue.extend(create_Player_instances(response.json()))
            # print("SERVER RETURNED:")
            # pprint(response.json())


            res_epoch_matches = []


            # pivot_dict_by_userId = {}
            


                # pools_without_userId = player.copy()
                # pools_without_userId.pop('user_id')

                # pivot_dict_by_userId[player["user_id"]] = pools_without_userId


            # Пока в эпохе можно создать матч -- создаем

            sorted_userId_by_mmr = sorted(list(players_in_queue), key=lambda x: x.mmr)
            grouped_userId_by_mmr = groupby(sorted_userId_by_mmr, lambda x: x.mmr // 500)
            # grouped_userId_by_mmr = groupby(players_in_queue, lambda x: int(x["mmr"]) // ((sorted_userId_by_mmr[-1]["mmr"] - sorted_userId_by_mmr[0]["mmr"]) // 20))
                
            amount = 0
            for mmr_rank, group in grouped_userId_by_mmr:
                group = list(group)
                while len(group) > 10:
                    players_for_match = group[:10]
                    res_epoch_matches.append(match_creator(players_for_match))
                    group = group[10:]

                    for used_player in players_for_match:
                        players_in_queue.remove(used_player)

            while len(players_in_queue) > 10:
                players_for_match = players_in_queue[:10]
                res_epoch_matches.append(match_creator(players_for_match))
                players_in_queue = players_in_queue[10:]


                # Здесь нужно объяснение, как высчитывается "ХОРОШЕСТЬ" команды

                # Честность(*fairness*) матча = разница медиан между рейтингами команд + сумма разниц в mmr по ролям.
                
                # Предпочитаемая позиция = сумма значений удовлетворенности игроков
                # 3, если игрок на первой в списке
                # 5, если на второй в списке
                # 8, если на третьей в списке
                # 13, если на четвертой в списке
                # 21, если на пятой в списке

                # Скорость поиска = сумма всего времени ожидания, с учётом пауз между эпохами
                # Время считается в секундах
                # Паузы между эпохами разные и их значение вам не будет известно


                # ЗДЕСЬ ВАЖНО обработать случай, когда в моем "ранге" не хватает игроков на матч
                # думаю норм поискать игроков снизу, пока не взятых
                # if len(list(group)) < 10:
                
            # Вызов, который передаст составы матчей в проверяющую систему
            headers = {'Content-Type': 'application/json'}
            response = requests.post(
                f'http://server:8000/matchmaking/match?test_name=test_{cur_test_ind}&epoch={cur_epoch}',
                headers=headers,
                json=formatting_multiple_matches_as_dict(res_epoch_matches))
            
            logger.info(response.text)
            # print("SERVER RETURNED:")
            # pprint(response.json())

            if is_last_epoch:
                last_epoch_finished = True

            elif response.json()["is_last_epoch"] is True:
                is_last_epoch = True

            cur_epoch = response.json()["new_epoch"] if response.json()["new_epoch"] else None