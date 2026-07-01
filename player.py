from __future__ import annotations

import pygame
import constants as c
from ball import *
from typing import Any

class Player:
    def __init__(self, pos: pygame.math.Vector2, field_rect) -> None:
        self.pos: pygame.math.Vector2 = pos
        self.initial_pos: pygame.math.Vector2 = pygame.math.Vector2(pos)

        self.velocity: pygame.math.Vector2 = pygame.math.Vector2(0, 0)

        self.angle: float = 0.0

        self.turn_speed: float = 0

        self.team_id: c.TeamID = None
        self.goal_pos_x: int = None

        self.field_rect: pygame.rect = field_rect

        self.color: tuple[int, int, int] = c.BLACK

        self.kick_cool_time: float = 0.0

    def reset(self) -> None:
        self.pos = pygame.math.Vector2(self.initial_pos)
        self.velocity = pygame.math.Vector2(0, 0)
        if self.goal_pos_x is not None:
            goal_dir = pygame.math.Vector2(self.goal_pos_x, self.pos.y) - self.pos
            _, self.angle = goal_dir.as_polar()
        self.kick_cool_time = 0

    def can_kick(self, ball_interface: BallInferface) -> bool:
        to_ball = ball_interface.pos - self.pos
        dist_to_ball_sq = to_ball.length_squared()
        reach_magin = 3.0
        min_dist_sq = (c.BALL_RADIUS + c.PLAYER_RADIUS + reach_magin) ** 2

        return dist_to_ball_sq < min_dist_sq * 1.1 and self.kick_cool_time <= 0
    
    def kick(self, ball_interface: BallInferface, target: pygame.math.Vector2, power: float) -> bool:
        if self.can_kick(ball_interface):
            ball_interface.apply_kick(target, power)
            self.kick_cool_time = 1.0


    def run(self, target_pos: pygame.math.Vector2):
        self.turn_towards(target_pos)
        to_target_pos = target_pos - self.pos
        distance_sq = to_target_pos.length_squared()

        if distance_sq < 2:
            self.velocity = pygame.math.Vector2(0, 0)
            return

        #目的地方向を向いているか判定
        dir_vector = pygame.math.Vector2(1, 0).rotate(self.angle)
        target_dir = to_target_pos.normalize()
        front_factor = dir_vector.dot(target_dir)

        if front_factor > 0.95:
            current_speed = c.PLAYER_SPEED
        else:
            current_speed = c.PLAYER_SPEED * 0.2

        self.velocity = target_dir * current_speed

    def turn_towards(self, target:pygame.math.Vector2):
        to_target = target - self.pos

        if to_target.length_squared() < 0.01:
            self.turn_speed = 0.0
            return 0.0
        
        current_dir = pygame.math.Vector2(1, 0).rotate(self.angle)

        angle_diff = current_dir.angle_to(to_target)

        angle_diff = (angle_diff - 180) % 360 -180
        

        if angle_diff > 0.1:
            self.turn_speed = c.PLAYER_TURN_SPEED
        elif angle_diff < -0.1:
            self.turn_speed = -c.PLAYER_TURN_SPEED
        else:
            self.turn_speed = 0.0

        return angle_diff




    def think(self, ball_interface: BallInferface, player_infos: list[PlayerInfo]) -> None:
        self.run(ball_interface.pos)
        goal_pos = pygame.math.Vector2(self.goal_pos_x, self.field_rect.centery)
        self.kick(ball_interface, goal_pos, c.MAX_BALL_SPEED)

    def update_ai(self, ball_interface: BallInferface, player_infos: list[PlayerInfo]):
        self.think(ball_interface, player_infos)

    def update(self, dt: float) -> None:
        if self.kick_cool_time > 0.0:
            self.kick_cool_time = max(0.0, self.kick_cool_time - dt)

        self.pos += self.velocity * dt
        self.angle += self.turn_speed * dt

        self.angle = (self.angle + 180) % 360 - 180


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