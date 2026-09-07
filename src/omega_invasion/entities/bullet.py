import pygame


class Bala(pygame.sprite.Sprite):
    def __init__(self, eje_x: float, eje_y: float, vel_x: float, vel_y: float, dano: float = 1, color: tuple = (0,255,255), *grupos):
        super().__init__(*grupos)
        self.image = pygame.Surface((6, 14), pygame.SRCALPHA)
        #self.image.fill(color)
        #self.rect = self.image.get_rect(center=(round(eje_x),round(eje_y)))
        self.pos = pygame.math.Vector2(eje_x, eje_y)
        self.vel = pygame.math.Vector2(vel_x, vel_y)
        self.dano = dano

        pygame.draw.polygon(self.image, color, [(6//2,0), (6,14), (0,14)])
        self.rect = self.image.get_rect(center=(round(eje_x),round(eje_y)))

    def update(self) -> None:
        self.pos += self.vel
        self.rect.center = (round(self.pos.x),round(self.pos.y))

        # Si sale de la pantalla, se destruye automáticamente para liberar memoria
        superficie = pygame.display.get_surface()
        if not superficie.get_rect().colliderect(self.rect):
            self.kill()
