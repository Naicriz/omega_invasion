from omega_invasion.entities.player import Jugador
from omega_invasion.entities.EnemyBase import DronEnemigo
import random
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

        # Instanciar grupos de sprites para organización
        self.todos_los_sprites = pygame.sprite.Group()
        self.balas_jugador = pygame.sprite.Group()
        self.balas_enemigos = pygame.sprite.Group()
        # Instanciar enemigos
        self.enemigos = pygame.sprite.Group()
        self.ultimo_spawn_enemigo = 0
        self.intervalo_spawn_ms = 800

        # Instanciar jugador centrado abajo (velocidad = 7 pixeles por frame)
        self.jugador = Jugador(settings.ANCHO_PANTALLA // 2, settings.ALTO_PANTALLA - 80, 7, self.balas_jugador)
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
        self.todos_los_sprites.update()
        self.spawn_enemigos()
        self.manejar_colisiones()

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

    def manejar_colisiones(self) -> None:
        # 1. Balas del jugador impactan enemigos
        # groupcollide elimina la bala (True) y no al enemigo aún (False) para evaluar su vida
        impactos = pygame.sprite.groupcollide(self.enemigos, self.balas_jugador, False, True)
        for enemigo, balas in impactos.items():
            for bala in balas:
                if enemigo.recibir_dano(bala.dano):
                    # Si el enemigo murió, le da experiencia al jugador
                    if self.jugador.ganar_exp(enemigo.exp_otorgada):
                        print(f"¡Subiste al nivel {self.jugador.nivel}!")

        # 2. Balas enemigas impactan al jugador
        if pygame.sprite.spritecollide(self.jugador, self.balas_enemigos, True):
            self.jugador.recibir_dano(1)

        # 3. Choque directo cuerpo a cuerpo (Nave enemiga choca con el jugador)
        enemigos_chocados = pygame.sprite.spritecollide(self.jugador, self.enemigos, True)
        for _ in enemigos_chocados:
            self.jugador.recibir_dano(2)

    def spawn_enemigos(self) -> None:
        ahora = pygame.time.get_ticks()
        if ahora - self.ultimo_spawn_enemigo >= self.intervalo_spawn_ms:
            self.ultimo_spawn_enemigo = ahora
            x_azar = random.randint(60, settings.ANCHO_PANTALLA - 60)
            # Creamos el dron arriba de la pantalla
            DronEnemigo(x_azar, -40, 3.0, self.enemigos, self.todos_los_sprites)