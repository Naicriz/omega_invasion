# src/omega_invasion/entities/enemy.py
import math
import random
import pygame
from omega_invasion.entities.base import NaveBase
from omega_invasion.entities.bullet import Bala


class DronEnemigo(NaveBase):
    """Enemigo estándar ágil que desciende oscilando en zigzag y dispara de vez en cuando."""

    def __init__(self, eje_x: float, eje_y: float, velocidad: float, grupo_balas: pygame.sprite.Group, grupo_sprites: pygame.sprite.Group, *grupos):
        super().__init__(eje_x, eje_y, 1, velocidad, 1800, *grupos)
        self.grupo_balas = grupo_balas
        self.grupo_sprites = grupo_sprites
        self.exp_otorgada = 25

        self.centro_x = eje_x
        self.amplitud_oscilacion = random.randint(35, 75)
        self.frecuencia = random.uniform(0.03, 0.05)
        self.tiempo_vivo = random.uniform(0, 100)

        # Gráfico: Triángulo rojo ágil
        self.image = pygame.Surface((36, 36), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, (255, 60, 60), [(18, 36), (0, 0), (18, 10), (36, 0)])
        self.rect = self.image.get_rect(center=(round(eje_x), round(eje_y)))

    def update(self) -> None:
        self.tiempo_vivo += 1
        self.pos.y += self.vel
        self.pos.x = self.centro_x + math.sin(self.tiempo_vivo * self.frecuencia) * self.amplitud_oscilacion
        self.rect.center = (round(self.pos.x), round(self.pos.y))

        # Disparo hacia abajo
        if self.puede_disparar():
            Bala(self.rect.centerx, self.rect.bottom, 0.0, 6.0, 1, (255, 80, 80), self.grupo_balas, self.grupo_sprites)

        superficie = pygame.display.get_surface()
        if superficie and self.rect.top > superficie.get_height():
            self.kill()


class CazadorEnemigo(NaveBase):
    """Enemigo rastreador que persigue el eje horizontal del jugador y dispara ráfagas directas."""

    def __init__(self, eje_x: float, eje_y: float, velocidad: float, jugador, grupo_balas: pygame.sprite.Group, grupo_sprites: pygame.sprite.Group, *grupos):
        super().__init__(eje_x, eje_y, 2, velocidad, 1200, *grupos)
        self.jugador = jugador
        self.grupo_balas = grupo_balas
        self.grupo_sprites = grupo_sprites
        self.exp_otorgada = 45

        # Gráfico: Caza afilado de color violeta / fucsia
        self.image = pygame.Surface((38, 38), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, (220, 60, 255), [(19, 38), (0, 6), (19, 14), (38, 6)])
        self.rect = self.image.get_rect(center=(round(eje_x), round(eje_y)))

    def update(self) -> None:
        # Movimiento: desciende mientras persigue la coordenada X del jugador
        self.pos.y += self.vel
        if self.jugador and self.jugador.alive():
            if self.pos.x < self.jugador.rect.centerx - 10:
                self.pos.x += self.vel * 0.7
            elif self.pos.x > self.jugador.rect.centerx + 10:
                self.pos.x -= self.vel * 0.7

        self.rect.center = (round(self.pos.x), round(self.pos.y))

        # Dispara proyectiles rápidos si está por encima del jugador
        if self.puede_disparar() and self.rect.bottom < self.jugador.rect.top:
            Bala(self.rect.centerx, self.rect.bottom, 0.0, 8.0, 1, (255, 50, 220), self.grupo_balas, self.grupo_sprites)

        superficie = pygame.display.get_surface()
        if superficie and self.rect.top > superficie.get_height():
            self.kill()


class NodrizaEnemiga(NaveBase):
    """Nave pesada blindada (6 HP) que desciende lento y dispara un doble cañón pesado."""

    def __init__(self, eje_x: float, eje_y: float, velocidad: float, grupo_balas: pygame.sprite.Group, grupo_sprites: pygame.sprite.Group, *grupos):
        super().__init__(eje_x, eje_y, 6, velocidad * 0.5, 1400, *grupos)
        self.grupo_balas = grupo_balas
        self.grupo_sprites = grupo_sprites
        self.exp_otorgada = 120

        # Gráfico: Nave acorazada más ancha y dorada/naranja
        self.image = pygame.Surface((56, 42), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, (255, 165, 0), [(28, 42), (0, 12), (14, 0), (42, 0), (56, 12)])
        pygame.draw.polygon(self.image, (255, 220, 100), [(28, 30), (14, 10), (42, 10)])  # Núcleo brillante
        self.rect = self.image.get_rect(center=(round(eje_x), round(eje_y)))

    def update(self) -> None:
        self.pos.y += self.vel
        self.rect.center = (round(self.pos.x), round(self.pos.y))

        # Disparo doble simultáneo desde las alas
        if self.puede_disparar():
            Bala(self.rect.left + 10, self.rect.bottom, 0.0, 6.5, 1, (255, 140, 0), self.grupo_balas, self.grupo_sprites)
            Bala(self.rect.right - 10, self.rect.bottom, 0.0, 6.5, 1, (255, 140, 0), self.grupo_balas, self.grupo_sprites)

        superficie = pygame.display.get_surface()
        if superficie and self.rect.top > superficie.get_height():
            self.kill()
