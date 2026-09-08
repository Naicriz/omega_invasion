# src/omega_invasion/entities/enemy.py
import math
import random
import pygame
from omega_invasion.entities.base import NaveBase
from omega_invasion.entities.bullet import Bala, BolaEnergia
from omega_invasion.entities.effects import ParticulaEstela
from omega_invasion.utils.assets import obtener_sprite, reproducir_sonido



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
        self.contador_estela = random.randint(0, 3)

        # Gráfico: Sprite pixel art de caza ágil
        self.image_base = obtener_sprite("dron")
        self.image = self.image_base.copy()
        self.rect = self.image.get_rect(center=(round(eje_x), round(eje_y)))

    def update(self) -> None:
        self.tiempo_vivo += 1
        self.pos.y += self.vel
        self.pos.x = self.centro_x + math.sin(self.tiempo_vivo * self.frecuencia) * self.amplitud_oscilacion

        # Inclinación visual según la dirección del vuelo en zigzag
        vx = math.cos(self.tiempo_vivo * self.frecuencia) * self.amplitud_oscilacion * self.frecuencia
        angulo_tilt = max(-14.0, min(14.0, -vx * 4.5))

        centro_prev = (round(self.pos.x), round(self.pos.y))
        if abs(angulo_tilt) > 1.0:
            self.image = pygame.transform.rotate(self.image_base, angulo_tilt)
        else:
            self.image = self.image_base
        self.rect = self.image.get_rect(center=centro_prev)

        # Estela de propulsión de chispas
        self.contador_estela += 1
        if self.contador_estela % 3 == 0:
            ParticulaEstela(
                self.rect.centerx + random.uniform(-2, 2),
                self.rect.top - 2,
                pygame.Color("orangered"),
                random.uniform(-0.3, 0.3),
                -random.uniform(1.5, 3.0),
                10,
                3,
                self.grupo_sprites
            )

        # Disparo hacia abajo
        if self.puede_disparar():
            reproducir_sonido("laser_enemigo", volumen=0.1)
            sprite_bala = obtener_sprite("bala_roja")
            Bala(self.rect.centerx, self.rect.bottom, 0.0, 6.0, 1, pygame.Color("tomato"), sprite_bala, self.grupo_balas, self.grupo_sprites)

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
        self.exp_otorgada = 35
        self.angulo_inclinacion = 0.0
        self.contador_estela = random.randint(0, 3)

        # Gráfico: Sprite pixel art de interceptor violeta
        self.image_base = obtener_sprite("cazador")
        self.image = self.image_base.copy()
        self.rect = self.image.get_rect(center=(round(eje_x), round(eje_y)))

    def update(self) -> None:
        # Movimiento: desciende mientras persigue la coordenada X del jugador
        self.pos.y += self.vel
        target_tilt = 0.0

        if self.jugador and self.jugador.alive():
            if self.pos.x < self.jugador.rect.centerx - 8:
                self.pos.x += self.vel * 0.6
                target_tilt = -12.0  # Inclinación al perseguir hacia la derecha
            elif self.pos.x > self.jugador.rect.centerx + 8:
                self.pos.x -= self.vel * 0.6
                target_tilt = 12.0   # Inclinación al perseguir hacia la izquierda

        self.angulo_inclinacion += (target_tilt - self.angulo_inclinacion) * 0.25
        centro_prev = (round(self.pos.x), round(self.pos.y))

        if abs(self.angulo_inclinacion) > 1.0:
            self.image = pygame.transform.rotate(self.image_base, self.angulo_inclinacion)
        else:
            self.image = self.image_base
        self.rect = self.image.get_rect(center=centro_prev)

        # Estela de plasma violeta/magenta
        self.contador_estela += 1
        if self.contador_estela % 3 == 0:
            ParticulaEstela(
                self.rect.centerx + random.uniform(-2, 2),
                self.rect.top - 2,
                pygame.Color("magenta"),
                random.uniform(-0.3, 0.3),
                -random.uniform(1.8, 3.2),
                10,
                3,
                self.grupo_sprites
            )

        # Dispara proyectiles rápidos si está por encima del jugador
        if self.puede_disparar() and self.rect.bottom < self.jugador.rect.top:
            reproducir_sonido("laser_enemigo", volumen=0.1)
            sprite_bala = obtener_sprite("bala_roja")
            Bala(self.rect.centerx, self.rect.bottom, 0.0, 8.0, 1, pygame.Color("magenta"), sprite_bala, self.grupo_balas, self.grupo_sprites)

        superficie = pygame.display.get_surface()
        if superficie and self.rect.top > superficie.get_height():
            self.kill()


class NodrizaEnemiga(NaveBase):
    """Nave pesada blindada (6 HP) que desciende lento y dispara un doble cañón pesado."""

    def __init__(self, eje_x: float, eje_y: float, velocidad: float, grupo_balas: pygame.sprite.Group, grupo_sprites: pygame.sprite.Group, *grupos):
        super().__init__(eje_x, eje_y, 6, velocidad * 0.5, 1400, *grupos)
        self.grupo_balas = grupo_balas
        self.grupo_sprites = grupo_sprites
        self.exp_otorgada = 75
        self.contador_estela = 0

        # Gráfico: Sprite pixel art de crucero acorazado
        self.image = obtener_sprite("nodriza").copy()
        self.rect = self.image.get_rect(center=(round(eje_x), round(eje_y)))

    def update(self) -> None:
        self.pos.y += self.vel
        self.rect.center = (round(self.pos.x), round(self.pos.y))

        # Estela doble de motores de plasma pesados
        self.contador_estela += 1
        if self.contador_estela % 2 == 0:
            ParticulaEstela(
                self.rect.left + 6,
                self.rect.top - 2,
                pygame.Color("orange"),
                random.uniform(-0.2, 0.2),
                -random.uniform(1.2, 2.2),
                12,
                3,
                self.grupo_sprites
            )
            ParticulaEstela(
                self.rect.right - 6,
                self.rect.top - 2,
                pygame.Color("orange"),
                random.uniform(-0.2, 0.2),
                -random.uniform(1.2, 2.2),
                12,
                3,
                self.grupo_sprites
            )

        # Patrón de disparo en abanico (salva triple de bolas de energía)
        if self.puede_disparar():
            reproducir_sonido("laser_enemigo", volumen=0.15)
            # 1. Cañón izquierdo en ángulo diagonal
            BolaEnergia(self.rect.left + 6, self.rect.bottom - 4, -2.2, 5.0, 1, self.grupo_balas, self.grupo_sprites)
            # 2. Reactor central frontal hacia abajo
            BolaEnergia(self.rect.centerx, self.rect.bottom, 0.0, 5.8, 1, self.grupo_balas, self.grupo_sprites)
            # 3. Cañón derecho en ángulo diagonal
            BolaEnergia(self.rect.right - 6, self.rect.bottom - 4, 2.2, 5.0, 1, self.grupo_balas, self.grupo_sprites)

        superficie = pygame.display.get_surface()
        if superficie and self.rect.top > superficie.get_height():
            self.kill()
