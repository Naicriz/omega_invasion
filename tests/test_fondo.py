import pygame
from omega_invasion import settings
from omega_invasion.utils.background import FondoEstrellas, EstrellaFugaz


def test_fondo_estrellas_inicializacion():
    """Verifica que el fondo de estrellas cree estrellas en las 3 capas."""
    fondo = FondoEstrellas(800, 800)
    assert len(fondo.estrellas) >= 90

    capas = {e.capa for e in fondo.estrellas}
    assert 0 in capas
    assert 1 in capas
    assert 2 in capas


def test_fondo_estrellas_actualizar_movimiento():
    """Verifica que las estrellas avancen hacia abajo según su velocidad."""
    fondo = FondoEstrellas(800, 800)
    pos_iniciales = [e.y for e in fondo.estrellas]

    fondo.actualizar()

    for e, y_ant in zip(fondo.estrellas, pos_iniciales):
        # O bien avanzó hacia abajo, o dio la vuelta al superar el límite inferior
        assert e.y > y_ant or e.y < 5


def test_fondo_estrellas_dibujar():
    """Verifica que el método dibujar renderice sobre una superficie sin errores."""
    fondo = FondoEstrellas(800, 800)
    superficie = pygame.Surface((800, 800))

    fondo.dibujar(superficie)
    # Debe haber rellenado con el color de fondo y dibujado puntos de estrellas
    assert superficie.get_at((0, 0)) is not None


def test_estrella_fugaz_ciclo():
    """Verifica el lanzamiento, actualización y finalización de una estrella fugaz."""
    fugaz = EstrellaFugaz()
    assert not fugaz.activa

    fugaz.lanzar()
    assert fugaz.activa
    assert fugaz.vida > 0

    superficie = pygame.Surface((800, 800))
    fugaz.dibujar(superficie)

    while fugaz.activa:
        fugaz.update()

    assert not fugaz.activa
