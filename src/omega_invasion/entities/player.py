from omega_invasion.settings import NVL_DANO, NVL_CADENCIA, NVL_CANON_OMNI, NVL_CANON, EXP_ACTUAL, NVL_ACTUAL, EXP_SIGUIENTE, ESCUDO_ACTUAL, ESCUDO_MAX, NVL_VELOCIDAD
from omega_invasion.entities.bullet import Bala
from omega_invasion.entities.base import NaveBase
from omega_invasion.entities.effects import ParticulaEstela
from omega_invasion.utils.assets import obtener_sprite, obtener_animacion, reproducir_sonido

import math
import random
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


class EscudoVisual(pygame.sprite.Sprite):
    """Burbuja de energía pixelada que envuelve a la nave cuando el escudo está activo."""

    def __init__(self, nave: "Jugador", *grupos):
        super().__init__(*grupos)
        self.nave = nave
        self.tamano_baja_res = 24  # Rejilla pixel art 24x24
        self.escala = 3             # Escalado 3x a 72x72 píxeles
        self.tamano_final = self.tamano_baja_res * self.escala
        self.image = pygame.Surface((self.tamano_final, self.tamano_final), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.actualizar_posicion()

    def actualizar_posicion(self) -> None:
        if self.nave and hasattr(self.nave, "rect"):
            self.rect.center = self.nave.rect.center

    def update(self) -> None:
        if not self.nave or not self.nave.alive():
            self.kill()
            return

        self.actualizar_posicion()

        # Si no hay cargas de escudo, el sprite permanece invisible
        if self.nave.escudo_actual <= 0:
            self.image.fill((0, 0, 0, 0))
            return

        tiempo = pygame.time.get_ticks()
        # Generar superficie pixel art de baja resolución (24x24)
        surf_low = pygame.Surface((self.tamano_baja_res, self.tamano_baja_res), pygame.SRCALPHA)
        centro = 11.5
        radio_externo = 10.5 + 0.5 * math.sin(tiempo * 0.008)
        radio_interno = radio_externo - 1.8

        color_borde = pygame.Color("cyan")
        color_borde_brillo = pygame.Color("white")
        alfa_interior = int(50 + 20 * math.sin(tiempo * 0.006))
        color_interior = pygame.Color(0, 200, 255, alfa_interior)

        fase_chispa = int((tiempo // 120) % 8)

        for y in range(self.tamano_baja_res):
            dy = y - centro
            for x in range(self.tamano_baja_res):
                dx = x - centro
                dist = math.hypot(dx, dy)
                if radio_interno <= dist <= radio_externo:
                    # Borde pixel art con destellos periódicos
                    if (x + y + fase_chispa) % 5 == 0:
                        surf_low.set_at((x, y), color_borde_brillo)
                    else:
                        surf_low.set_at((x, y), color_borde)
                elif dist < radio_interno:
                    # Trama etérea dithered (tablero de ajedrez)
                    if (x + y) % 2 == 0:
                        surf_low.set_at((x, y), color_interior)

        # Escalar con vecinos más cercanos para conservar bordes pixel art nítidos
        self.image = pygame.transform.scale(surf_low, (self.tamano_final, self.tamano_final))


class Jugador(NaveBase):
    def __init__(self, eje_x: float, eje_y: float, velocidad: float, grupo_balas: pygame.sprite.Group, *grupos: tuple):
        # 1. Instanciar el propulsor en los grupos primero para que se dibuje por debajo de la nave
        self.propulsor = Propulsor(self, *grupos)
        # 2. Inicia con 5 puntos de vida, la velocidad indicada y cadencia de 400ms.
        super().__init__(eje_x, eje_y, 5, velocidad, 400, *grupos)
        self.grupo_balas = grupo_balas # Grupo donde se guardaran las balas creadas por el jugador
        self.image_base = obtener_sprite("jugador") # Sprite base sin rotar
        self.image = self.image_base.copy()
        self.rect = self.image.get_rect(center=(eje_x, eje_y)) # Obtener el rectángulo de la nave
        self.propulsor.actualizar_posicion()
        # 3. Instanciar la burbuja visual del escudo en los grupos (se dibuja encima del chasis)
        self.escudo_visual = EscudoVisual(self, *grupos)

        # --- Efectos visuales de movimiento ---
        self.angulo_inclinacion = 0.0
        self.contador_estela = 0

        # --- Sistema de Niveles y Experiencia ---
        self.nivel = NVL_ACTUAL                     # Nivel actual del jugador
        self.exp = EXP_ACTUAL                       # Experiencia actual del jugador
        self.exp_siguiente_nivel = EXP_SIGUIENTE    # Experiencia necesaria para subir de nivel

        # --- Niveles de Mejoras Permanentes ---
        self.nivel_canon = NVL_CANON                # 1..4: Balas frontales por ráfaga
        self.nivel_canon_omni = NVL_CANON_OMNI      # 0..4: 2, 4, 6, 8 direcciones omni
        self.nivel_cadencia = NVL_CADENCIA          # Reduce self.cadencia_ms
        self.nivel_dano = NVL_DANO                  # Aumenta el daño de cada proyectil
        self.nivel_velocidad = NVL_VELOCIDAD        # Aumenta self.vel
        self.nivel_vida_max = 0                     # Cantidad de mejoras de vida máxima aplicadas
        self.escudo_max = ESCUDO_MAX                # Escudos que absorben daño antes de perder HP
        self.escudo_actual = ESCUDO_ACTUAL          # Escudo actual

    def update(self):
        """Procesa las entradas y actualiza la posición del jugador con efectos visuales."""

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
        superficie = pygame.display.get_surface()
        if superficie:
            self.rect.clamp_ip(superficie.get_rect())
            self.pos = pygame.math.Vector2(self.rect.center)

        # Efecto visual de inclinación lateral (Banking)
        target_angulo = 0.0
        if direccion.x < 0:
            target_angulo = 12.0  # Se inclina a la izquierda
        elif direccion.x > 0:
            target_angulo = -12.0 # Se inclina a la derecha

        self.angulo_inclinacion += (target_angulo - self.angulo_inclinacion) * 0.35
        if abs(self.angulo_inclinacion) < 0.3:
            self.angulo_inclinacion = 0.0

        centro_prev = self.rect.center
        if self.angulo_inclinacion != 0.0:
            self.image = pygame.transform.rotate(self.image_base, self.angulo_inclinacion)
        else:
            self.image = self.image_base
        self.rect = self.image.get_rect(center=centro_prev)

        # Emisión de estela del motor de propulsión
        self.contador_estela += 1
        if self.contador_estela % 2 == 0 and self.groups():
            grupo_sprites = self.groups()[0]
            ParticulaEstela(
                self.rect.centerx + random.uniform(-3, 3),
                self.rect.bottom - 2,
                pygame.Color("cyan"),
                random.uniform(-0.4, 0.4),
                random.uniform(2.5, 4.2),
                12,
                3,
                grupo_sprites
            )

        # Sincronizar posición del propulsor y escudo con el movimiento del jugador
        if hasattr(self, "propulsor") and self.propulsor:
            self.propulsor.actualizar_posicion()
        if hasattr(self, "escudo_visual") and self.escudo_visual:
            self.escudo_visual.actualizar_posicion()

        # Dispara cuando se mantiene presionado
        if teclas[pygame.K_SPACE]:
            self.disparar(self.grupo_balas)

    def recibir_dano(self, cantidad: float) -> bool:
        """Resta vida, absorbiendo con el escudo protector primero si está activo."""
        if self.escudo_actual > 0:
            self.escudo_actual = max(0, self.escudo_actual - 1)
            reproducir_sonido("escudo_golpe")
            return False  # El escudo absorbió el golpe completo

        reproducir_sonido("dano")
        return super().recibir_dano(cantidad)

    def destruir(self) -> None:
        if hasattr(self, "propulsor") and self.propulsor:
            self.propulsor.kill()
        if hasattr(self, "escudo_visual") and self.escudo_visual:
            self.escudo_visual.kill()
        super().destruir()

    def kill(self) -> None:
        if hasattr(self, "propulsor") and self.propulsor:
            self.propulsor.kill()
        if hasattr(self, "escudo_visual") and self.escudo_visual:
            self.escudo_visual.kill()
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

    def nivel_de_mejora(self, id_mejora: str) -> int:
        """Devuelve el nivel actual alcanzado para una mejora específica."""
        match id_mejora:
            case "canon":
                return self.nivel_canon
            case "canon_omni":
                return self.nivel_canon_omni
            case "cadencia":
                return self.nivel_cadencia
            case "dano":
                return int(self.nivel_dano)
            case "velocidad":
                return self.nivel_velocidad
            case "vida_max":
                return getattr(self, "nivel_vida_max", 0)
            case "escudo":
                return self.escudo_max
            case _:
                return 0

    def puede_mejorar(self, id_mejora: str, nivel_max: int) -> bool:
        """Determina si la mejora todavía puede ser seleccionada."""
        return self.nivel_de_mejora(id_mejora) < nivel_max

    def aplicar_mejora(self, tipo_mejora: str) -> None:
        """Aplica una mejora permanente acumulativa."""
        match tipo_mejora:
            case "canon":
                self.nivel_canon += 1  # Añade más balas por ráfaga
            case "canon_omni":
                self.nivel_canon_omni += 1 # Aumenta direcciones del cañón omni (de 2 en 2)
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
                self.nivel_vida_max = getattr(self, "nivel_vida_max", 0) + 1
                self.max_hp += 1
                self.hp += 1     # Sube vida máxima y cura 1 punto
            case "escudo":
                self.escudo_max += 1
                self.escudo_actual = self.escudo_max

    def reiniciar_mejoras(self) -> None:
        """Restablece los niveles, atributos y mejoras del jugador a sus valores base."""
        self.nivel = NVL_ACTUAL
        self.exp = EXP_ACTUAL
        self.exp_siguiente_nivel = EXP_SIGUIENTE
        self.nivel_canon = NVL_CANON
        self.nivel_canon_omni = NVL_CANON_OMNI
        self.nivel_cadencia = NVL_CADENCIA
        self.nivel_dano = NVL_DANO
        self.nivel_velocidad = NVL_VELOCIDAD
        self.nivel_vida_max = 0
        self.escudo_max = ESCUDO_MAX
        self.escudo_actual = ESCUDO_ACTUAL
        self.hp = 5.0
        self.max_hp = 5.0
        self.vel = 7.0
        self.cadencia_ms = 400.0
        self.muerto = False

    def disparar(self, grupo_balas: pygame.sprite.Group) -> None:
        """Genera los proyectiles según el nivel de la mejora."""
        if not self.puede_disparar():
            return
        
        dano = self.nivel_dano # Daño base afectado por mejoras
        grupo_global = self.groups()[0] 
        sprite_bala = obtener_sprite("bala_azul")
        sprite_omni = obtener_sprite("bala_omni")

        # Sonido retro de láser
        reproducir_sonido("laser_jugador", volumen=0.15)

        # DISPARO FRONTAL VERTICAL (Básico + Mejoras de Ráfaga)
        color_frontal = pygame.Color("cyan")
        match self.nivel_canon:
            case 1:  # 1 bala central
                Bala(self.rect.centerx, self.rect.top, 0.0, -12.0, dano, color_frontal, sprite_bala, grupo_balas, grupo_global)
            case 2:  # 2 balas paralelas
                Bala(self.rect.left + 8, self.rect.top, 0.0, -12.0, dano, color_frontal, sprite_bala, grupo_balas, grupo_global)
                Bala(self.rect.right - 8, self.rect.top, 0.0, -12.0, dano, color_frontal, sprite_bala, grupo_balas, grupo_global)
            case 3:  # Nivel 3: ráfaga de 3
                Bala(self.rect.centerx, self.rect.top, 0.0, -12.0, dano, color_frontal, sprite_bala, grupo_balas, grupo_global)
                Bala(self.rect.left + 6, self.rect.top, 0.0, -12.0, dano, color_frontal, sprite_bala, grupo_balas, grupo_global)
                Bala(self.rect.right - 6, self.rect.top, 0.0, -12.0, dano, color_frontal, sprite_bala, grupo_balas, grupo_global)
            case _:  # Nivel 4 o superior: ráfaga de 4
                Bala(self.rect.centerx, self.rect.top, 0.0, -12.0, dano, color_frontal, sprite_bala, grupo_balas, grupo_global)
                Bala(self.rect.left + 6, self.rect.top, 0.0, -12.0, dano, color_frontal, sprite_bala, grupo_balas, grupo_global)
                Bala(self.rect.right - 6, self.rect.top, 0.0, -12.0, dano, color_frontal, sprite_bala, grupo_balas, grupo_global)
                Bala(self.rect.centerx, self.rect.top - 20, 0.0, -12.0, dano, color_frontal, sprite_bala, grupo_balas, grupo_global)

        # CAÑÓN OMNIDIRECCIONAL (Comienza con 2 direcciones y añade 2 por nivel hasta 8)
        if self.nivel_canon_omni > 0:
            reproducir_sonido("laser_omni", volumen=0.15)
            vel_omni = 9.0
            diag = 6.36  # 9 / sqrt(2) para velocidad consistente
            color_omni = pygame.Color("aquamarine")
            
            direcciones = []
            # Nivel 1 (2 direcciones): Laterales (Izquierda y Derecha)
            if self.nivel_canon_omni >= 1:
                direcciones.extend([(-vel_omni, 0.0), (vel_omni, 0.0)])
            # Nivel 2 (4 direcciones): Se suman Arriba y Abajo
            if self.nivel_canon_omni >= 2:
                direcciones.extend([(0.0, -vel_omni), (0.0, vel_omni)])
            # Nivel 3 (6 direcciones): Se suman Diagonales frontales (Arriba-Izq y Arriba-Der)
            if self.nivel_canon_omni >= 3:
                direcciones.extend([(-diag, -diag), (diag, -diag)])
            # Nivel 4 (8 direcciones): Se completan las Diagonales traseras (Abajo-Izq y Abajo-Der)
            if self.nivel_canon_omni >= 4:
                direcciones.extend([(-diag, diag), (diag, diag)])

            for vx, vy in direcciones:
                Bala(self.rect.centerx, self.rect.centery, vx, vy, dano * 0.8, color_omni, sprite_omni, grupo_balas, grupo_global)