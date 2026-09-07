import pygame


class NaveBase(pygame.sprite.Sprite):
    """Clase base para cualquier nave (Jugador O Enemigos.)"""

    def __init__(self, eje_x: float, eje_y: float, hp: float, velocidad: float, cadencia_ms: float, *grupos: tuple):
        super().__init__(*grupos)
        self.hp = hp                                    # Vida actual
        self.max_hp = hp                                # Vida maxima
        self.pos = pygame.math.Vector2(eje_x, eje_y)    # Posición del jugador
        self.vel = velocidad                            # Velocidad del jugador
        self.cadencia_ms = cadencia_ms                  # Tiempo minimo en milisegundos entre disparos.
        self.ultimo_disparo = -cadencia_ms              # Permite disparar de inmediato al iniciar.
        
    def recibir_dano(self, cantidad: float) -> bool:
        """Resta vida. Devuelve True si la nave fue destruida."""
        self.hp -= cantidad
        if self.hp <= 0:
            self.hp = 0
            self.destruir()
            return True
        return False

    def puede_disparar(self) -> bool:
        """Indica si la nave puede disparar en función de la cadencia."""
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.ultimo_disparo >= self.cadencia_ms:
            self.ultimo_disparo = tiempo_actual
            return True
        return False

    def destruir(self) -> None:
        """Acción al morir (eliminar sprite, generar chispas, etc.)"""
        self.kill()
