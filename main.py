import pygame
import sys
import constants as c
from ball import *
from player import *
from team import Team
from ai_player import FSMPlayer
import random

class GameController:
    def __init__(self):
        # pygameの初期化と画面・フィールドの準備
        if not pygame.get_init():
            pygame.init()
        
        self.screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
        pygame.display.set_caption("Minimal Soccer")

        self.clock = pygame.time.Clock()

        self.field_rect = pygame.Rect(0, 0, c.FIELD_WIDTH, c.FIELD_HEIGHT)
        self.field_rect.center = self.screen.get_rect().center

        self.ball: Ball = Ball(pygame.math.Vector2(c.SCREEN_WIDTH // 2, c.SCREEN_HEIGHT // 2))  # ボールの生成
        self.ball_interface = BallInferface(self.ball)

        self.teams: list[Team] = [Team(c.TeamID.TEAM_A, pygame.math.Vector2(self.field_rect.midright) , c.RED),
                                Team(c.TeamID.TEAM_B, pygame.math.Vector2(self.field_rect.midleft) ,c.BLUE)]


        # フィールドを9×5のグリッドに分け、プレイヤーの初期位置を決める
        positions = []
        for row in range(9):
            row_positions = []
            for col in range(5):
                x = self.field_rect.left + c.FIELD_WIDTH / 10 * (row + 1)
                y = self.field_rect.top + c.FIELD_HEIGHT / 6 * (col + 1)

                row_positions.append(pygame.math.Vector2(x, y))
            positions.append(row_positions)

        # 各チームにプレイヤーを配置する
        self.players: list[Player] = [
            FSMPlayer(positions[1][0], self.field_rect),
            FSMPlayer(positions[1][4], self.field_rect),
            FSMPlayer(positions[3][2], self.field_rect),
            FSMPlayer(positions[7][0], self.field_rect),
            FSMPlayer(positions[7][4], self.field_rect),
            FSMPlayer(positions[5][2], self.field_rect)
        ]
        self.num_players: int = len(self.players)

        self.teams[0].add_player(self.players[0])
        self.teams[0].add_player(self.players[1])
        self.teams[0].add_player(self.players[2])
        self.teams[1].add_player(self.players[3])
        self.teams[1].add_player(self.players[4])
        self.teams[1].add_player(self.players[5])

        self.player_infos: list[PlayerInfo] = [PlayerInfo(player) for player in self.players]



        self.post_poses: list[pygame.math.Vector2] = [
            pygame.math.Vector2(self.field_rect.left, self.field_rect.centery - c.GOAL_WIDTH / 2),
            pygame.math.Vector2(self.field_rect.left, self.field_rect.centery + c.GOAL_WIDTH / 2),
            pygame.math.Vector2(self.field_rect.right, self.field_rect.centery - c.GOAL_WIDTH / 2),
            pygame.math.Vector2(self.field_rect.right, self.field_rect.centery + c.GOAL_WIDTH / 2),
        ]

        self.score_font = pygame.font.Font(None, 70)

        self.reset()

    def reset(self):
        # ゲーム状態を初期化してボールを中央へ戻す
        for player in self.players:
            player.reset()
        self.ball.pos = pygame.math.Vector2(self.field_rect.center)
        self.ball.velocity = pygame.math.Vector2(0, 0)
        return None

    def resolve_collisions(self):  # 壁・ポスト・プレイヤー間の衝突をまとめて処理
        self._check_wall_and_ball()
        self._check_posts_and_ball()
        self._check_player_and_player()
        return None

    def _check_wall_and_ball(self):
        #左右の壁との衝突。ゴールはすり抜ける
        if self.ball.pos.x - c.BALL_RADIUS < self.field_rect.left:
            if self.ball.pos.y < (c.SCREEN_HEIGHT - c.GOAL_WIDTH) / 2 or self.ball.pos.y > (c.SCREEN_HEIGHT + c.GOAL_WIDTH) / 2:
                self.ball.pos.x = self.field_rect.left + c.BALL_RADIUS
                self.ball.velocity.x = -self.ball.velocity.x
        elif self.ball.pos.x + c.BALL_RADIUS > self.field_rect.right:
            if self.ball.pos.y < (c.SCREEN_HEIGHT - c.GOAL_WIDTH) / 2 or self.ball.pos.y > (c.SCREEN_HEIGHT + c.GOAL_WIDTH) / 2:
                self.ball.pos.x = self.field_rect.right - c.BALL_RADIUS
                self.ball.velocity.x = -self.ball.velocity.x
        #上下の壁との衝突
        if self.ball.pos.y - c.BALL_RADIUS < self.field_rect.top:
            self.ball.pos.y = self.field_rect.top + c.BALL_RADIUS
            self.ball.velocity.y = -self.ball.velocity.y
        elif self.ball.pos.y + c.BALL_RADIUS > self.field_rect.bottom:
            self.ball.pos.y = self.field_rect.bottom - c.BALL_RADIUS
            self.ball.velocity.y = -self.ball.velocity.y

    def _check_posts_and_ball(self):
        for post_pos in self.post_poses:
            post_to_ball = self.ball.pos - post_pos
            dist_sq = post_to_ball.length_squared()
            radius = c.BALL_RADIUS

            if dist_sq < radius * radius:
                #print("post")

                if dist_sq > 0:
                    distance = dist_sq ** 0.5
                    n_post_to_ball = post_to_ball / distance
                else:
                    n_post_to_ball = pygame.math.Vector2(1, 0)
                    distance = 0

                overlap = radius - distance
                self.ball.pos += n_post_to_ball * overlap

                v_dot_n = self.ball.velocity.dot(n_post_to_ball)
                if v_dot_n < 0:
                    self.ball.velocity -= 2 * v_dot_n * n_post_to_ball

    def _check_player_and_player(self):
        for i in range(0, self.num_players - 1):
            for j in range(i + 1, self.num_players):#プレイヤー同士のすべての組み合わせを一度ずつ処理
                player_0 = self.players[i]
                player_1 = self.players[j]

                p0_to_p1 = player_1.pos - player_0.pos
                dist_sq = p0_to_p1.length_squared()

                min_distance = c.PLAYER_RADIUS * 2

                if dist_sq < min_distance * min_distance:
                    if dist_sq > 0:
                        distance = dist_sq ** 0.5
                        n_p0_to_p1 = p0_to_p1 / distance
                    else:
                        n_p0_to_p1 = pygame.math.Vector2(1, 0)
                        distance = 0

                    overlap = min_distance - distance

                    player_0.pos -= n_p0_to_p1 * overlap / 2
                    player_1.pos += n_p0_to_p1 * overlap / 2

    def goal_check(self):
        # ゴール判定を行い、得点したら試合をリセットする
        if self.ball.pos.x + c.BALL_RADIUS < self.teams[1].goal_pos.x:
            self.teams[1].score +=1
            self.reset()
        elif self.ball.pos.x - c.BALL_RADIUS> self.teams[0].goal_pos.x:
            self.teams[0].score +=1
            self.reset()
        return None
                

    def display(self):
        # 画面を描画し直して現在の状態を表示する
        self.screen.fill(c.GRASS_COLOR)

        pygame.draw.line(self.screen, c.WHITE, (self.field_rect.centerx, self.field_rect.top), (self.field_rect.centerx, self.field_rect.bottom), c.LINE_WIDTH)
        pygame.draw.circle(self.screen, c.WHITE, self.field_rect.center, c.FIELD_HEIGHT // 4, c.LINE_WIDTH)
        pygame.draw.circle(self.screen, c.WHITE, self.field_rect.center, c.LINE_WIDTH * 2)

        # pygame.draw.line(self.screen, c.WHITE, self.field_rect.topright, self.field_rect.topleft, 3)
        # pygame.draw.line(self.screen, c.WHITE, self.field_rect.bottomright, self.field_rect.bottomleft, 3)
        # pygame.draw.line(self.screen, c.WHITE, self.field_rect.topleft, self.post_poses[0], 3)
        # pygame.draw.line(self.screen, c.WHITE, self.field_rect.bottomleft, self.post_poses[1], 3)
        # pygame.draw.line(self.screen, c.WHITE, self.field_rect.topright, self.post_poses[2], 3)
        # pygame.draw.line(self.screen, c.WHITE, self.field_rect.bottomright, self.post_poses[3], 3)

        pygame.draw.rect(self.screen, c.WHITE, self.field_rect, c.LINE_WIDTH)
        
        for post_pos in self.post_poses:
            pygame.draw.circle(self.screen, c.WHITE, (int(post_pos.x), int(post_pos.y)), c.LINE_WIDTH * 3)

        score_text = f"{self.teams[0].score} - {self.teams[1].score}"
        score_surface = self.score_font.render(score_text, True, c.WHITE)
        score_rect = score_surface.get_rect()
        score_rect.centerx = self.field_rect.centerx
        self.screen.blit(score_surface, score_rect)

        for player in self.players:
            player.draw(self.screen)
        self.ball.draw(self.screen)

        
        pygame.display.flip()
        return None

    def play_game(self):
        # メインループ。入力処理・物理演算・描画を順に行う
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.resolve_collisions()
            self.goal_check()
            dt = self.clock.tick(c.FPS) / 1000.0
            self.ball.update(dt)
            
            for player in self.players:
                player.update_ai(self.ball_interface, self.player_infos)

            for player in self.players:
                player.update(dt)

            self.display()

        pygame.quit()
        sys.exit()

        return None

if __name__ == "__main__":
    gm = GameController()
    gm.play_game()