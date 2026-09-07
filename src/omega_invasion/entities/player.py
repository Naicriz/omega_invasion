from omega_invasion.settings import NVL_DANO, NVL_CADENCIA, NVL_CANON_OMNI, NVL_CANON, EXP_ACTUAL, NVL_ACTUAL, EXP_SIGUIENTE, ESCUDO_ACTUAL, ESCUDO_MAX, NVL_VELOCIDAD
from omega_invasion.entities.bullet import Bala
from omega_invasion.entities.base import NaveBase
from omega_invasion.utils.assets import obtener_sprite, obtener_animacion

import pygame


class Propulsor(pygame.sprite.Sprite):
    """Efecto visual del propulsor animado que se dibuja debajo de la nave."""

    def __init__(self, nave: "Jugador", *grupos):
        super().__init__(*grupos)
        self.nave = nave
        self.animacion = obtener_animacion("thruster")
        self.indice_frame = 0
        self.tiempo_ultimo_frame = pygame.time.get_ticks()

        if self.animacion:
            self.image = self.animacion[0][0]
        else:
            self.image = pygame.Surface((24, 24), pygame.SRCALPHA)

        self.rect = self.image.get_rect()
        self.actualizar_posicion()

    def actualizar_posicion(self) -> None:
        """Ubica el propulsor centrado justo debajo de la tobera de la nave."""
        if self.nave and hasattr(self.nave, "rect"):
            self.rect.midtop = (self.nave.rect.centerx, self.nave.rect.bottom - 4)

    def update(self) -> None:
        """Avanza los fotogramas del GIF respetando su temporización original."""
        if not self.nave or not self.nave.alive():
            self.kill()
            return

        if self.animacion:
            ahora = pygame.time.get_ticks()
            duracion_frame = self.animacion[self.indice_frame][1]
            if ahora - self.tiempo_ultimo_frame >= duracion_frame:
                self.tiempo_ultimo_frame = ahora
                self.indice_frame = (self.indice_frame + 1) % len(self.animacion)
                self.image = self.animacion[self.indice_frame][0]

        self.actualizar_posicion()


