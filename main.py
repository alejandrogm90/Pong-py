#!/usr/bin/env python3
#
#       Copyright 2016 Alejandro Gomez
#
#       This program is free software: you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation, either version 3 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import json
import pygame
from pygame.locals import *

CONFIG = json.load(open('config.json'))
formWidth = CONFIG["formWidth"]
formHeight = CONFIG["formHeight"]
ballSpeed = CONFIG["ballSpeed"]
playerSpeed = CONFIG["playerSpeed"]
computerSpeed = CONFIG["computerSpeed"]
pointsToWin = CONFIG["pointsToWin"]


def get_image(filename, transparent=False):
    """Function to returns the image object."""
    try:
        image = pygame.image.load(filename).convert()
    except pygame.error:
        raise SystemExit
    if transparent:
        color = image.get_at((0, 0))
        image.set_colorkey(color, RLEACCEL)
    return image


def get_text(text1, pos_x, pos_y, color=(255, 255, 255)):
    """Manage text box in pygame."""
    my_font = pygame.font.Font("font/DroidSans.ttf", 25)
    output_text = my_font.render(text1, True, color)
    text_pos = output_text.get_rect()
    text_pos.centerx = pos_x
    text_pos.centery = pos_y
    return output_text, text_pos


class Ball(pygame.sprite.Sprite):
    """Class to control the Ball."""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = get_image("img/ball.png", True)
        self.rect = self.image.get_rect()
        self.rect.centerx = formWidth / 2
        self.rect.centery = formHeight / 2
        self.speed = [ballSpeed, (ballSpeed * -1)]

    def update_ball_status(self, time, player_shovel, ai_shovel, points):
        """Manage ball's movement."""
        self.rect.centerx += self.speed[0] * time
        self.rect.centery += self.speed[1] * time
        if self.rect.left <= 0:
            points[1] += 1
        if self.rect.right >= formWidth:
            points[0] += 1
        if self.rect.left <= 0 or self.rect.right >= formWidth:
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time
        if self.rect.top <= 0 or self.rect.bottom >= formHeight:
            self.speed[1] = -self.speed[1]
            self.rect.centery += self.speed[1] * time
        if pygame.sprite.collide_rect(self, player_shovel):
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time
        if pygame.sprite.collide_rect(self, ai_shovel):
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time
        return points


class Shovel(pygame.sprite.Sprite):
    """Class to control the shovel."""

    def __init__(self, pos_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = get_image("img/shovel.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = pos_x
        self.rect.centery = formHeight / 2

    def payer_move(self, time, keys):
        """Manage player's movement."""
        if self.rect.top >= 0:
            if keys[K_UP]:
                self.rect.centery -= playerSpeed * time
        if self.rect.bottom <= formHeight:
            if keys[K_DOWN]:
                self.rect.centery += playerSpeed * time

    def ai_move(self, time, ball):
        """Manage AI's movement."""
        if ball.speed[0] >= 0 and ball.rect.centerx >= formWidth / 2:
            if self.rect.centery < ball.rect.centery:
                self.rect.centery += computerSpeed * time
            if self.rect.centery > ball.rect.centery:
                self.rect.centery -= computerSpeed * time


class Arrow(pygame.sprite.Sprite):
    """Class to control the arrow."""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = get_image("img/arrow.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = formWidth / 3
        self.rect.centery = 200

    def arrow_move(self, keys):
        """Manage Player."""
        arrow_movement = 0
        if self.rect.centery != 200:
            if keys[K_UP]:
                self.rect.centery = 200
        if self.rect.centery != 300:
            if keys[K_DOWN]:
                self.rect.centery = 300
        if self.rect.centery == 300:
            if keys[K_RETURN]:
                raise SystemExit
        if self.rect.centery == 200:
            if keys[K_RETURN]:
                arrow_movement = 1
        return arrow_movement


class Game(pygame.sprite.Sprite):
    """Class to control the game."""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()
        self.points = [0, 0]
        self.screen = pygame.display.set_mode((formWidth, formHeight))
        self.background_image = get_image("img/backgroundGame.png")
        self.game_ball = Ball()
        self.player_shovel = Shovel(30)
        self.ai_shovel = Shovel(formWidth - 30)
        self.HALF_FROM_WIDTH = formWidth / 2
        self.PLAYER_TEXT_POSITION = formWidth / 4
        self.AI_TEXT_POSITION = formWidth - self.PLAYER_TEXT_POSITION

    def start(self):
        """Manage a game."""
        self.points = [0, 0]
        while True:
            time = self.clock.tick(60)
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)

            self.points = self.game_ball.update_ball_status(time, self.player_shovel, self.ai_shovel, self.points)
            self.player_shovel.payer_move(time, keys)
            self.ai_shovel.ai_move(time, self.game_ball)

            texo_jug = get_text(str(self.points[0]), self.PLAYER_TEXT_POSITION, 40)
            texo_cpu = get_text(str(self.points[1]), self.AI_TEXT_POSITION, 40)

            self.screen.blit(self.background_image, (0, 0))
            self.screen.blit(texo_jug[0], texo_jug[1])
            self.screen.blit(texo_cpu[0], texo_cpu[1])
            self.screen.blit(self.game_ball.image, self.game_ball.rect)
            self.screen.blit(self.player_shovel.image, self.player_shovel.rect)
            self.screen.blit(self.ai_shovel.image, self.ai_shovel.rect)

            pygame.display.flip()
            if self.points[0] >= pointsToWin or self.points[1] >= pointsToWin:
                break

    def menu(self):
        """Manage main menu."""
        win_image = get_image("img/menu.png")
        arrow1 = Arrow()
        t1 = get_text(CONFIG["lang"]["text_play"], self.HALF_FROM_WIDTH, 200)
        t2 = get_text(CONFIG["lang"]["text_exit"], self.HALF_FROM_WIDTH, 300)
        if self.points[0] >= pointsToWin:
            t3 = get_text(CONFIG["lang"]["text_win"], self.HALF_FROM_WIDTH, 100)
        elif self.points[1] >= pointsToWin:
            t3 = get_text(CONFIG["lang"]["text_lose"], self.HALF_FROM_WIDTH, 100)
        else:
            t3 = get_text(CONFIG["lang"]["text_welcome"], self.HALF_FROM_WIDTH, 100)
        t4 = get_text("Player {0} - AI {1}".format(self.points[0], self.points[1]), self.HALF_FROM_WIDTH, 150)

        while True:
            self.clock.tick(60)
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)

            self.screen.blit(win_image, (0, 0))
            self.screen.blit(t1[0], t1[1])
            self.screen.blit(t2[0], t2[1])
            self.screen.blit(t3[0], t3[1])
            if self.points[0] == pointsToWin or self.points[1] == pointsToWin:
                self.screen.blit(t4[0], t4[1])
            self.screen.blit(arrow1.image, arrow1.rect)

            pygame.display.flip()
            arrow_movement = arrow1.arrow_move(keys)
            if arrow_movement == 1:
                break


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Pong-py")
    g1 = Game()

    while True:
        g1.menu()
        g1.start()
