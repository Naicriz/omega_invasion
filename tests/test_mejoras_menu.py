import pygame
from omega_invasion.entities.upgrades import CATALOGO_MEJORAS
from omega_invasion.scenes.upgrade_menu import MenuMejoras


def test_catalogo_mejoras_estructura():
    """Verifica que todas las mejoras del catálogo tengan los campos requeridos."""
    assert len(CATALOGO_MEJORAS) >= 5

    for mejora in CATALOGO_MEJORAS:
        assert "id" in mejora and isinstance(mejora["id"], str)
        assert "titulo" in mejora and isinstance(mejora["titulo"], str)
        assert "icono" in mejora and isinstance(mejora["icono"], str)
        assert "desc" in mejora and isinstance(mejora["desc"], str)
        assert "color" in mejora and isinstance(mejora["color"], tuple)


def test_menu_mejoras_abrir():
    """Verifica que el menú seleccione 3 opciones al azar y cree los rectángulos de las cartas."""
    menu = MenuMejoras()
    assert menu.activo is False

    menu.abrir()
    assert menu.activo is True
    assert len(menu.opciones) == 3
    assert len(menu.rects_cartas) == 3


def test_menu_mejoras_seleccion_teclado():
    """Verifica que presionar 1, 2 o 3 elija la mejora correspondiente y desactive el menú."""
    menu = MenuMejoras()
    menu.abrir()

    id_esperado = menu.opciones[0]["id"]
    evento_k1 = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_1)
    eleccion = menu.manejar_evento(evento_k1)

    assert eleccion == id_esperado
    assert menu.activo is False


def test_menu_mejoras_seleccion_mouse():
    """Verifica que hacer clic sobre una carta la seleccione."""
    menu = MenuMejoras()
    menu.abrir()

    rect_segunda_carta = menu.rects_cartas[1]
    id_esperado = menu.opciones[1]["id"]

    evento_click = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        button=1,
        pos=rect_segunda_carta.center
    )
    eleccion = menu.manejar_evento(evento_click)

    assert eleccion == id_esperado
    assert menu.activo is False


def test_menu_mejoras_dibujar():
    """Verifica que el método dibujar funcione sin errores tanto activo como inactivo."""
    pantalla = pygame.Surface((1280, 1280))
    menu = MenuMejoras()

    # Inactivo
    menu.dibujar(pantalla)

    # Activo
    menu.abrir()
    menu.dibujar(pantalla)
