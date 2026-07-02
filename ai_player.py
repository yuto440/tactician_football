from enum import Enum, auto
from player import *
from ball import *

# AIプレイヤーの行動状態を定義する
class MovingState(Enum):
    OFFENSE_CHASE = auto()
    DIFFENSE_RETURN = auto()
    BYPASS = auto()

class KickingState(Enum):
    SHOT = auto()

class FSMPlayer(Player):
    def __init__(self, pos, field_rect: pygame.rect):
        super().__init__(pos, field_rect)
        # まずは守備に戻る状態から始める
        self.moving_state:MovingState = MovingState.DIFFENSE_RETURN
        self.Kicking_state:KickingState = None
        

    def think(self, ball_interface, player_infos) -> None:
        to_goal = self.goal_pos - self.pos
        dist_to_goal_sq = to_goal.length_squared()
        if self.Kicking_state == None:
            if dist_to_goal_sq < 90000:
                self.Kicking_state = KickingState.SHOT
            else:
                self.Kicking_state = None
        elif self.Kicking_state == KickingState.SHOT:
            if dist_to_goal_sq > 96100:
                self.Kicking_state = None

        if self.can_kick(ball_interface):
            match self.Kicking_state:
                case KickingState.SHOT:
                    self.kick(ball_interface, self.goal_pos, c.MAX_BALL_SPEED)
                    print(f"{self.team_id.name} shot!!")
                case None:
                    my_direction = pygame.math.Vector2(1, 0).rotate(self.angle)
                    rand_angle = random.randint(-180, 180)
                    ball_direction = my_direction.rotate(rand_angle)
                    ball_target = ball_direction * 100 + self.pos
                    self.kick(ball_interface, ball_target, c.MAX_BALL_SPEED)
            
        to_ball = ball_interface.pos - self.pos
        dist_to_ball_sq = to_ball.length_squared()

        # 自チーム内で最もボールに近い選手かどうかで役割を切り替える
        self.moving_state = MovingState.OFFENSE_CHASE
        for player in player_infos:
            if player.team_id == self.team_id:
                player_to_ball = ball_interface.pos - player.pos
                dist_player_to_ball_sq = player_to_ball.length_squared()
                if dist_player_to_ball_sq < dist_to_ball_sq:
                    self.moving_state = MovingState.DIFFENSE_RETURN
                    break


        # 状態に応じて移動先を決める
        match self.moving_state:
            case MovingState.OFFENSE_CHASE:  # ボールを追いかける
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

            case MovingState.DIFFENSE_RETURN:
                self.run(self.initial_pos)