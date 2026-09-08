import math
import random
import pygame


class ParticulaEstela(pygame.sprite.Sprite):
    """Partícula emitida por motores/propulsores que se desvanece al descender."""

    def __init__(self, x: float, y: float, color: pygame.Color, vel_x: float, vel_y: float, vida_max: int = 14, tamano: int = 4, *grupos):
        super().__init__(*grupos)
        self.pos_x = float(x)
        self.pos_y = float(y)
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.vida = vida_max
        self.vida_max = vida_max
        self.color_base = pygame.Color(color)
        self.tamano_inicial = tamano

        self.image = pygame.Surface((self.tamano_inicial, self.tamano_inicial), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(round(self.pos_x), round(self.pos_y)))
        self._actualizar_grafico()

    def _actualizar_grafico(self) -> None:
        progreso = max(0.0, self.vida / self.vida_max)
        tam = max(1, round(self.tamano_inicial * progreso))
        alfa = max(0, min(255, int(255 * progreso)))

        self.image = pygame.Surface((tam, tam), pygame.SRCALPHA)
        color = pygame.Color(self.color_base.r, self.color_base.g, self.color_base.b, alfa)
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(round(self.pos_x), round(self.pos_y)))

    def update(self) -> None:
        self.vida -= 1
        if self.vida <= 0:
            self.kill()
            return

        self.pos_x += self.vel_x
        self.pos_y += self.vel_y
        self._actualizar_grafico()


class ParticulaEscombro(pygame.sprite.Sprite):
    """Bloque expulsado en explosiones con desaceleración y cambio de color progresivo."""

    def __init__(self, x: float, y: float, color_inicial: pygame.Color, color_final: pygame.Color, vel_x: float, vel_y: float, vida_max: int = 22, tamano: int = 4, *grupos):
        super().__init__(*grupos)
        self.pos_x = float(x)
        self.pos_y = float(y)
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.vida = vida_max
        self.vida_max = vida_max
        self.color_inicial = pygame.Color(color_inicial)
        self.color_final = pygame.Color(color_final)
        self.tamano = tamano

        self.image = pygame.Surface((tamano, tamano), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(round(self.pos_x), round(self.pos_y)))
        self._actualizar_grafico()

    def _actualizar_grafico(self) -> None:
        t = 1.0 - (self.vida / self.vida_max)  # 0.0 al inicio, 1.0 al final
        # Interpolación de color
        r = int(self.color_inicial.r + (self.color_final.r - self.color_inicial.r) * t)
        g = int(self.color_inicial.g + (self.color_final.g - self.color_inicial.g) * t)
        b = int(self.color_inicial.b + (self.color_final.b - self.color_inicial.b) * t)
        alfa = int(255 * (1.0 - t))

        self.image.fill(pygame.Color(r, g, b, max(0, min(255, alfa))))

    def update(self) -> None:
        self.vida -= 1
        if self.vida <= 0:
            self.kill()
            return

        # Fricción del espacio
        self.vel_x *= 0.92
        self.vel_y *= 0.92

        self.pos_x += self.vel_x
        self.pos_y += self.vel_y
        self.rect.center = (round(self.pos_x), round(self.pos_y))
        self._actualizar_grafico()


class OndaChoque(pygame.sprite.Sprite):
    """Anillo de onda de choque de una detonación."""

    def __init__(self, x: float, y: float, radio_max: int, color: pygame.Color, vida_max: int = 16, *grupos):
        super().__init__(*grupos)
        self.centro_x = round(x)
        self.centro_y = round(y)
        self.radio_max = radio_max
        self.vida = vida_max
        self.vida_max = vida_max
        self.color = pygame.Color(color)

        diametro = radio_max * 2 + 6
        self.image = pygame.Surface((diametro, diametro), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(self.centro_x, self.centro_y))
        self._dibujar_anillo()

    def _dibujar_anillo(self) -> None:
        progreso = 1.0 - (self.vida / self.vida_max)
        radio_actual = max(2, int(self.radio_max * progreso))
        alfa = max(0, min(255, int(255 * (1.0 - progreso))))

        self.image.fill((0, 0, 0, 0))
        centro = (self.image.get_width() // 2, self.image.get_height() // 2)

        color_actual = pygame.Color(self.color.r, self.color.g, self.color.b, alfa)
        # Dibujado con trazo pixelado
        pygame.draw.circle(self.image, color_actual, centro, radio_actual, width=3)

    def update(self) -> None:
        self.vida -= 1
        if self.vida <= 0:
            self.kill()
            return
        self._dibujar_anillo()


def crear_explosion(pos: tuple[float, float], tipo_nave: str, grupo_sprites: pygame.sprite.Group) -> None:
    """Genera una explosión con onda de choque y escombros."""
    x, y = pos

    match tipo_nave:
        case "dron":
            # Explosión ágil en fuego carmesí y chispas amarillas
            OndaChoque(x, y, 26, pygame.Color("orange"), 14, grupo_sprites)
            colores = [pygame.Color("yellow"), pygame.Color("crimson"), pygame.Color("orangered"), pygame.Color("white")]
            num_particulas = 16
            vel_max = 5.5
        case "cazador":
            # Explosión de plasma violeta, magenta y cian
            OndaChoque(x, y, 32, pygame.Color("magenta"), 16, grupo_sprites)
            colores = [pygame.Color("cyan"), pygame.Color("violet"), pygame.Color("darkviolet"), pygame.Color("white")]
            num_particulas = 20
            vel_max = 6.0
        case "nodriza":
            # Gran detonación acorazada: doble onda de choque y escombros dorados / bronce
            OndaChoque(x, y, 46, pygame.Color("gold"), 20, grupo_sprites)
            OndaChoque(x, y, 28, pygame.Color("deepskyblue"), 14, grupo_sprites)
            colores = [pygame.Color("gold"), pygame.Color("darkorange"), pygame.Color("deepskyblue"), pygame.Color("white"), pygame.Color("gray40")]
            num_particulas = 32
            vel_max = 7.5
        case "jugador":
            # Explosión masiva de la nave del jugador
            OndaChoque(x, y, 50, pygame.Color("cyan"), 22, grupo_sprites)
            OndaChoque(x, y, 30, pygame.Color("aquamarine"), 16, grupo_sprites)
            colores = [pygame.Color("white"), pygame.Color("cyan"), pygame.Color("aquamarine"), pygame.Color("deepskyblue"), pygame.Color("lightgray")]
            num_particulas = 36
            vel_max = 8.0
        case _:
            OndaChoque(x, y, 25, pygame.Color("orange"), 14, grupo_sprites)
            colores = [pygame.Color("yellow"), pygame.Color("red")]
            num_particulas = 14
            vel_max = 5.0

    color_fin = pygame.Color(40, 40, 40)
    for _ in range(num_particulas):
        angulo = random.uniform(0, math.tau)
        velocidad = random.uniform(1.5, vel_max)
        vx = math.cos(angulo) * velocidad
        vy = math.sin(angulo) * velocidad
        col = random.choice(colores)
        tam = random.choice([3, 4, 5])
        vida = random.randint(14, 26)
        ParticulaEscombro(x, y, col, color_fin, vx, vy, vida, tam, grupo_sprites)
