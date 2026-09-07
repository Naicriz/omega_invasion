import pygame
from omega_invasion.scenes.game_over_menu import MenuGameOver


def test_menu_game_over_inicializacion():
    """Verifica el estado inicial del menú de Game Over."""
    menu = MenuGameOver()
    assert menu.activo is False
    assert menu.nivel == 1
    assert menu.tiempo_segundos == 0


def test_menu_game_over_abrir():
    """Verifica que abrir el menú actualice estadísticas y active la bandera."""
    menu = MenuGameOver()
    menu.abrir(nivel=5, tiempo_segundos=135)

    assert menu.activo is True
    assert menu.nivel == 5
    assert menu.tiempo_segundos == 135
    assert menu.rect_reiniciar.width > 0
    assert menu.rect_salir.width > 0


def test_menu_game_over_teclado_reiniciar():
    """Verifica que teclas R o ENTER seleccionen reiniciar."""
    menu = MenuGameOver()
    menu.abrir()

    evento_r = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r)
    assert menu.manejar_evento(evento_r) == "reiniciar"
    assert menu.activo is False

    menu.abrir()
    evento_enter = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
    assert menu.manejar_evento(evento_enter) == "reiniciar"
    assert menu.activo is False


def test_menu_game_over_teclado_salir():
    """Verifica que teclas ESC o Q seleccionen salir."""
    menu = MenuGameOver()
    menu.abrir()

    evento_esc = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)
    assert menu.manejar_evento(evento_esc) == "salir"
    assert menu.activo is False

    menu.abrir()
    evento_q = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_q)
    assert menu.manejar_evento(evento_q) == "salir"
    assert menu.activo is False


def test_menu_game_over_clic_mouse():
    """Verifica que hacer clic en los botones de reiniciar y salir funcione correctamente."""
    menu = MenuGameOver()
    menu.abrir()

    # Clic en reiniciar
    evento_click_reiniciar = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        button=1,
        pos=menu.rect_reiniciar.center
    )
    assert menu.manejar_evento(evento_click_reiniciar) == "reiniciar"
    assert menu.activo is False

    # Clic en salir
    menu.abrir()
    evento_click_salir = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        button=1,
        pos=menu.rect_salir.center
    )
    assert menu.manejar_evento(evento_click_salir) == "salir"
    assert menu.activo is False


def test_menu_game_over_dibujar():
    """Verifica que dibujar renderice sin errores tanto activo como inactivo."""
    pantalla = pygame.Surface((1280, 1280))
    menu = MenuGameOver()

    # Inactivo
    menu.dibujar(pantalla)

    # Activo
    menu.abrir(nivel=3, tiempo_segundos=75)
    menu.dibujar(pantalla)
