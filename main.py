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

# Módulos
# ---------------------------------------------------------------------
import sys
import json
import pygame
from pygame.locals import *

# Constantes
# ---------------------------------------------------------------------
CONFIG = json.load(open('config.json'))
formWidth = CONFIG["formWidth"]
formHeight = CONFIG["formHeight"]
ballSpeed = CONFIG["ballSpeed"]
playerSpeed = CONFIG["playerSpeed"]
computerSpeed = CONFIG["computerSpeed"]
pointsToWin = CONFIG["pointsToWin"]
lang1 = list()
lang1.append(str(CONFIG["lang"]["text_play"]))
lang1.append(str(CONFIG["lang"]["text_exit"]))
lang1.append(str(CONFIG["lang"]["text_win"]))
lang1.append(str(CONFIG["lang"]["text_lose"]))
lang1.append(str(CONFIG["lang"]["text_welcome"]))


# Funciones
# ---------------------------------------------------------------------
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


def get_text(text1, posx, posy, color=(255, 255, 255)):
    """Manage text box in pygame."""
    my_font = pygame.font.Font("font/DroidSans.ttf", 25)
    output_text = my_font.render(text1, True, color)
    text_pos = output_text.get_rect()
    text_pos.centerx = posx
    text_pos.centery = posy
    return output_text, text_pos


# Clases
# ---------------------------------------------------------------------
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

    def arrow_move(self, time, keys):
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
        self.Ball = Ball()
        self.player_shovel = Shovel(30)
        self.ai_shovel = Shovel(formWidth - 30)

    def start(self):
        """Manage a game."""
        self.points = [0, 0]
        while True:
            time = self.clock.tick(60)
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)

            self.points = self.Ball.update_ball_status(time, self.player_shovel, self.ai_shovel, self.points)
            self.player_shovel.payer_move(time, keys)
            self.ai_shovel.ai_move(time, self.Ball)

            texo_jug = get_text(str(self.points[0]), formWidth / 4, 40)
            texo_cpu = get_text(str(self.points[1]), formWidth - (formWidth / 4), 40)

            self.screen.blit(self.background_image, (0, 0))
            self.screen.blit(texo_jug[0], texo_jug[1])
            self.screen.blit(texo_cpu[0], texo_cpu[1])
            self.screen.blit(self.Ball.image, self.Ball.rect)
            self.screen.blit(self.player_shovel.image, self.player_shovel.rect)
            self.screen.blit(self.ai_shovel.image, self.ai_shovel.rect)
            pygame.display.flip()
            if self.points[0] >= pointsToWin or self.points[1] >= pointsToWin:
                break

    def menu(self):
        """Manage main menu."""
        win_image = get_image("img/menu.png")
        arrow1 = Arrow()
        while True:
            time = self.clock.tick(60)
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)

            arrow_movement = arrow1.arrow_move(time, keys)
            t1 = get_text(lang1[0], formWidth / 2, 200)
            t2 = get_text(lang1[1], formWidth / 2, 300)
            if self.points[0] >= pointsToWin:
                t3 = get_text(lang1[2], formWidth / 2, 100)
            elif self.points[1] >= pointsToWin:
                t3 = get_text(lang1[3], formWidth / 2, 100)
            else:
                t3 = get_text(lang1[4], formWidth / 2, 100)
            self.screen.blit(win_image, (0, 0))
            self.screen.blit(t1[0], t1[1])
            self.screen.blit(t2[0], t2[1])
            self.screen.blit(t3[0], t3[1])
            self.screen.blit(arrow1.image, arrow1.rect)
            pygame.display.flip()
            if arrow_movement == 1:
                break


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Pong-py")
    g1 = Game()

    while True:
        g1.menu()
        g1.start()
