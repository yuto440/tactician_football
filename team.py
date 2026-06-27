from __future__ import annotations

from typing import List, Tuple

from player import Player
import constants as c


class Team:
    def __init__(self, team_id: c.TeamID, goal_pos_x: int, color: Tuple[int, int, int]) -> None:
        self.team_id: c.TeamID = team_id
        self.goal_pos_x: int =goal_pos_x
        self.score: int = 0
        self.players: List[Player] = []
        self.color: Tuple[int, int, int] = color

    def add_player(self, player: Player) -> None:
        self.players.append(player)
        player.color = self.color
        player.team_id = self.team_id
        player.goal_pos_x = self.goal_pos_x