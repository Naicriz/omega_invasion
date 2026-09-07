import pygame
import math

class Bala(pygame.sprite.Sprite):
    def __init__(self, eje_x: float, eje_y: float, vel_x: float, vel_y: float, dano: float = 1, color: tuple = (0, 255, 255), sprite: pygame.Surface | None = None, *grupos):
        # Si se pasó un Group en la posición de sprite por omisión, lo reubicamos a grupos
        if isinstance(sprite, pygame.sprite.Group):
            grupos = (sprite,) + grupos
            sprite = None
        super().__init__(*grupos)
        
        if sprite is not None:
            # Rotar el sprite hacia la dirección de vuelo
            if vel_x != 0 or vel_y != 0:
                angulo = math.degrees(math.atan2(-vel_y, vel_x)) - 90
                self.image = pygame.transform.rotate(sprite, angulo)
            else:
                self.image = sprite.copy()
        else:
            self.image = pygame.Surface((6, 14), pygame.SRCALPHA)
            self.image.fill(color)

        self.rect = self.image.get_rect(center=(round(eje_x), round(eje_y)))
        self.pos = pygame.math.Vector2(eje_x, eje_y)
        self.vel = pygame.math.Vector2(vel_x, vel_y)
        self.dano = dano

    def update(self) -> None:
        self.pos += self.vel
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        superficie = pygame.display.get_surface()
        if superficie and not superficie.get_rect().colliderect(self.rect):
            self.kill()