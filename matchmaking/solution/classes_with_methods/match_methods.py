from algorithm.roles_assignment import assign_roles_in_match
from classes_with_methods.classes_description import Team, Player, Match


def teams_creator(players: list) -> dict:
    """Создает команды из списка игроков
    
    Возвращает словарь: team_red, team_blue"""

    # Получает распределение игроков по ролям
    roles_of_players = assign_roles_in_match(players)

    # Будущие команды 
    red_team = Team("red", [])
    blue_team = Team("blue", [])

    already_taken_roles = set()
    for player, role in zip(players, roles_of_players):
        # Создаем из игрока словарь нужного формата 
        user_of_player = {"id": player.user_id, "role": role}

        # Если его роль свободна в команде красных, туда его
        # Иначе в синюю
        if role in already_taken_roles:
            blue_team.users.append(user_of_player)
        else:
            red_team.users.append(user_of_player)
            already_taken_roles.add(role)
    
    return {"team_red": red_team, "team_blue": blue_team}


def ten_player_match(players: list) -> Match:
    """Создает матч из списка игроков(10 человек)
    
    Если их больше -- вернет `None`"""
    
    if len(players) != 10:
        return None
    
    teams = teams_creator(players)

    return Match(team_red=teams["team_red"], team_blue=teams["team_blue"])
