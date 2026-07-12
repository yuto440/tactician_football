from team import Team
from infos import *

 #プレイヤーの判断に用いる情報を計算し、保持する。
class MatchAnalysis:
    def __init__(self, teams: list[Team], ball_info: BallInfo, player_infos: list[PlayerInfo]):
        self.teams: list[Team] = teams
        self.ball_info: BallInfo = ball_info
        self.player_infos: list[PlayerInfo] = player_infos
        self.player_info_dict = {p.player_id: p for p in self.player_infos}

        self.player_to_ball_vectors = {}#{player_id: (player_info, vector2)}

        self.ball_proximity_ranking = []#[(player_info, distance)]
        self.ball_proximity_list_by_id = {}#{player_id: (player_info, distance)}
        self.ball_proximity_ranking_by_team = {team.team_id: [] for team in self.teams}#{team_id:[(player_info, distance)]}

        

    def update(self):
        raw_list = []
        for player_info in self.player_infos:
            #print(player_info.player_id)
            p_to_b = self.ball_info.pos - player_info.pos
            self.player_to_ball_vectors[player_info.player_id] = (player_info, p_to_b)
            distanse_sq = p_to_b.length_squared()
            raw_list.append((player_info, distanse_sq))

        raw_list.sort(key=lambda x: x[1])
        self.ball_proximity_ranking = raw_list

        self.ball_proximity_list_by_id = {
            p.player_id: (p, distanse_sq) for p, distanse_sq in self.ball_proximity_ranking
        }

        for team in self.teams:
            self.ball_proximity_ranking_by_team[team.team_id] = []

        for info, dist_sq in raw_list:
            self.ball_proximity_ranking_by_team[info.team_id].append((info, dist_sq))