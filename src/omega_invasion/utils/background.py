import random
import pygame
from omega_invasion import settings


class Estrella:
    """Representa una estrella individual en el campo estelar con velocidad y profundidad."""
    __slots__ = ("x", "y", "velocidad", "tamano", "color", "capa", "fase_brillo")

    def __init__(self, x: float, y: float, velocidad: float, tamano: int, color: pygame.Color, capa: int):
        self.x = float(x)
        self.y = float(y)
        self.velocidad = velocidad
        self.tamano = tamano
        self.color = color
        self.capa = capa
        self.fase_brillo = random.uniform(0.0, 6.28)


class EstrellaFugaz:
    """Estrella fugaz que cruza velozmente la pantalla en diagonal dejando una estela."""

    def __init__(self):
        self.activa = False
        self.x = 0.0
        self.y = 0.0
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.longitud = 0
        self.vida = 0

    def lanzar(self) -> None:
        self.activa = True
        self.x = random.uniform(50, settings.ANCHO_PANTALLA - 150)
        self.y = random.uniform(0, settings.ALTO_PANTALLA * 0.4)
        velocidad = random.uniform(14.0, 18.0)
        self.vel_x = velocidad * 0.85
        self.vel_y = velocidad * 0.55
        self.longitud = random.randint(25, 45)
        self.vida = random.randint(22, 35)

    def update(self) -> None:
        if not self.activa:
            return
        self.x += self.vel_x
        self.y += self.vel_y
        self.vida -= 1
        if self.vida <= 0 or self.x > settings.ANCHO_PANTALLA or self.y > settings.ALTO_PANTALLA:
            self.activa = False

    def dibujar(self, superficie: pygame.Surface) -> None:
        if not self.activa:
            return
        # Dibujar línea brillante con degradado
        origen = (round(self.x), round(self.y))
        fin = (round(self.x - self.vel_x * (self.longitud / 15)), round(self.y - self.vel_y * (self.longitud / 15)))
        pygame.draw.line(superficie, pygame.Color("white"), origen, fin, 2)


class FondoEstrellas:
    """Fondo espacial con múltiples capas en paralaje que genera sensación de viaje a gran velocidad."""

    def __init__(self, ancho: int = settings.ANCHO_PANTALLA, alto: int = settings.ALTO_PANTALLA):
        self.ancho = ancho
        self.alto = alto
        self.estrellas: list[Estrella] = []
        self.estrella_fugaz = EstrellaFugaz()
        self.tiempo_proxima_fugaz = random.randint(180, 360)

        # Capa 0: Lejana (Fondo profundo, estrellas tenues y lentas)
        for _ in range(55):
            x = random.uniform(0, self.ancho)
            y = random.uniform(0, self.alto)
            vel = random.uniform(0.5, 0.9)
            color = random.choice([
                pygame.Color(100, 120, 160),
                pygame.Color(120, 140, 180),
                pygame.Color(80, 100, 140)
            ])
            self.estrellas.append(Estrella(x, y, vel, 1, color, 0))

        # Capa 1: Media (Estrellas azuladas/cian de tamaño medio y velocidad intermedia)
        for _ in range(30):
            x = random.uniform(0, self.ancho)
            y = random.uniform(0, self.alto)
            vel = random.uniform(1.3, 2.0)
            color = random.choice([
                pygame.Color(160, 200, 240),
                pygame.Color(190, 230, 255),
                pygame.Color(140, 180, 220)
            ])
            self.estrellas.append(Estrella(x, y, vel, 2, color, 1))

        # Capa 2: Cercana (Estrellas rápidas, brillantes, con sensación de proximidad)
        for _ in range(16):
            x = random.uniform(0, self.ancho)
            y = random.uniform(0, self.alto)
            vel = random.uniform(2.8, 3.8)
            color = random.choice([
                pygame.Color(255, 255, 255),
                pygame.Color(230, 250, 255),
                pygame.Color(210, 245, 255)
            ])
            self.estrellas.append(Estrella(x, y, vel, 3, color, 2))

    def actualizar(self) -> None:
        """Avanza las estrellas hacia abajo creando el desplazamiento estelar."""
        for e in self.estrellas:
            e.y += e.velocidad
            # Ciclo infinito envolvente al superar el borde inferior
            if e.y >= self.alto:
                e.y = random.uniform(-10, 0)
                e.x = random.uniform(0, self.ancho)

        # Manejo de estrellas fugaces periódicas
        self.tiempo_proxima_fugaz -= 1
        if self.tiempo_proxima_fugaz <= 0 and not self.estrella_fugaz.activa:
            self.estrella_fugaz.lanzar()
            self.tiempo_proxima_fugaz = random.randint(220, 450)

        self.estrella_fugaz.update()

    def dibujar(self, superficie: pygame.Surface) -> None:
        """Renderiza todas las capas estelares optimizadamente."""
        superficie.fill(settings.COLOR_FONDO)

        # Renderizado de estrellas
        for e in self.estrellas:
            if e.tamano == 1:
                superficie.set_at((round(e.x), round(e.y)), e.color)
            else:
                rect = pygame.Rect(round(e.x), round(e.y), e.tamano, e.tamano)
                superficie.fill(e.color, rect)

        # Renderizado de estrella fugaz
        self.estrella_fugaz.dibujar(superficie)
