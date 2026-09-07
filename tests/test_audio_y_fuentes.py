from pathlib import Path
import pygame
from omega_invasion.utils.assets import (
     obtener_fuente,
     reproducir_sonido,
     RUTA_FUENTES,
     RUTA_AUDIO,
 )


def test_archivo_fuente_pixel_art_existe():
    """Verifica que el archivo de fuente Press Start 2P esté en la ruta esperada."""
    ruta = RUTA_FUENTES / "PressStart2P-Regular.ttf"
    assert ruta.exists()
    assert ruta.stat().st_size > 0


def test_obtener_fuente_pixel_art():
    """Verifica que obtener_fuente retorne instancias válidas de Font y las almacene en caché."""
    fuente_12 = obtener_fuente(12)
    assert isinstance(fuente_12, pygame.font.Font)

    fuente_20 = obtener_fuente(20)
    assert isinstance(fuente_20, pygame.font.Font)

    # Comprueba la caché
    assert obtener_fuente(12) is fuente_12


def test_archivos_audio_existen():
    """Verifica que todos los archivos de sonido retro requeridos estén generados."""
    sonidos_requeridos = [
        "laser_jugador.wav",
        "laser_omni.wav",
        "laser_enemigo.wav",
        "explosion.wav",
        "subir_nivel.wav",
        "escudo_golpe.wav",
        "dano.wav",
        "game_over.wav",
    ]
    for s in sonidos_requeridos:
        archivo = RUTA_AUDIO / s
        assert archivo.exists(), f"Falta el archivo de audio: {s}"
        assert archivo.stat().st_size > 0


def test_reproducir_sonido_seguro():
    """Verifica que reproducir_sonido no lance excepciones ante sonidos válidos o inexistentes."""
    # Sonido existente
    reproducir_sonido("laser_jugador")
    # Sonido que no existe
    reproducir_sonido("sonido_fantasma_inexistente")
