import pygame
from omega_invasion import settings
from omega_invasion.entities.upgrades import CATALOGO_MEJORAS
from omega_invasion.scenes.upgrade_menu import MenuMejoras


def test_catalogo_mejoras_estructura():
    """Verifica que todas las mejoras del catálogo tengan los campos requeridos y nivel_max."""
    assert len(CATALOGO_MEJORAS) >= 5

    for mejora in CATALOGO_MEJORAS:
        assert "id" in mejora and isinstance(mejora["id"], str)
        assert "titulo" in mejora and isinstance(mejora["titulo"], str)
        assert "icono" in mejora and isinstance(mejora["icono"], str)
        assert "color" in mejora and isinstance(mejora["color"], (tuple, pygame.Color))
        assert "nivel_max" in mejora and isinstance(mejora["nivel_max"], int) and mejora["nivel_max"] > 0


def test_menu_mejoras_abrir():
    """Verifica que el menú seleccione hasta 3 opciones al azar y cree los rectángulos de las cartas."""
    menu = MenuMejoras()
    assert menu.activo is False

    menu.abrir()
    assert menu.activo is True
    assert len(menu.opciones) == 3
    assert len(menu.rects_cartas) == 3


def test_menu_mejoras_tamano_cartas_adecuado():
    """Verifica que las cartas se adapten y no desborden la resolución de la pantalla."""
    menu = MenuMejoras()
    menu.abrir()

    for rect in menu.rects_cartas:
        assert rect.left >= 0
        assert rect.right <= settings.ANCHO_PANTALLA
        assert rect.top >= 0
        assert rect.bottom <= settings.ALTO_PANTALLA


def test_menu_mejoras_filtra_mejoras_maximizadas():
    """Verifica que si una mejora alcanza su nivel máximo, ya no se ofrezca en el menú."""
    from omega_invasion.entities.player import Jugador

    grupo_balas = pygame.sprite.Group()
    jugador = Jugador(200, 200, 5, grupo_balas)

    # Maximizar cañón omni (máx 4) y cañón (máx 4)
    jugador.nivel_canon_omni = 4
    jugador.nivel_canon = 4

    menu = MenuMejoras()
    # Abrir muchas veces para comprobar que nunca aparezcan 'canon' ni 'canon_omni'
    for _ in range(20):
        menu.abrir(jugador)
        assert menu.activo is True
        ids_mostrados = [opt["id"] for opt in menu.opciones]
        assert "canon" not in ids_mostrados
        assert "canon_omni" not in ids_mostrados


def test_menu_mejoras_todas_maximizadas_no_abre():
    """Verifica que si todas las mejoras están completadas, el menú no se active."""
    from omega_invasion.entities.player import Jugador

    grupo_balas = pygame.sprite.Group()
    jugador = Jugador(200, 200, 5, grupo_balas)

    # Maximizar todas las mejoras del catálogo
    jugador.nivel_canon = 4
    jugador.nivel_canon_omni = 4
    jugador.nivel_cadencia = 5
    jugador.nivel_dano = 5
    jugador.nivel_velocidad = 5
    jugador.nivel_vida_max = 5
    jugador.escudo_max = 3

    menu = MenuMejoras()
    menu.abrir(jugador)
    assert menu.activo is False
    assert len(menu.opciones) == 0


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
    pantalla = pygame.Surface((800, 800))
    menu = MenuMejoras()

    # Inactivo
    menu.dibujar(pantalla)

    # Activo
    menu.abrir()
    menu.dibujar(pantalla)
