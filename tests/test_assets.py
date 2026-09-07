import pygame
from omega_invasion.utils.assets import inicializar_assets, obtener_sprite, obtener_animacion


def test_inicializar_y_obtener_sprites():
    """Verifica que los sprites se carguen y devuelvan superficies de pygame válidas."""
    inicializar_assets()

    jugador = obtener_sprite("jugador")
    assert isinstance(jugador, pygame.Surface)
    assert jugador.get_width() > 0
    assert jugador.get_height() > 0

    bala_azul = obtener_sprite("bala_azul")
    assert isinstance(bala_azul, pygame.Surface)

    bala_omni = obtener_sprite("bala_omni")
    assert isinstance(bala_omni, pygame.Surface)

    bala_roja = obtener_sprite("bala_roja")
    assert isinstance(bala_roja, pygame.Surface)


def test_obtener_animacion_thruster():
    """Verifica que la animación del propulsor cargue sus fotogramas y duraciones."""
    animacion = obtener_animacion("thruster")
    assert isinstance(animacion, list)
    assert len(animacion) > 0

    for surface, duracion in animacion:
        assert isinstance(surface, pygame.Surface)
        assert surface.get_width() == 24
        assert surface.get_height() == 24
        assert duracion > 0


def test_obtener_animacion_inexistente():
    """Verifica que una clave inexistente devuelva una lista vacía."""
    assert obtener_animacion("clave_que_no_existe") == []
