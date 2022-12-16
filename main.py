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
import pygame
from pygame.locals import *

# Constantes
# ---------------------------------------------------------------------
formWidth = 640
formHeight = 480
ballSpeed = 0.1
playerSpeed = 0.5
computerSpeed = 0.4
pointsToWin = 3
lang1 = ['Play', 'Exit', 'The winner is the Player', 'The winner is the Computer', 'Welcome to Pong-py']

# Funciones
# ---------------------------------------------------------------------
def load_image(filename, transparent=False):
    """Function to reurn a image object."""
    try:
        image = pygame.image.load(filename)
    except pygame.error:
        raise SystemExit
    image = image.convert()
    if transparent:
        color = image.get_at((0, 0))
        image.set_colorkey(color, RLEACCEL)
    return image

def fText(text1, posx, posy, color=(255, 255, 255)):
    """Manage text box in pygame."""
    fuente = pygame.font.Font("images/DroidSans.ttf", 25)
    salida = pygame.font.Font.render(fuente, text1, 1, color)
    salida_rect = salida.get_rect()
    salida_rect.centerx = posx
    salida_rect.centery = posy
    return salida, salida_rect

# Clases
# ---------------------------------------------------------------------
class Ball(pygame.sprite.Sprite):
    """Class to control the Ball."""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("images/ball.png", True)
        self.rect = self.image.get_rect()
        self.rect.centerx = formWidth / 2
        self.rect.centery = formHeight / 2
        self.speed = [ballSpeed, (ballSpeed * -1)]

    def updateBallStatus(self, time, Shovel_jug, Shovel_cpu, puntos):
        """Manage ball's movement."""
        self.rect.centerx += self.speed[0] * time
        self.rect.centery += self.speed[1] * time
        if self.rect.left <= 0:
            puntos[1] += 1
        if self.rect.right >= formWidth:
            puntos[0] += 1
        if self.rect.left <= 0 or self.rect.right >= formWidth:
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time
        if self.rect.top <= 0 or self.rect.bottom >= formHeight:
            self.speed[1] = -self.speed[1]
            self.rect.centery += self.speed[1] * time
        if pygame.sprite.collide_rect(self, Shovel_jug):
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time
        if pygame.sprite.collide_rect(self, Shovel_cpu):
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time
        return puntos

class Shovel(pygame.sprite.Sprite):
    """Class to control the shovel."""

    def __init__(self, pos_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("images/shovel.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = pos_x
        self.rect.centery = formHeight / 2

    def payerMove(self, time, keys):
        """Manage player's movement."""
        if self.rect.top >= 0:
            if keys[K_UP]:
                self.rect.centery -= playerSpeed * time
        if self.rect.bottom <= formHeight:
            if keys[K_DOWN]:
                self.rect.centery += playerSpeed * time

    def aiMove(self, time, ball):
        """Manage AI's movement."""
        if ball.speed[0] >= 0 and ball.rect.centerx >= formWidth/2:
            if self.rect.centery < ball.rect.centery:
                self.rect.centery += computerSpeed * time
            if self.rect.centery > ball.rect.centery:
                self.rect.centery -= computerSpeed * time

class Arrow(pygame.sprite.Sprite):
    """Class to control the arrow."""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("images/arrow.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = formWidth / 3
        self.rect.centery = 200

    def arrowMove(self, time, keys):
        """Manage Player."""
        salida = 0
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
                salida = 1
        return salida

class Game(pygame.sprite.Sprite):
    """Class to control the game."""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()
        self.puntos = [0, 0]
        self.screen = pygame.display.set_mode((formWidth, formHeight))
        self.background_image = load_image("images/backgroundGame.png")
        self.Ball = Ball()
        self.Shovel_jug = Shovel(30)
        self.Shovel_cpu = Shovel(formWidth - 30)

    def start(self):
        """Manage a game."""
        self.puntos = [0, 0] # Para cuando se vuelve a jugar
        while True:
            time = self.clock.tick(60)
            keys = pygame.key.get_pressed()
            for eventos in pygame.event.get():
                if eventos.type == QUIT:
                    sys.exit(0)

            self.puntos = self.Ball.updateBallStatus(time, self.Shovel_jug, self.Shovel_cpu, self.puntos)
            self.Shovel_jug.payerMove(time, keys)
            self.Shovel_cpu.aiMove(time, self.Ball)

            texo_jug = fText(str(self.puntos[0]), formWidth/4, 40)
            texo_cpu = fText(str(self.puntos[1]), formWidth-(formWidth/4), 40)

            self.screen.blit(self.background_image, (0, 0))
            self.screen.blit(texo_jug[0], texo_jug[1])
            self.screen.blit(texo_cpu[0], texo_cpu[1])
            self.screen.blit(self.Ball.image, self.Ball.rect)
            self.screen.blit(self.Shovel_jug.image, self.Shovel_jug.rect)
            self.screen.blit(self.Shovel_cpu.image, self.Shovel_cpu.rect)
            pygame.display.flip()
            if self.puntos[0] >= pointsToWin or self.puntos[1] >= pointsToWin:
                break

    def menu(self):
        """Manage main menu."""
        image_ganar = load_image("images/menu.png")
        arrow1 = Arrow()
        while True:
            time = self.clock.tick(60)
            keys = pygame.key.get_pressed()
            for eventos in pygame.event.get():
                if eventos.type == QUIT:
                    sys.exit(0)

            arrowReturn = arrow1.arrowMove(time, keys)
            t1 = fText(lang1[0], formWidth/2, 200)
            t2 = fText(lang1[1], formWidth/2, 300)
            if self.puntos[0] >= pointsToWin:
                t3 = fText(lang1[2], formWidth/2, 100)
            elif self.puntos[1] >= pointsToWin:
                t3 = fText(lang1[3], formWidth/2, 100)
            else:
                t3 = fText(lang1[4], formWidth/2, 100)
            self.screen.blit(image_ganar, (0, 0))
            self.screen.blit(t1[0], t1[1])
            self.screen.blit(t2[0], t2[1])
            self.screen.blit(t3[0], t3[1])
            self.screen.blit(arrow1.image, arrow1.rect)
            pygame.display.flip()
            if arrowReturn == 1:
                break;


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Pong-py")
    g1 = Game()

    while True:
        g1.menu()
        g1.start()
