# Jacob Meadows
# Computer Programming II, 6th Period
# 26 February, 2019
"""
pong.py

Be sure it meets previous requirements before moving onto these:
Changes:
1. Top half of PADDLE makes ball go up, bottom half makes it go down. (something different for middle of pad would be a
   good idea as well)
2. Your choice (must do two):
   a. Ball moves faster on every hit
   b. Paddle gets smaller on every successful hit
   c. Enemy paddle speed increases every hit
3. Have a way for the player to lose. Some options: certain amount of points by the PC, limited time, etc
4. Ball start should change (direction)
5. Only keep a score for the winner. Keep a high score of top 10 and show that after every loss. You don't need a menu
   or anything, but after the score shows you should have a prompt letting them know if they press space bar it will
   start the game over.

Copyright (C) 2018 Jacob Meadows

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
import pygame
import sys


class App:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Pong")
        pygame.display.set_icon(pygame.image.load("pong.png"))
        self.screen = pygame.display.set_mode((700, 400))
        self.clock = pygame.time.Clock()
        self.player = Player(rect=(20, 175, 20, 50))
        self.enemy = Enemy(rect=(660, 175, 20, 50))
        self.ball = Ball(rect=(340, 190, 20, 20))
        self.player_score = ScreenObject(rect=(100, 20, 100, 40))
        self.enemy_score = ScreenObject(rect=(self.screen.get_width() - 200, 20, 100, 40))
        self.player_score.image.blit(self.player.font.render(str(self.player.score), True, (255, 255, 255)), (0, 0))
        enemy_score = self.enemy.font.render(str(self.enemy.score), True, (255, 255, 255))
        self.enemy_score.image.blit(enemy_score, (self.enemy_score.image.get_width() - enemy_score.get_width(), 0))
        self.sprite_list = pygame.sprite.Group(self.player_score, self.enemy_score, self.player, self.enemy, self.ball)
        self.game_over = False
        self.game_animation = 0
        self.high_score_font = pygame.font.SysFont("Times New Roman", 30)
        self.high_score_surfs = [pygame.Surface((100, 100)) for _ in range(10)]

        while True:
            self.keys = pygame.key.get_pressed()
            self.sprite_rectangles = [tuple(sprite.rect.copy()) for sprite in self.sprite_list]

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    with open("high_scores.txt", "w") as high_scores:
                        high_scores.write("\n".join([str(score) for score in current_scores]))
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.game_over:
                            self.screen.fill((0, 0, 0))
                            self.player.rect.y = 175
                            self.enemy.rect.y = 175
                            self.player.score = 0
                            self.enemy.score = 0
                            self.player_score.image.fill((0, 0, 0))
                            self.player_score.image.blit(
                                self.player.font.render(str(self.player.score), True, (255, 255, 255)), (0, 0))
                            self.enemy_score.image.fill((0, 0, 0))
                            enemy_score = self.enemy.font.render(str(self.enemy.score), True, (255, 255, 255))
                            self.enemy_score.image.blit(
                                enemy_score, (self.enemy_score.image.get_width() - enemy_score.get_width(), 0)
                            )
                            [x.fill((0, 0, 0)) for x in self.high_score_surfs]
                            self.game_over = False
                            self.game_animation = 0
                            pygame.display.flip()

            if not self.game_over:
                self.sprite_list.update(self)
                for sprite_rectangle in range(len(self.sprite_rectangles)):
                    sprite_surf = pygame.Surface(
                        (self.sprite_rectangles[sprite_rectangle][2] * 3, self.sprite_rectangles[sprite_rectangle][3] * 3)
                    )
                    sprite_surf.fill((0, 0, 0))
                    self.screen.blit(sprite_surf, (
                        self.sprite_rectangles[sprite_rectangle][0] - self.sprite_rectangles[sprite_rectangle][2],
                        self.sprite_rectangles[sprite_rectangle][1] - self.sprite_rectangles[sprite_rectangle][3]
                    ))
                    self.sprite_rectangles[sprite_rectangle] = tuple((
                        self.sprite_rectangles[sprite_rectangle][0] - self.sprite_rectangles[sprite_rectangle][2],
                        self.sprite_rectangles[sprite_rectangle][1] - self.sprite_rectangles[sprite_rectangle][3],
                        *sprite_surf.get_size()
                    ))
                self.sprite_list.draw(self.screen)
                self.sprite_rectangles += [tuple(sprite.rect.copy()) for sprite in self.sprite_list]

                pygame.display.update(list(set(self.sprite_rectangles)))
            else:
                if self.game_animation < 100:
                    bg = pygame.Surface(self.screen.get_size())
                    bg.set_alpha(1)
                    bg.fill((100, 100, 100))
                    self.screen.blit(bg, (0, 0))
                    self.game_animation += 1
                elif self.game_animation == 100:
                    scores_text = self.high_score_font.render("High Scores", True, (255, 255, 255))
                    self.screen.blit(scores_text, ((self.screen.get_width() / 2) - (scores_text.get_width() / 2), 20))
                    self.game_animation += 1
                elif 100 < self.game_animation < 110:
                    if self.player.score >= int(current_scores[self.game_animation - 101]):
                        current_scores[self.game_animation - 101], self.player.score = \
                            self.player.score, int(current_scores[self.game_animation - 101])
                    self.high_score_surfs[self.game_animation - 101].blit(
                        self.high_score_font.render(
                            str(current_scores[self.game_animation - 101]), True, (255, 255, 255)
                        ), (0, 0)
                    )
                    self.screen.blit(self.high_score_surfs[self.game_animation - 101],
                                     ((self.screen.get_width() / 2) - (scores_text.get_width() / 2),
                                      40 + 30 * (self.game_animation - 100)))
                    self.game_animation += 1
                elif self.game_animation == 110:
                    restart_text = self.high_score_font.render(
                        "Press the space bar to play again", True, (255, 255, 255)
                    )
                    self.screen.blit(restart_text, ((self.screen.get_width() / 2) - (restart_text.get_width() / 2),
                                                    45 + 30 * (self.game_animation - 100)))
                    self.game_animation += 1
                pygame.display.flip()

            self.clock.tick(1500)


class ScreenObject(pygame.sprite.Sprite):
    def __init__(self, image=None, rect=None):
        super().__init__()
        if image:
            if isinstance(image, str):
                self.image = pygame.image.load(image).convert()
            else:
                self.image = image
            if rect:
                self.rect = pygame.Rect(*rect[:2], *self.image.get_size())
            else:
                self.rect = self.image.get_rect()
        else:
            if rect:
                self.rect = pygame.Rect(rect)
                self.image = pygame.Surface(self.rect[2:])
            else:
                self.rect = pygame.Rect(0, 0, 0, 0)
                self.image = None


class Player(ScreenObject):
    def __init__(self, const_y=5, **kwargs):
        super().__init__(**kwargs)
        self.image.fill((255, 255, 255))

        self.delta_y = int()
        self.const_y = const_y
        self.font = pygame.font.SysFont("Times New Roman", 40)
        self.score = 0

    def update(self, app):
        time_ms = app.clock.get_time()
        if time_ms == 0:
            time_ms = 1
        if app.keys[pygame.K_UP]:
            self.delta_y -= self.const_y * 40 * (time_ms / 1000.0)
        if app.keys[pygame.K_DOWN]:
            self.delta_y += self.const_y * 40 * (time_ms / 1000.0)

        self.rect.y += int(self.delta_y)
        if self.rect.y > app.screen.get_height() - self.rect.height:
            self.rect.y = app.screen.get_height() - self.rect.height
        elif self.rect.y < 0:
            self.rect.y = 0
        self.delta_y -= int(self.delta_y)


class Enemy(ScreenObject):
    def __init__(self, const_y=4, **kwargs):
        super().__init__(**kwargs)
        self.image.fill((255, 255, 255))

        self.delta_y = int()
        self.norm_const_y = const_y
        self.const_y = const_y
        self.font = pygame.font.SysFont("Times New Roman", 40)
        self.score = 0

    def update(self, app):
        time_ms = app.clock.get_time()
        if app.ball is not None:
            if self.rect.y > app.ball.rect.y:
                self.delta_y -= self.const_y * 40 * (time_ms / 1000.0)
            if self.rect.y < app.ball.rect.y:
                self.delta_y += self.const_y * 40 * (time_ms / 1000.0)

        self.rect.y += int(self.delta_y)
        if self.rect.y > app.screen.get_height() - self.rect.height:
            self.rect.y -= int(self.delta_y)
        self.delta_y -= int(self.delta_y)


class Ball(ScreenObject):
    def __init__(self, speed=4, **kwargs):
        super().__init__(**kwargs)
        self.image.fill((255, 255, 255))

        self.delta_y = int()
        self.delta_x = int()
        self.const_y = 40
        self.const_x = 40
        self.norm_speed = speed
        self.speed = speed

    def update(self, app):
        time_ms = app.clock.get_time()
        self.delta_y += self.speed * self.const_y * (time_ms / 1000.0)
        self.delta_x += self.speed * self.const_x * (time_ms / 1000.0)

        self.rect.y += int(self.delta_y)
        self.rect.x += int(self.delta_x)

        if self.rect.y < 0:
            self.rect.y = 0
            self.const_y *= -1
        if self.rect.y > app.screen.get_height() - self.rect.height:
            self.rect.y = app.screen.get_height() - self.rect.height
            self.const_y *= -1
        if self.rect.x < 0:
            self.rect.x = 340
            self.rect.y = 190
            self.const_x *= -1
            self.const_y *= -1
            self.speed = self.norm_speed
            app.enemy.score += 1
            app.enemy_score.image.fill((0, 0, 0))
            enemy_score = app.enemy.font.render(str(app.enemy.score), True, (255, 255, 255))
            app.enemy_score.image.blit(enemy_score, (app.enemy_score.image.get_width() - enemy_score.get_width(), 0))
            if app.enemy.score == 3:
                app.game_over = True
        if self.rect.x > app.screen.get_width() - self.rect.width:
            self.rect.x = 340
            self.rect.y = 190
            self.const_x *= -1
            self.const_y *= -1
            self.speed = self.norm_speed
            app.player.score += 1
            app.player_score.image.fill((0, 0, 0))
            app.player_score.image.blit(app.player.font.render(str(app.player.score), True, (255, 255, 255)), (0, 0))
        if self.rect.colliderect(pygame.Rect(*app.player.rect.topright, 0, app.player.rect.height / 2)) or \
                self.rect.colliderect(pygame.Rect(*app.enemy.rect.topleft, 0, app.player.rect.height / 2)):
            self.rect.x -= int(self.delta_x)
            self.const_x *= -1
            self.const_y = - abs(self.const_y)
            if self.speed < 7.5:
                self.speed += .3
            if app.enemy.const_y < 6.4:
                app.enemy.const_y += .1
        if self.rect.colliderect(pygame.Rect(app.player.rect.right, app.player.rect.top + (app.player.rect.height / 2),
                                             0, (app.player.rect.height / 2))) or \
                self.rect.colliderect(pygame.Rect(app.enemy.rect.left, app.enemy.rect.top + (app.enemy.rect.height / 2),
                                                  0, (app.enemy.rect.height / 2))):
            self.rect.x -= int(self.delta_x)
            self.const_x *= -1
            self.const_y = abs(self.const_y)
            if self.speed < 7.5:
                self.speed += .3
            if app.enemy.const_y < 6.4:
                app.enemy.const_y += .1
        if self.rect.colliderect(pygame.Rect(*app.player.rect.topleft, app.player.rect.width, 0)):
            self.rect.y -= int(self.delta_y) - app.player.rect.y + self.rect.y + self.rect.height
            self.const_y *= -1
        if self.rect.colliderect(pygame.Rect(*app.player.rect.bottomleft, app.player.rect.width, 0)):
            self.rect.y -= int(self.delta_y) - app.player.rect.y - app.player.rect.height + self.rect.y
            self.const_y *= -1
        if self.rect.colliderect(pygame.Rect(*app.enemy.rect.topleft, app.enemy.rect.width, 0)):
            self.rect.y -= int(self.delta_y) - app.enemy.rect.y + self.rect.y + self.rect.height
            self.const_y *= -1
        if self.rect.colliderect(pygame.Rect(*app.enemy.rect.bottomleft, app.enemy.rect.width, 0)):
            self.rect.y -= int(self.delta_y) - app.player.rect.y - app.player.rect.height + self.rect.y
            self.const_y *= -1

        self.delta_y -= int(self.delta_y)
        self.delta_x -= int(self.delta_x)


if __name__ == '__main__':
    try:
        with open("high_scores.txt", "r") as high_scores:
            current_scores = high_scores.read().split("\n")
    except FileNotFoundError:
        with open("high_scores.txt", "w") as high_scores:
            high_scores.write("0\n0\n0\n0\n0\n0\n0\n0\n0\n0")
        with open("high_scores.txt", "r") as high_scores:
            current_scores = high_scores.read().split("\n")
    App()
