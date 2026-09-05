import os
import pytest

# Configurar SDL en modo "dummy" (headless) antes de importar pygame.
# Esto evita que se abran ventanas gráficas o suene audio durante los tests.
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame


@pytest.fixture(scope="session", autouse=True)
def inicializar_pygame():
    """Inicializa Pygame para la sesión de pruebas y lo limpia al finalizar."""
    pygame.init()
    yield
    pygame.quit()
