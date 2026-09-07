import random
import pygame
from omega_invasion import settings
from omega_invasion.entities.upgrades import CATALOGO_MEJORAS


class MenuMejoras:
    def __init__(self):
        self.activo = False
        self.opciones = []
        self.rects_cartas = []
        self.fuente_titulo = pygame.font.SysFont("Arial", 28, bold=True)
        self.fuente_desc = pygame.font.SysFont("Arial", 18)
        self.fuente_tecla = pygame.font.SysFont("Arial", 22, bold=True)

    def abrir(self) -> None:
        """Elige 3 mejoras al azar y pausa el juego."""
        self.opciones = random.sample(CATALOGO_MEJORAS, 3)
        self.rects_cartas.clear()
        
        # Geometría de las 3 cartas en el centro de la pantalla
        ancho_carta = 340
        alto_carta = 260
        espaciado = 40
        x_inicial = (settings.ANCHO_PANTALLA - (3 * ancho_carta + 2 * espaciado)) // 2
        y_pos = (settings.ALTO_PANTALLA - alto_carta) // 2

        for i in range(3):
            rect = pygame.Rect(x_inicial + i * (ancho_carta + espaciado), y_pos, ancho_carta, alto_carta)
            self.rects_cartas.append(rect)
            
        self.activo = True

    def manejar_evento(self, evento: pygame.event.Event) -> str | None:
        """Detecta si el jugador eligió una carta (por clic o tecla 1, 2, 3)."""
        if not self.activo:
            return None

        # Opción 1: Clic del ratón
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            for i, rect in enumerate(self.rects_cartas):
                if rect.collidepoint(evento.pos):
                    self.activo = False
                    return self.opciones[i]["id"]

        # Opción 2: Teclado (1, 2 o 3)
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_1:
                self.activo = False
                return self.opciones[0]["id"]
            elif evento.key == pygame.K_2:
                self.activo = False
                return self.opciones[1]["id"]
            elif evento.key == pygame.K_3:
                self.activo = False
                return self.opciones[2]["id"]

        return None

    def dibujar(self, pantalla: pygame.Surface) -> None:
        if not self.activo:
            return

        # 1. Capa semitransparente oscura sobre el juego
        overlay = pygame.Surface((settings.ANCHO_PANTALLA, settings.ALTO_PANTALLA), pygame.SRCALPHA)
        overlay.fill(pygame.Color(0, 0, 0, 180))  # Negro con transparencia
        pantalla.blit(overlay, (0, 0))

        # Título superior
        texto_banner = self.fuente_titulo.render("¡SUBISTE DE NIVEL! ELIGE UNA MEJORA", True, pygame.Color("white"))
        pantalla.blit(texto_banner, texto_banner.get_rect(center=(settings.ANCHO_PANTALLA // 2, 180)))

        # 2. Dibujar las 3 cartas
        mouse_pos = pygame.mouse.get_pos()
        for i, (carta, rect) in enumerate(zip(self.opciones, self.rects_cartas)):
            es_hover = rect.collidepoint(mouse_pos)
            
            # Fondo de la carta
            color_fondo = pygame.Color("gray20") if not es_hover else pygame.Color("gray30")
            pygame.draw.rect(pantalla, color_fondo, rect, border_radius=16)
            
            # Borde brillante
            color_borde = carta["color"] if es_hover else pygame.Color("gray45")
            grosor = 4 if es_hover else 2
            pygame.draw.rect(pantalla, color_borde, rect, width=grosor, border_radius=16)

            # Número / Atajo de tecla
            tecla_txt = self.fuente_tecla.render(f"[{i + 1}]", True, carta["color"])
            pantalla.blit(tecla_txt, (rect.x + 20, rect.y + 20))

            # Título de la mejora
            tit_surf = self.fuente_titulo.render(carta["titulo"], True, pygame.Color("white"))
            pantalla.blit(tit_surf, (rect.x + 20, rect.y + 65))

            # Descripción
            desc_surf = self.fuente_desc.render(carta["desc"], True, pygame.Color("lightgray"))
            pantalla.blit(desc_surf, (rect.x + 20, rect.y + 120))
