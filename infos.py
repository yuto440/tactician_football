from player import Player
from ball import Ball
import pygame


class PlayerInfo:
    def __init__(self, player: Player):
        self._player = player

    @property
    def player_id(self):
        return self._player.player_id

    @property
    def pos(self):
        return self._player.pos
    
    @property
    def velocity(self):
        return self._player.velocity
    
    @property
    def team_id(self):
        return self._player.team_id
    
    
class BallInterface:
    def __init__(self, ball: Ball):
        self._ball = ball

    @property
    def pos(self):
        return self._ball.pos.copy()
    
    @property
    def velocity(self):
        return self._ball.velocity.copy()
    
    def apply_kick(self, target:pygame.math.Vector2, power: float):
        self._ball.apply_kick(target, power)