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
                t = 0
                coeff_a = ball_info.velocity.length_squared() - c.PLAYER_SPEED ** 2
                coeff_b = to_ball.dot(ball_info.velocity)
                coeff_c = to_ball.length_squared()

                discriminant = coeff_b ** 2 - coeff_a * coeff_c

                if abs(coeff_a) > 0.01 and discriminant >= 0:
                    t = (-coeff_b - discriminant ** 0.5) / coeff_a
                elif discriminant < 0:
                    t = 0
                else:
                    t = -coeff_c / (2 * coeff_b)

                t = min(max(0, t), 1)

                predicted_ball_pos = ball_info.pos + ball_info.velocity * t
                self.run(predicted_ball_pos)

            case State.DIFFENSE_RETURN:
                self.run(self.initial_pos)