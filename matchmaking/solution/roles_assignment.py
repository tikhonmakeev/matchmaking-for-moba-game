from scipy.optimize import linear_sum_assignment
from numpy import ndarray, asarray


ROLES_LIST = ['mid', 'sup', 'top', 'bot', 'jungle']
ROLES_POSITIONS_COST = {
                        "0":3,
                        "1":5,
                        "2":8,
                        "3":13,
                        "4":21
                        }


def create_cost_matrix(players: list) -> ndarray:
    """Возвращает массив стоимости выбора разных ролей по каждому игроку"""
    
    res = []
    for player in players:

        # Для каждого игрока создаем словарь ценности каждой роли
        player_costs_by_role = {}
        for ind, role in enumerate(player.roles):
            player_costs_by_role[role] = ROLES_POSITIONS_COST[str(ind)]
            
        # В итоговый массив добавляем в строгом порядке списка ролей
        res.append([player_costs_by_role[x] for x in ROLES_LIST * 2])

    return(asarray(res))


def assign_roles_by_cost(cost_matrix: ndarray) -> ndarray:
    """Принимает решения по роялм при помощи Венгерского алгоритма,
    
        минимизируя суммарные траты критерия на матч"""
    
    # Алгорит находит минимальное соответствие весов в двудольных графах
    grad_idx, role_idx = linear_sum_assignment(cost_matrix)

    if sorted(grad_idx.tolist()) != grad_idx.tolist():
        print("Игроки пришли не в надлежащем порядке!")
        role_idx, grad_idx = zip(*sorted(zip(grad_idx.tolist(), role_idx.tolist())))

        role_idx = asarray(role_idx)

    return role_idx


def assign_roles_in_match(players: list) -> list:
    """Назначает роли каждому игроку в матче(из 10 человек)"""
    
    cost_matrix = create_cost_matrix(players)
    role_idx = assign_roles_by_cost(cost_matrix)

    roles_by_player = []
    for role in role_idx:
        if role > 4:
            role -= 5
        roles_by_player.append(ROLES_LIST[role])

    return roles_by_player
