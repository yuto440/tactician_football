from __future__ import annotations

from typing import List, Tuple
import pygame
from player import Player
import constants as c


class Team:
    def __init__(self, team_id: c.TeamID, goal_pos: pygame.math.Vector2, color: Tuple[int, int, int]) -> None:
        # チームごとのゴール位置・得点・所属プレイヤーを管理する
        self.team_id: c.TeamID = team_id
        self.goal_pos: pygame.math.Vector2 = goal_pos
        self.score: int = 0
        self.players: List[Player] = []
        self.color: Tuple[int, int, int] = color

    def add_player(self, player: Player) -> None:
        # プレイヤーをチームに登録し、色やゴール位置を設定する
        self.players.append(player)
        player.color = self.color
        player.team_id = self.team_id
        player.goal_pos = self.goal_pos