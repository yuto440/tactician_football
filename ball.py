import pygame
import constants as c

class Ball:
    def __init__(self, pos: pygame.math.Vector2) -> None:
        self.pos: pygame.math.Vector2 = pos
        self.velocity: pygame.math.Vector2 = pygame.math.Vector2(0, 0)

    def update(self, dt: float) -> None:
        self.apply_friction(dt)
        self.pos += self.velocity * dt

    def apply_friction(self, dt: float) -> None:
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


class BallInfo:
    def __init__(self, ball: Ball):
        self._ball = ball

    @property
    def pos(self):
        return self._ball.pos
    
    @property
    def velocity(self):
        return self._ball.velocity