class Jugador(NaveBase):
    def __init__(self, eje_x: float, eje_y: float, velocidad: float, grupo_balas: pygame.sprite.Group, *grupos: tuple):
        # 1. Instanciar el propulsor en los grupos primero para que se dibuje por debajo de la nave
        self.propulsor = Propulsor(self, *grupos)
        # 2. Inicia con 5 puntos de vida, la velocidad indicada y cadencia de 400ms.
        super().__init__(eje_x, eje_y, 5, velocidad, 400, *grupos)
        self.grupo_balas = grupo_balas # Grupo donde se guardaran las balas creadas por el jugador
        self.image = obtener_sprite("jugador") # Cargar la imagen del jugador
        self.rect = self.image.get_rect(center=(eje_x, eje_y)) # Obtener el rectángulo de la nave
        self.propulsor.actualizar_posicion()

        # --- Sistema de Niveles y Experiencia ---
        self.nivel = NVL_ACTUAL                     # Nivel actual del jugador
        self.exp = EXP_ACTUAL                       # Experiencia actual del jugador
        self.exp_siguiente_nivel = EXP_SIGUIENTE    # Experiencia necesaria para subir de nivel

        # --- Niveles de Mejoras Permanentes ---
        self.nivel_canon = NVL_CANON                # 1: Simple, 2: Doble, 3: Triple
        self.nivel_canon_omni = NVL_CANON_OMNI      # 0: No equipado, 1: Equipado (8 direcciones)
        self.nivel_cadencia = NVL_CADENCIA          # Reduce self.cadencia_ms
        self.nivel_dano = NVL_DANO                  # Aumenta el daño de cada proyectil
        self.nivel_velocidad = NVL_VELOCIDAD        # Aumenta self.vel
        self.escudo_max = ESCUDO_MAX                # Escudos que absorben daño antes de perder HP
        self.escudo_actual = ESCUDO_ACTUAL          # Escudo actual

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
    
        # Límites para no salirse de la pantalla
        self.rect.clamp_ip(pygame.display.get_surface().get_rect()) # clamp_ip es para que no se salga de la pantalla
        self.pos = pygame.math.Vector2(self.rect.center) # Actualizar la posición del vector

        # Sincronizar posición del propulsor con el movimiento del jugador
        if hasattr(self, "propulsor") and self.propulsor:
            self.propulsor.actualizar_posicion()

        # Dispara cuando se mantiene presionado
        if teclas[pygame.K_SPACE]:
            self.disparar(self.grupo_balas)

    def destruir(self) -> None:
        if hasattr(self, "propulsor") and self.propulsor:
            self.propulsor.kill()
        super().destruir()

    def kill(self) -> None:
        if hasattr(self, "propulsor") and self.propulsor:
            self.propulsor.kill()
        super().kill()

    def ganar_exp(self, cantidad: int) -> bool:
        """Suma experiencia. Devuelve True si subió de nivel."""
        self.exp += cantidad
        if self.exp >= self.exp_siguiente_nivel:
            self.exp -= self.exp_siguiente_nivel
            self.nivel += 1
            # Cada nivel pide un 50% más de XP que el anterior
            self.exp_siguiente_nivel = int(self.exp_siguiente_nivel * 1.5)
            return True  # ¡Subió de nivel!
        return False

    def aplicar_mejora(self, tipo_mejora: str) -> None:
        """Aplica una mejora permanente acumulativa."""
        match tipo_mejora:
            case "canon":
                self.nivel_canon += 1  # Añade más balas por ráfaga
            case "canon_omni":
                self.nivel_canon_omni += 1 # Equipa el cañón omni
            case "cadencia":
                self.nivel_cadencia += 1
                # Reduce el cooldown de disparo (con un límite de 30ms para no romper el juego)
                self.cadencia_ms = max(30, int(self.cadencia_ms * 0.70))
            case "dano":
                self.nivel_dano += 1
            case "velocidad":
                self.nivel_velocidad += 1
                self.vel += 0.6  # Aumenta en 0.6 px/frame permanentemente
            case "vida_max":
                self.max_hp += 1
                self.hp += 1     # Sube vida máxima y cura 1 punto
            case "escudo":
                self.escudo_max += 1
                self.escudo_actual = self.escudo_max
    
    def disparar(self, grupo_balas: pygame.sprite.Group) -> None:
        """Genera los proyectiles según el nivel de la mejora."""
        if not self.puede_disparar():
            return
        
        dano = self.nivel_dano # Daño base afectado por mejoras
        grupo_global = self.groups()[0] 
        sprite_bala = obtener_sprite("bala_azul")
        sprite_omni = obtener_sprite("bala_omni")

        # DISPARO FRONTAL VERTICAL (Básico + Mejoras de Ráfaga)
        match self.nivel_canon:
            case 1:  # 1 bala central
                Bala(self.rect.centerx, self.rect.top, 0.0, -12.0, dano, (0, 255, 255), sprite_bala, grupo_balas, grupo_global)
            case 2:  # 2 balas paralelas
                Bala(self.rect.left + 8, self.rect.top, 0.0, -12.0, dano, (0, 255, 255), sprite_bala, grupo_balas, grupo_global)
                Bala(self.rect.right - 8, self.rect.top, 0.0, -12.0, dano, (0, 255, 255), sprite_bala, grupo_balas, grupo_global)
            case 3:  # Nivel 3: ráfaga de 3
                Bala(self.rect.centerx, self.rect.top, 0.0, -12.0, dano, (0, 255, 255), sprite_bala, grupo_balas, grupo_global)
                Bala(self.rect.left + 6, self.rect.top, 0.0, -12.0, dano, (0, 255, 255), sprite_bala, grupo_balas, grupo_global)
                Bala(self.rect.right - 6, self.rect.top, 0.0, -12.0, dano, (0, 255, 255), sprite_bala, grupo_balas, grupo_global)
            case _:  # Nivel 4 o superior: ráfaga de
                Bala(self.rect.centerx, self.rect.top, 0.0, -12.0, dano, (0, 255, 255), sprite_bala, grupo_balas, grupo_global)
                Bala(self.rect.left + 6, self.rect.top, 0.0, -12.0, dano, (0, 255, 255), sprite_bala, grupo_balas, grupo_global)
                Bala(self.rect.right - 6, self.rect.top, 0.0, -12.0, dano, (0, 255, 255), sprite_bala, grupo_balas, grupo_global)
                Bala(self.rect.centerx, self.rect.top - 20, 0.0, -12.0, dano, (0, 255, 255), sprite_bala, grupo_balas, grupo_global)

        # CAÑÓN OMNIDIRECCIONAL (Dispara en todas direcciones en 360°)
        if self.nivel_canon_omni > 0:
            vel_omni = 9.0
            diag = 6.36  # 9 / sqrt(2) para que las diagonales tengan la misma velocidad
            
            # Las 8 direcciones cardinales y diagonales
            direcciones = [
                (0.0, -vel_omni),       # Arriba
                (0.0, vel_omni),        # Abajo
                (-vel_omni, 0.0),       # Izquierda
                (vel_omni, 0.0),        # Derecha
                (-diag, -diag),         # Diagonal arriba-izq
                (diag, -diag),          # Diagonal arriba-der
                (-diag, diag),          # Diagonal abajo-izq
                (diag, diag)            # Diagonal abajo-der
            ]
            for vx, vy in direcciones:
                Bala(self.rect.centerx, self.rect.centery, vx, vy, dano * 0.8, (50, 255, 200), sprite_omni, grupo_balas, grupo_global)