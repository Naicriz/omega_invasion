import random
import pygame
from omega_invasion import settings
from omega_invasion.entities.upgrades import CATALOGO_MEJORAS
from omega_invasion.utils.assets import obtener_fuente


class MenuMejoras:
    def __init__(self):
        self.activo = False
        self.opciones = []
        self.rects_cartas = []
        self.jugador_actual = None
        self.fuente_banner = obtener_fuente(13)
        self.fuente_titulo = obtener_fuente(9)
        self.fuente_desc = obtener_fuente(8)
        self.fuente_tecla = obtener_fuente(12)

    def abrir(self, jugador=None) -> None:
        """Elige hasta 3 mejoras al azar entre las no maximizadas y pausa el juego."""
        self.jugador_actual = jugador

        if jugador:
            disponibles = [
                m for m in CATALOGO_MEJORAS
                if jugador.puede_mejorar(m["id"], m.get("nivel_max", 999))
            ]
        else:
            disponibles = list(CATALOGO_MEJORAS)

        if not disponibles:
            self.activo = False
            self.opciones.clear()
            self.rects_cartas.clear()
            return

        k = min(3, len(disponibles))
        self.opciones = random.sample(disponibles, k)
        self.rects_cartas.clear()

        # Geometría adaptada para la ventana (800x800)
        ancho_carta = 220
        alto_carta = 260
        espaciado = 20
        total_ancho = k * ancho_carta + (k - 1) * espaciado
        x_inicial = (settings.ANCHO_PANTALLA - total_ancho) // 2
        y_pos = (settings.ALTO_PANTALLA - alto_carta) // 2

        for i in range(k):
            rect = pygame.Rect(x_inicial + i * (ancho_carta + espaciado), y_pos, ancho_carta, alto_carta)
            self.rects_cartas.append(rect)

        self.activo = True

    def manejar_evento(self, evento: pygame.event.Event) -> str | None:
        """Detecta si el jugador eligió una carta (por clic o teclado numérico)."""
        if not self.activo:
            return None

        # Opción 1: Clic del ratón
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            for i, rect in enumerate(self.rects_cartas):
                if rect.collidepoint(evento.pos):
                    self.activo = False
                    return self.opciones[i]["id"]

        # Opción 2: Teclado (1, 2 o 3 según opciones disponibles)
        if evento.type == pygame.KEYDOWN:
            teclas_numeros = [
                (pygame.K_1, pygame.K_KP1),
                (pygame.K_2, pygame.K_KP2),
                (pygame.K_3, pygame.K_KP3),
            ]
            for i, pares in enumerate(teclas_numeros[:len(self.opciones)]):
                if evento.key in pares:
                    self.activo = False
                    return self.opciones[i]["id"]

        return None

    def envolver_texto(self, texto: str, fuente: pygame.font.Font, ancho_max: int) -> list[str]:
        """Divide un texto en múltiples líneas si excede el ancho máximo."""
        palabras = texto.split(" ")
        lineas = []
        linea_actual = ""
        for p in palabras:
            prueba = f"{linea_actual} {p}".strip()
            if fuente.render(prueba, True, pygame.Color("white")).get_width() <= ancho_max:
                linea_actual = prueba
            else:
                if linea_actual:
                    lineas.append(linea_actual)
                linea_actual = p
        if linea_actual:
            lineas.append(linea_actual)
        return lineas

    def dibujar(self, pantalla: pygame.Surface) -> None:
        if not self.activo:
            return

        # Capa semitransparente oscura sobre el juego
        overlay = pygame.Surface((settings.ANCHO_PANTALLA, settings.ALTO_PANTALLA), pygame.SRCALPHA)
        overlay.fill(pygame.Color(0, 0, 0, 190))
        pantalla.blit(overlay, (0, 0))

        # Título superior
        texto_banner = self.fuente_banner.render("¡SUBISTE DE NIVEL! ELIGE UNA MEJORA", True, pygame.Color("white"))
        banner_y = max(50, (settings.ALTO_PANTALLA - 260) // 2 - 50)
        pantalla.blit(texto_banner, texto_banner.get_rect(center=(settings.ANCHO_PANTALLA // 2, banner_y)))

        # Dibujar las cartas
        mouse_pos = pygame.mouse.get_pos()
        for i, (carta, rect) in enumerate(zip(self.opciones, self.rects_cartas)):
            es_hover = rect.collidepoint(mouse_pos)

            # Fondo de la carta
            color_fondo = pygame.Color("gray22") if not es_hover else pygame.Color("gray32")
            pygame.draw.rect(pantalla, color_fondo, rect, border_radius=12)

            # Borde brillante
            color_borde = carta["color"] if es_hover else pygame.Color("gray45")
            grosor = 4 if es_hover else 2
            pygame.draw.rect(pantalla, color_borde, rect, width=grosor, border_radius=12)

            # Número / Atajo de tecla
            tecla_txt = self.fuente_tecla.render(f"[{i + 1}]", True, carta["color"])
            pantalla.blit(tecla_txt, (rect.x + 16, rect.y + 16))

            # Título de la mejora
            tit_surf = self.fuente_titulo.render(carta["titulo"], True, pygame.Color("white"))
            pantalla.blit(tit_surf, (rect.x + 16, rect.y + 55))

            # Indicador de nivel si se conoce el jugador
            if self.jugador_actual:
                nvl_actual = self.jugador_actual.nivel_de_mejora(carta["id"])
                nvl_sig = nvl_actual + 1
                max_nvl = carta.get("nivel_max", "?")
                txt_nvl = self.fuente_desc.render(f"NIVEL {nvl_sig}/{max_nvl}", True, carta["color"])
                pantalla.blit(txt_nvl, (rect.x + 16, rect.y + 80))

            # Línea divisoria decorativa
            pygame.draw.line(pantalla, pygame.Color("gray40"), (rect.x + 16, rect.y + 105), (rect.right - 16, rect.y + 105), 1)

            # Descripción
            lineas_desc = self.envolver_texto(carta["desc"], self.fuente_desc, rect.width - 32)
            for idx, lin in enumerate(lineas_desc):
                desc_surf = self.fuente_desc.render(lin, True, pygame.Color("lightgray"))
                pantalla.blit(desc_surf, (rect.x + 16, rect.y + 125 + idx * 18))
