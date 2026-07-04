import pygame
import constants as c
import random

class Ball:
    def __init__(self, pos: pygame.math.Vector2) -> None:
        # ボールの現在位置と速度を保持する
        self.pos: pygame.math.Vector2 = pos
        self.velocity: pygame.math.Vector2 = pygame.math.Vector2(0, 0)

    def apply_kick_direction(self, direction:pygame.math.Vector2, power):
        power = min(power, c.MAX_BALL_SPEED)

        if direction.length_squared() > 0.01:
            self.velocity = direction.normalize() * power
        else:
            self.velocity = pygame.math.Vector2(0, 0)

        rrandom_angle = random.uniform(-1, 1)
        self.velocity.rotate(rrandom_angle)

    def apply_kick_target(self, target: pygame.math.Vector2, power: float):
        # 速すぎるキックを制限し、指定ターゲットへ速度を与える
        direction = target - self.pos
        
        self.apply_kick_direction(direction, power)


    def update(self, dt: float) -> None:
        # 摩擦を適用した後にボールを移動させる
        self.apply_friction(dt)
        self.pos += self.velocity * dt

    def apply_friction(self, dt: float) -> None:
        # 時間経過に応じてボールの速度を減衰させる
        speed_sq = self.velocity.length_squared()

        if speed_sq == 0:
            return

        speed = speed_sq ** 0.5
        deceleration = c.BALL_FRICTION_ACCEL * dt

        if speed < deceleration:
            self.velocity = pygame.math.Vector2(0, 0)
        else:
            self.velocity = self.velocity.normalize() * (speed - deceleration)
        
    def draw(self, screen: "pygame.Surface") -> None:
        pygame.draw.circle(screen, c.WHITE, (int(self.pos.x), int(self.pos.y)), c.BALL_RADIUS)

