import pygame
from omega_invasion import settings
from omega_invasion.utils.assets import obtener_fuente, reproducir_sonido


class MenuGameOver:
    """Menú de fin de partida (Game Over) que permite reiniciar o salir del juego."""

    def __init__(self) -> None:
        self.activo: bool = False
        self.nivel: int = 1
        self.tiempo_segundos: int = 0

        self.fuente_titulo = obtener_fuente(22)
        self.fuente_stats = obtener_fuente(10)
        self.fuente_boton = obtener_fuente(12)
        self.fuente_subtexto = obtener_fuente(9)

        ancho_btn = 320
        alto_btn = 60
        self.rect_reiniciar = pygame.Rect(0, 0, ancho_btn, alto_btn)
        self.rect_salir = pygame.Rect(0, 0, ancho_btn, alto_btn)

    def abrir(self, nivel: int = 1, tiempo_segundos: int = 0) -> None:
        """Activa el menú, calcula la posición de sus elementos y reproduce sonido de derrota."""
        self.nivel = nivel
        self.tiempo_segundos = tiempo_segundos

        cx = settings.ANCHO_PANTALLA // 2
        cy = settings.ALTO_PANTALLA // 2

        self.rect_reiniciar.center = (cx, cy + 40)
        self.rect_salir.center = (cx, cy + 125)
        self.activo = True
        reproducir_sonido("game_over")

    def manejar_evento(self, evento: pygame.event.Event) -> str | None:
        """Procesa entradas de ratón y teclado. Retorna 'reiniciar', 'salir' o None."""
        if not self.activo:
            return None

        # Opción 1: Clic de ratón
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.rect_reiniciar.collidepoint(evento.pos):
                self.activo = False
                return "reiniciar"
            elif self.rect_salir.collidepoint(evento.pos):
                self.activo = False
                return "salir"

        # Opción 2: Atajos de teclado
        if evento.type == pygame.KEYDOWN:
            if evento.key in (pygame.K_r, pygame.K_RETURN, pygame.K_KP_ENTER):
                self.activo = False
                return "reiniciar"
            elif evento.key in (pygame.K_ESCAPE, pygame.K_q):
                self.activo = False
                return "salir"

        return None

    def dibujar(self, pantalla: pygame.Surface) -> None:
        """Dibuja el overlay semitransparente, panel de derrota y botones interactivos."""
        if not self.activo:
            return

        # Capa semitransparente oscura
        overlay = pygame.Surface((settings.ANCHO_PANTALLA, settings.ALTO_PANTALLA), pygame.SRCALPHA)
        overlay.fill(pygame.Color(0, 0, 0, 210))
        pantalla.blit(overlay, (0, 0))

        # Panel central
        panel_ancho = 480
        panel_alto = 360
        cx = settings.ANCHO_PANTALLA // 2
        cy = settings.ALTO_PANTALLA // 2
        panel_rect = pygame.Rect(0, 0, panel_ancho, panel_alto)
        panel_rect.center = (cx, cy)

        pygame.draw.rect(pantalla, pygame.Color("gray15"), panel_rect, border_radius=20)
        pygame.draw.rect(pantalla, pygame.Color("crimson"), panel_rect, width=3, border_radius=20)

        # Título de derrota
        tit_surf = self.fuente_titulo.render("FIN DEL JUEGO", True, pygame.Color("crimson"))
        pantalla.blit(tit_surf, tit_surf.get_rect(center=(cx, panel_rect.top + 45)))

        # Estadísticas
        minutos = self.tiempo_segundos // 60
        segs = self.tiempo_segundos % 60
        stats_texto = f"Nivel alcanzado: {self.nivel}   |   Tiempo: {minutos:02d}:{segs:02d}"
        stats_surf = self.fuente_stats.render(stats_texto, True, pygame.Color("lightgray"))
        pantalla.blit(stats_surf, stats_surf.get_rect(center=(cx, panel_rect.top + 95)))

        # Botones
        mouse_pos = pygame.mouse.get_pos()

        # Botón Reiniciar
        hover_reiniciar = self.rect_reiniciar.collidepoint(mouse_pos)
        bg_reiniciar = pygame.Color("gray25") if hover_reiniciar else pygame.Color("gray20")
        borde_reiniciar = pygame.Color("springgreen") if hover_reiniciar else pygame.Color("gray45")
        grosor_reiniciar = 3 if hover_reiniciar else 1

        pygame.draw.rect(pantalla, bg_reiniciar, self.rect_reiniciar, border_radius=12)
        pygame.draw.rect(pantalla, borde_reiniciar, self.rect_reiniciar, width=grosor_reiniciar, border_radius=12)

        txt_reiniciar = self.fuente_boton.render("REINICIAR", True, pygame.Color("white") if hover_reiniciar else pygame.Color("lightgray"))
        pantalla.blit(txt_reiniciar, txt_reiniciar.get_rect(center=(cx, self.rect_reiniciar.centery - 8)))
        sub_reiniciar = self.fuente_subtexto.render("[ R / ENTER ]", True, pygame.Color("springgreen") if hover_reiniciar else pygame.Color("gray60"))
        pantalla.blit(sub_reiniciar, sub_reiniciar.get_rect(center=(cx, self.rect_reiniciar.centery + 14)))

        # Botón Salir
        hover_salir = self.rect_salir.collidepoint(mouse_pos)
        bg_salir = pygame.Color("gray25") if hover_salir else pygame.Color("gray20")
        borde_salir = pygame.Color("tomato") if hover_salir else pygame.Color("gray45")
        grosor_salir = 3 if hover_salir else 1

        pygame.draw.rect(pantalla, bg_salir, self.rect_salir, border_radius=12)
        pygame.draw.rect(pantalla, borde_salir, self.rect_salir, width=grosor_salir, border_radius=12)

        txt_salir = self.fuente_boton.render("SALIR DEL JUEGO", True, pygame.Color("white") if hover_salir else pygame.Color("lightgray"))
        pantalla.blit(txt_salir, txt_salir.get_rect(center=(cx, self.rect_salir.centery - 8)))
        sub_salir = self.fuente_subtexto.render("[ ESC / Q ]", True, pygame.Color("tomato") if hover_salir else pygame.Color("gray60"))
        pantalla.blit(sub_salir, sub_salir.get_rect(center=(cx, self.rect_salir.centery + 14)))
