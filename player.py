from __future__ import annotations

import pygame
import constants as c
from ball import *
from typing import Any

class Player:
    def __init__(self, pos: pygame.math.Vector2) -> None:
        self.pos: pygame.math.Vector2 = pos
        self.initial_pos: pygame.math.Vector2 = pygame.math.Vector2(pos)

        self.velocity: pygame.math.Vector2 = pygame.math.Vector2(0, 0)

        self.team_id: c.TeamID = None
        self.goal_pos_x: int = None

        self.color: tuple[int, int, int] = c.BLACK

        self.knockback_timer: float = 0.0

    def reset(self) -> None:
        self.pos = pygame.math.Vector2(self.initial_pos)
        self.velocity = pygame.math.Vector2(0, 0)
        self.knockback_timer = 0

    def think(self, ball_info: BallInfo, player_infos: list[PlayerInfo]) -> None:
        to_ball = ball_info.pos - self.pos

        if to_ball.length_squared() > 0:
            self.velocity = to_ball.normalize() * c.PLAYER_SPEED

    def trigger_knockback(self, n_player_to_ball: pygame.math.Vector2) -> None:
        self.knockback_timer = 0.5  # 0.5秒間ノックバック
        self.velocity = -n_player_to_ball * c.PLAYER_SPEED

    def update_ai(self, ball_info: BallInfo, player_infos: list[PlayerInfo]):
        if self.knockback_timer == 0:
            self.think(ball_info, player_infos)

    def update(self, dt: float) -> None:
        if self.knockback_timer > 0.0:
            self.knockback_timer = max(0.0, self.knockback_timer - dt)

        self.pos += self.velocity * dt


    def draw(self, screen: Any) -> None:
        pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), c.PLAYER_RADIUS)


class PlayerInfo:
    def __init__(self, player: Player):
        self._player = player

    @property
    def pos(self):
        return self._player.pos
    
    @property
    def velocity(self):
        return self._player.velocity
    
    @property
    def team_id(self):
        return self._player.team_id