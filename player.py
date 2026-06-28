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

        self.angle: float = 0.0

        self.team_id: c.TeamID = None
        self.goal_pos_x: int = None

        self.color: tuple[int, int, int] = c.BLACK

        self.knockback_timer: float = 0.0

    def reset(self) -> None:
        self.pos = pygame.math.Vector2(self.initial_pos)
        self.velocity = pygame.math.Vector2(0, 0)
        self.angle = 0.0
        self.knockback_timer = 0

    def run(self, target_pos: pygame.math.Vector2):
        to_target_pos = target_pos - self.pos
        distance, to_target_angle = to_target_pos.as_polar()

        if distance < 2:
            self.velocity = pygame.math.Vector2(0, 0)
            return
        
        self.angle = to_target_angle

        #目的地方向を向いているか判定
        dir_vector = pygame.math.Vector2(1, 0).rotate(self.angle)
        target_dir = to_target_pos.normalize()
        front_factor = dir_vector.dot(target_dir)

        if front_factor > 0.95:
            current_speed = c.PLAYER_SPEED
        else:
            current_speed = c.PLAYER_SPEED * 0.2

        self.velocity = target_dir * current_speed
        


    def think(self, ball_info: BallInfo, player_infos: list[PlayerInfo]) -> None:
        self.run(ball_info.pos)

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

        #腕の表示
        direction_vector = pygame.math.Vector2(1, 0).rotate(self.angle)
        right_arm_vector = direction_vector.rotate(70.0)
        left_arm_vector = direction_vector.rotate(-70.0)

        line_len = c.PLAYER_RADIUS * 1.3
        right_end_pos = self.pos + right_arm_vector * line_len
        left_end_pos = self.pos + left_arm_vector * line_len

        pygame.draw.line(screen, c.BLACK, (int(self.pos.x), int(self.pos.y)), (int(right_end_pos.x), int(right_end_pos.y)), 3)
        pygame.draw.line(screen, c.BLACK, (int(self.pos.x), int(self.pos.y)), (int(left_end_pos.x), int(left_end_pos.y)), 3)



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