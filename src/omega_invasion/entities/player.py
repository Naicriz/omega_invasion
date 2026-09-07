from omega_invasion.entities.base import NaveBase
import pygame


class Jugador(NaveBase):
    def __init__(self, eje_x: float, eje_y: float, velocidad: float, *grupos: tuple):
        # Inicia con 3 puntos de vida, la velocidad indicada y cadencia de 350ms.
        super().__init__(eje_x, eje_y, hp=3, velocidad=velocidad, cadencia_ms=350, *grupos)
        # Cargar la imagen del jugador
        self.image = pygame.Surface((44, 44), pygame.SRCALPHA)
        # Dibujar la nave del jugador
        pygame.draw.polygon(self.image, (0, 220, 255), [(22, 0), (44, 40), (22, 30), (0, 40)])
        # Obtener el rectángulo de la nave
        self.rect = self.image.get_rect(center=(eje_x, eje_y))

        # --- Sistema de Niveles y Experiencia ---
        self.nivel = 1
        self.exp = 0
        self.exp_siguiente_nivel = 100


        # --- Niveles de Mejoras Permanentes ---
        self.nivel_canon = 1        # 1: Simple, 2: Doble, 3: Triple, 4: Abanico cuádruple
        self.nivel_cadencia = 1     # Reduce self.cadencia_ms
        self.nivel_dano = 1         # Aumenta el daño de cada proyectil
        self.nivel_velocidad = 1    # Aumenta self.vel
        self.escudo_max = 0         # Escudos que absorben daño antes de perder HP
        self.escudo_actual = 0

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

        self.pos += direccion * self.vel # Actualizar la posición
        self.rect.center = (round(self.pos.x), round(self.pos.y)) # Actualizar la posición del rectángulo
    
        # Límites para no salirse de la pantalla (1280 x 720)
        self.rect.clamp_ip(pygame.display.get_surface().get_rect()) # clamp_ip es para que no se salga de la pantalla
        self.pos = pygame.math.Vector2(self.rect.center) # Actualizar la posición del vector

    def ganar_exp(self, cantidad: int) -> bool:
        """Suma experiencia. Devuelve True si subió de nivel."""
        self.exp += cantidad
        if self.exp >= self.exp_siguiente_nivel:
            self.exp -= self.exp_siguiente_nivel
            self.nivel += 1
            # Cada nivel pide un 40% más de XP que el anterior
            self.exp_siguiente_nivel = int(self.exp_siguiente_nivel * 1.4)
            return True  # ¡Subió de nivel!
        return False

    def aplicar_mejora(self, tipo_mejora: str) -> None:
        """Aplica una mejora permanente acumulativa."""
        match tipo_mejora:
            case "canon":
                self.nivel_canon += 1  # Añade más balas por ráfaga
            case "cadencia":
                self.nivel_cadencia += 1
                # Reduce el cooldown en un 15% (con un límite de 70ms para no romper el juego)
                self.cadencia_ms = max(70, int(self.cadencia_ms * 0.85))
            case "dano":
                self.nivel_dano += 1
            case "velocidad":
                self.nivel_velocidad += 1
                self.vel += 0.8  # +0.8 píxeles por frame permanentemente
            case "vida_max":
                self.max_hp += 1
                self.hp += 1     # Sube vida máxima y cura 1 punto
            case "escudo":
                self.escudo_max += 1
                self.escudo_actual = self.escudo_max