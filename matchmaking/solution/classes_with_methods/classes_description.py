import uuid

class Player:
    def __init__(self, user_id: str, mmr: int, roles: list, waitingTime: int) -> None:
        self.user_id = user_id
        self.mmr = mmr
        self.roles = roles
        self.waitingTime = waitingTime


class Team:
    def __init__(self, side: str, users: list) -> None:
        self.side = side
        self.users = users


class Match:
    def __init__(self, team_red: Team, team_blue: Team) -> None:
        self.match_id = str(uuid.uuid4())
        self.team_red = team_red
        self.team_blue = team_blue


    def asdict(self):
        res_dict = {"match_id": self.match_id,
                    "teams": []}
        
        for team in ("team_blue", "team_red"):
            res_dict["teams"].append(self.__dict__[team].__dict__)
        return res_dict
