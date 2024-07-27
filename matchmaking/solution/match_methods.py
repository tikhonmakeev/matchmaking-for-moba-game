from pprint import pprint
from roles_assignment import assign_roles_in_match
from classes_description import Team, Player, Match


def create_Player_instances(players: list) -> list:
    """Создает из словарей объекты класса Player"""

    players_instances = []
    for player in players:
        if not isinstance(player, dict):
            print("Выброс игрока, скип")
            continue
        player_instance = Player(player["user_id"], int(player["mmr"]), player["roles"], int(player["waitingTime"]))
        players_instances.append(player_instance)

    return players_instances


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


def match_creator(players: list) -> Match:
    """Создает матч из списка игроков(10 человек)
    
    Если их больше -- вернет `None`"""
    
    if len(players) != 10:
        return None
    
    teams = teams_creator(players)

    return Match(team_red=teams["team_red"], team_blue=teams["team_blue"])


def formatting_multiple_matches_as_dict(matches: list) -> list:
    """Представляет объекты класса Match словарями нужного формата"""

    return list(map(Match.asdict, matches))
