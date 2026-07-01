from enum import Enum, auto
from player import *
from ball import *

class State(Enum):
    OFFENSE_CHASE = auto()
    DIFFENSE_RETURN = auto()
    BYPASS = auto()

class FSMPlayer(Player):
    def __init__(self, pos, field_rect: pygame.rect):
        super().__init__(pos, field_rect)
        self.state = State.DIFFENSE_RETURN
        

    def think(self, ball_interface, player_infos) -> None:
        if self.can_kick(ball_interface):
            my_direction = pygame.math.Vector2(1, 0).rotate(self.angle)
            rand_angle = random.randint(-70, 70)
            ball_direction = my_direction.rotate(rand_angle)
            ball_target = ball_direction * 100 + self.pos
            self.kick(ball_interface, ball_target, c.MAX_BALL_SPEED)
            
        to_ball = ball_interface.pos - self.pos
        dist_to_ball_sq = to_ball.length_squared()

        #チームの中で一番ボールに近くなければDIFFENSE_RETURN
        self.state = State.OFFENSE_CHASE
        for player in player_infos:
            if player.team_id == self.team_id:
                player_to_ball = ball_interface.pos - player.pos
                dist_player_to_ball_sq = player_to_ball.length_squared()
                if dist_player_to_ball_sq < dist_to_ball_sq:
                    self.state = State.DIFFENSE_RETURN
                    break


        match self.state:
            case State.OFFENSE_CHASE:#ボールを追いかける
                t = 0
                coeff_a = ball_interface.velocity.length_squared() - c.PLAYER_SPEED ** 2
                coeff_b = to_ball.dot(ball_interface.velocity)
                coeff_c = to_ball.length_squared()

                discriminant = coeff_b ** 2 - coeff_a * coeff_c

                if abs(coeff_a) > 0.01 and discriminant >= 0:
                    t = (-coeff_b - discriminant ** 0.5) / coeff_a
                elif discriminant < 0:
                    t = 0
                else:
                    t = -coeff_c / (2 * coeff_b)

                t = min(max(0, t), 1)

                predicted_ball_pos = ball_interface.pos + ball_interface.velocity * t
                self.run(predicted_ball_pos)

            case State.DIFFENSE_RETURN:
                self.run(self.initial_pos)