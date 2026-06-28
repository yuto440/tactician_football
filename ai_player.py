from enum import Enum, auto
from player import *
from ball import *

class State(Enum):
    OFFENSE_CHASE = auto()
    DIFFENSE_RETURN = auto()
    BYPASS = auto()

class FSMPlayer(Player):
    def __init__(self, pos):
        super().__init__(pos)
        self.state = State.DIFFENSE_RETURN
        

    def think(self, ball_info, player_infos) -> None:
        to_ball = ball_info.pos - self.pos
        dist_to_ball_sq = to_ball.length_squared()

        #チームの中で一番ボールに近くなければDIFFENSE_RETURN
        self.state = State.OFFENSE_CHASE
        for player in player_infos:
            if player.team_id == self.team_id:
                player_to_ball = ball_info.pos - player.pos
                dist_player_to_ball_sq = player_to_ball.length_squared()
                if dist_player_to_ball_sq < dist_to_ball_sq:
                    self.state = State.DIFFENSE_RETURN
                    break


        match self.state:
            case State.OFFENSE_CHASE:#ボールを追いかける
                t = 0.0
                ball_speed = ball_info.velocity.length()
                if dist_to_ball_sq > 0 and ball_speed > 0:
                    n_to_ball = to_ball.normalize()
                    n_ball_speed = ball_info.velocity.normalize()
                    moving_away_rate = n_ball_speed.dot(n_to_ball)

                    t = (1 + moving_away_rate) * ball_speed / c.PLAYER_SPEED * 0.8

                predicted_ball_pos = ball_info.pos + ball_info.velocity * t
                to_target = predicted_ball_pos - self.pos
                if to_target.length_squared() > 0:
                    self.velocity = to_target.normalize() * c.PLAYER_SPEED

            case State.DIFFENSE_RETURN:
                to_home = self.initial_pos - self.pos
                if to_home.length_squared() > (c.PLAYER_SPEED / c.FPS) ** 2:
                    n_to_home = to_home.normalize()
                    self.velocity = c.PLAYER_SPEED * n_to_home
                else:
                    self.pos = pygame.math.Vector2(self.initial_pos)
                    self.velocity = pygame.math.Vector2(0, 0)