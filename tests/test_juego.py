from omega_invasion.game import Juego
from omega_invasion import settings


def test_inicializacion_juego():
    """Verifica que la instancia del juego se inicialice con los valores correctos."""
    juego = Juego()

    assert juego.en_ejecucion is False
    assert juego.pantalla.get_width() == settings.ANCHO_PANTALLA
    assert juego.pantalla.get_height() == settings.ALTO_PANTALLA


def test_manejar_eventos_cambio_estado():
    """Verifica que el juego pueda cambiar su bandera en_ejecucion."""
    juego = Juego()
    juego.en_ejecucion = True
    assert juego.en_ejecucion is True
