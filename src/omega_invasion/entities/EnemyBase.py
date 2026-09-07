import math
import random
import pygame
from omega_invasion.entities.base import NaveBase



class DronEnemigo(NaveBase):
    """Enemigo estándar que desciende oscilando en zigzag."""

    def __init__(self, eje_x: float, eje_y: float, velocidad: float, *grupos):
        # 1 punto de vida, velocidad y 1000ms de cadencia en orden posicional
        super().__init__(eje_x, eje_y, 1, velocidad, 1000, *grupos)
        
        self.exp_otorgada = 25  # Experiencia que da al morir
        self.centro_x = eje_x
        self.amplitud_oscilacion = random.randint(30, 80)
        self.frecuencia = random.uniform(0.03, 0.06)
        self.tiempo_vivo = random.uniform(0, 100)

        # Gráfico del enemigo (nave alienígena roja/naranja)
        self.image = pygame.Surface((36, 36), pygame.SRCALPHA)
        # Se dibuja un triángulo invertido agresivo
        pygame.draw.polygon(self.image, (255, 60, 60), [(18, 36), (0, 0), (18, 10), (36, 0)])
        self.rect = self.image.get_rect(center=(round(eje_x), round(eje_y)))

    def update(self) -> None:
        self.tiempo_vivo += 1
        
        # Movimiento hacia abajo + oscilación matemática con seno (zigzag dinámico)
        self.pos.y += self.vel
        self.pos.x = self.centro_x + math.sin(self.tiempo_vivo * self.frecuencia) * self.amplitud_oscilacion
        
        self.rect.center = (round(self.pos.x), round(self.pos.y))

        # Si sale por el borde inferior de la pantalla, se destruye
        superficie = pygame.display.get_surface()
        if superficie and self.rect.top > superficie.get_height():
            self.kill()
