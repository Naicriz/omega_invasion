import pygame
from omega_invasion import settings


class Juego:
    """Clase principal que maneja el ciclo de vida del juego."""

    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Omega Invasion")
        self.pantalla = pygame.display.set_mode(
            (settings.ANCHO_PANTALLA, settings.ALTO_PANTALLA)
        )
        self.reloj = pygame.time.Clock()
        self.en_ejecucion = False

    def manejar_eventos(self) -> None:
        """Procesa la cola de eventos de Pygame."""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.en_ejecucion = False
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                self.en_ejecucion = False

    def actualizar(self) -> None:
        """Actualiza el estado y la lógica de las entidades del juego."""
        pass

    def dibujar(self) -> None:
        """Renderiza los elementos gráficos en la pantalla."""
        self.pantalla.fill(settings.COLOR_FONDO)
        pygame.display.flip()

    def ejecutar(self) -> None:
        """Bucle principal del juego."""
        self.en_ejecucion = True
        while self.en_ejecucion:
            self.manejar_eventos()
            self.actualizar()
            self.dibujar()
            self.reloj.tick(settings.FPS)
        pygame.quit()
