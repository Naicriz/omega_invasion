from omega_invasion.entities.player import Jugador
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

        # Instanciar grupo de sprites
        self.todos_los_sprites = pygame.sprite.Group()
        # Instanciar jugador centrado abajo (velocidad = 7 pixeles por frame)
        self.jugador = Jugador(settings.ANCHO_PANTALLA // 2, settings.ALTO_PANTALLA - 80, velocidad=7)
        # Agregar jugador al grupo de sprites
        self.todos_los_sprites.add(self.jugador)


    def manejar_eventos(self) -> None:
        """Procesa la cola de eventos de Pygame."""
        for evento in pygame.event.get():
            match evento.type:
                case pygame.QUIT:
                    self.en_ejecucion = False
                case pygame.KEYDOWN:
                    match evento.key:
                        case pygame.K_ESCAPE:
                            self.en_ejecucion = False

    def actualizar(self) -> None:
        """Actualiza el estado y la lógica de las entidades del juego."""
        self.jugador.update()

    def dibujar(self) -> None:
        """Renderiza los elementos gráficos en la pantalla."""
        self.pantalla.fill(settings.COLOR_FONDO)
        self.todos_los_sprites.draw(self.pantalla)
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
