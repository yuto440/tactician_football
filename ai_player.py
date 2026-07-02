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
    def __init__(self, player_id: int, pos: pygame.math.Vector2, field_rect: pygame.rect):
        super().__init__(player_id, pos, field_rect)
        # まずは守備に戻る状態から始める
        self.moving_state:MovingState = MovingState.DIFFENSE_RETURN
        self.Kicking_state:KickingState = None
        

    def update_ai(self, match_analysis: MatchAnalysis) -> None:
        self._update_state(match_analysis)
        self._handle_kicking(match_analysis)
        self._handle_movement(match_analysis)


    def _update_state(self, match_analysis: MatchAnalysis):
        to_goal = self.goal_pos - self.pos
        dist_to_goal_sq = to_goal.length_squared()

        shot_range = 300
        shot_range_margin = 10

        if self.Kicking_state == None:
            if dist_to_goal_sq < shot_range ** 2:
                self.Kicking_state = KickingState.SHOT
            else:
                self.Kicking_state = None
        elif self.Kicking_state == KickingState.SHOT:
            if dist_to_goal_sq > shot_range ** 2 + shot_range_margin ** 2:
                self.Kicking_state = None

                # 自チーム内で最もボールに近い選手かどうかで役割を切り替える
        team_closest_rangikg = match_analysis.ball_proximity_list_by_team[self.team_id]
        closest_player, _ = team_closest_rangikg[0]
        if closest_player.player_id == self.player_id:
            self.moving_state = MovingState.OFFENSE_CHASE
        else:
            self.moving_state = MovingState.DIFFENSE_RETURN


    def _handle_kicking(self, match_analysis: MatchAnalysis):
        if self.can_kick(match_analysis.ball_interface):
            match self.Kicking_state:
                case KickingState.SHOT:
                    if not self.kick(match_analysis.ball_interface, self.goal_pos, c.MAX_BALL_SPEED):
                        self.Kicking_state = None
                case None:
                    my_direction = pygame.math.Vector2(1, 0).rotate(self.angle)
                    rand_angle = random.randint(-180, 180)
                    ball_direction = my_direction.rotate(rand_angle)
                    ball_target = ball_direction * 100 + match_analysis.ball_interface.pos
                    self.kick(match_analysis.ball_interface, ball_target, c.MAX_BALL_SPEED)

    def _handle_movement(self, match_analysis: MatchAnalysis):
                # 状態に応じて移動先を決める
        match self.moving_state:
            case MovingState.OFFENSE_CHASE:  # ボールを追いかける
                t = 0
                _, player_to_ball = match_analysis.player_to_ball_vectors[self.player_id]
                coeff_a = match_analysis.ball_interface.velocity.length_squared() - c.PLAYER_SPEED ** 2
                coeff_b = player_to_ball.dot(match_analysis.ball_interface.velocity)
                _, coeff_c = match_analysis.ball_proximity_list_by_id[self.player_id]

                discriminant = coeff_b ** 2 - coeff_a * coeff_c

                if abs(coeff_a) > 0.01 and discriminant >= 0:
                    t = (-coeff_b - discriminant ** 0.5) / coeff_a
                elif discriminant < 0:
                    t = 0
                else:
                    t = -coeff_c / (2 * coeff_b)

                t = min(max(0, t), 1)

                predicted_ball_pos = match_analysis.ball_interface.pos + match_analysis.ball_interface.velocity * t
                self.run(predicted_ball_pos)

            case MovingState.DIFFENSE_RETURN:
                self.run(self.initial_pos)