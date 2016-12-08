#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Módulos
# ---------------------------------------------------------------------
import sys, pygame
from pygame.locals import *

# Constantes
# ---------------------------------------------------------------------
WIDTH = 640
HEIGHT = 480
puntos_ganar = 1

# Funciones
# ---------------------------------------------------------------------
def load_image(filename, transparent=False):
    """Funcion que devuelve un objeto de tipo imagen."""
    try:
        image = pygame.image.load(filename)
    except pygame.error:
        raise SystemExit
    image = image.convert()
    if transparent:
        color = image.get_at((0, 0))
        image.set_colorkey(color, RLEACCEL)
    return image

def texto(texto, posx, posy, color=(255, 255, 255)):
    """Funcion que se encarga de consrtuir un texto."""
    fuente = pygame.font.Font("images/DroidSans.ttf", 25)
    salida = pygame.font.Font.render(fuente, texto, 1, color)
    salida_rect = salida.get_rect()
    salida_rect.centerx = posx
    salida_rect.centery = posy
    return salida, salida_rect

# Clases
# ---------------------------------------------------------------------
class Bola(pygame.sprite.Sprite):
    """Clase encargada de gestinar la bola."""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("images/ball.png", True)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 2
        self.speed = [0.5, -0.5]

    def actualizar(self, time, pala_jug, pala_cpu, puntos):
        """Movimiento de la Pelota."""
        self.rect.centerx += self.speed[0] * time
        self.rect.centery += self.speed[1] * time
        if self.rect.left <= 0:
            puntos[1] += 1
        if self.rect.right >= WIDTH:
            puntos[0] += 1
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed[1] = -self.speed[1]
            self.rect.centery += self.speed[1] * time
        if pygame.sprite.collide_rect(self, pala_jug):
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time
        if pygame.sprite.collide_rect(self, pala_cpu):
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time
        return puntos

class Pala(pygame.sprite.Sprite):
    """Clase encargada de gestinar la bola."""

    def __init__(self, pos_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("images/pala.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = pos_x
        self.rect.centery = HEIGHT / 2
        self.speed = 0.5

    def moverJugador(self, time, keys):
        """Movimiento del jugador."""
        if self.rect.top >= 0:
            if keys[K_UP]:
                self.rect.centery -= self.speed * time
        if self.rect.bottom <= HEIGHT:
            if keys[K_DOWN]:
                self.rect.centery += self.speed * time

    def moverIA(self, time, ball):
        """Movimiento de la IA."""
        if ball.speed[0] >= 0 and ball.rect.centerx >= WIDTH/2:
            if self.rect.centery < ball.rect.centery:
                self.rect.centery += self.speed * time
            if self.rect.centery > ball.rect.centery:
                self.rect.centery -= self.speed * time

class Flecha(pygame.sprite.Sprite):
    """Clase encargada de gestinar la Flecha."""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("images/flecha.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 4
        self.rect.centery = 200

    def moverFlecha(self, time, keys):
        """Movimiento del jugador."""
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

class Partida(pygame.sprite.Sprite):
    """Clase para controlar la partida."""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()
        self.puntos = [0, 0]
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.background_image = load_image("images/fondo_pong.png")
        self.bola = Bola()
        self.pala_jug = Pala(30)
        self.pala_cpu = Pala(WIDTH - 30)

    def comenzar(self):
        """Gestiona el mobimiento."""
        self.puntos = [0, 0] # Para cuando se vuelve a jugar
        while True:
            time = self.clock.tick(60)
            keys = pygame.key.get_pressed()
            for eventos in pygame.event.get():
                if eventos.type == QUIT:
                    sys.exit(0)

            self.puntos = self.bola.actualizar(time, self.pala_jug, self.pala_cpu, self.puntos)
            self.pala_jug.moverJugador(time, keys)
            self.pala_cpu.moverIA(time, self.bola)

            texo_jug = texto(str(self.puntos[0]), WIDTH/4, 40)
            texo_cpu = texto(str(self.puntos[1]), WIDTH-(WIDTH/4), 40)

            self.screen.blit(self.background_image, (0, 0))
            self.screen.blit(texo_jug[0], texo_jug[1])
            self.screen.blit(texo_cpu[0], texo_cpu[1])
            self.screen.blit(self.bola.image, self.bola.rect)
            self.screen.blit(self.pala_jug.image, self.pala_jug.rect)
            self.screen.blit(self.pala_cpu.image, self.pala_cpu.rect)
            pygame.display.flip()
            if self.puntos[0] >= puntos_ganar or self.puntos[1] >= puntos_ganar:
                break

    def ganar(self):
        """Gestiona las eleciones del jugador al terminar la partida."""
        image_ganar = load_image("images/fondo_ganar.png")
        flecha = Flecha()
        while True:
            time = self.clock.tick(60)
            keys = pygame.key.get_pressed()
            for eventos in pygame.event.get():
                if eventos.type == QUIT:
                    sys.exit(0)

            salida_flecha = flecha.moverFlecha(time, keys)
            t1 = texto("Jugar de nuevo", WIDTH/2, 200)
            t2 = texto("Salir", WIDTH/2, 300)
            if self.puntos[0] >= puntos_ganar:
                t3 = texto("El ganador es el jugador", WIDTH/2, 100)
            else:
                t3 = texto("El ganador es el ordenador", WIDTH/2, 100)
            self.screen.blit(image_ganar, (0, 0))
            self.screen.blit(t1[0], t1[1])
            self.screen.blit(t2[0], t2[1])
            self.screen.blit(t3[0], t3[1])
            self.screen.blit(flecha.image, flecha.rect)
            pygame.display.flip()
            if salida_flecha == 1:
                break;

# MAIN
# ---------------------------------------------------------------------

def main():
    pygame.display.set_caption("Pong-py")
    par1 = Partida()

    while True:
        par1.comenzar()
        par1.ganar()

    return 0

if __name__ == "__main__":
    pygame.init()
    main()
