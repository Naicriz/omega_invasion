import pygame


class Jugador(pygame.sprite.Sprite):
    def __init__(self, eje_x: float, eje_y: float, velocidad: float, *grupos: tuple):
        super().__init__(*grupos)
        # Cargar la imagen del jugador
        self.image = pygame.Surface((44, 44), pygame.SRCALPHA)
        # Dibujar la nave del jugador
        pygame.draw.polygon(self.image, (0, 220, 255), [(22, 0), (44, 40), (22, 30), (0, 40)])
        # Obtener el rectángulo de la nave
        self.rect = self.image.get_rect(center=(eje_x, eje_y))
        # Posición del jugador
        self.pos = pygame.math.Vector2(eje_x, eje_y)
        # Velocidad del jugador
        self.vel = velocidad
    
    def update(self):
        """Procesa las entradas y actualiza la posición del jugador."""

        teclas = pygame.key.get_pressed()
        direccion = pygame.math.Vector2()

        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            direccion.y -= 1
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            direccion.y += 1
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            direccion.x -= 1
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            direccion.x += 1
        
        # Normalizar la dirección para evitar que el jugador se mueva más rápido en diagonal
        if direccion.length() > 0:
            direccion = direccion.normalize()

        # Actualizar la posición
        self.pos += direccion * self.vel
        # Actualizar la posición del rectángulo
        self.rect.center = (round(self.pos.x), round(self.pos.y))
    
        # Límites para no salirse de la pantalla (1280 x 720)
        self.rect.clamp_ip(pygame.display.get_surface().get_rect()) # clamp_ip es para que no se salga de la pantalla
        self.pos = pygame.math.Vector2(self.rect.center) # Actualizar la posición del vector
