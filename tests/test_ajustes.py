import pygame
from omega_invasion import settings


def test_dimensiones_pantalla_validas():
    """Verifica que las dimensiones de la pantalla sean números positivos."""
    assert settings.ANCHO_PANTALLA > 0
    assert settings.ALTO_PANTALLA > 0
    assert settings.FPS > 0


def test_color_fondo_rgb_valido():
    """Verifica que el color de fondo sea un pygame.Color o tupla válida."""
    assert isinstance(settings.COLOR_FONDO, (tuple, pygame.Color))
    assert len(settings.COLOR_FONDO) in (3, 4)
    for canal in settings.COLOR_FONDO[:3]:
        assert 0 <= canal <= 255
