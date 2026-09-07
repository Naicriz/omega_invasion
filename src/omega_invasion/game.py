from omega_invasion.scenes.upgrade_menu import MenuMejoras
from omega_invasion.entities.player import Jugador
from omega_invasion.entities.enemy import DronEnemigo, CazadorEnemigo, NodrizaEnemiga

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
        self.enemigos = pygame.sprite.Group()

        self.tiempo_inicio_juego = pygame.time.get_ticks()
        self.ultimo_spawn_enemigo = 0
        self.intervalo_spawn_ms = 800
        # Instanciar jugador centrado abajo (velocidad = 7 px/frame)
        self.jugador = Jugador(settings.ANCHO_PANTALLA // 2, settings.ALTO_PANTALLA - 80, 7, self.balas_jugador, self.todos_los_sprites)

        self.menu_mejoras = MenuMejoras()

    def manejar_eventos(self) -> None:
        """Procesa la cola de eventos de Pygame."""
        for evento in pygame.event.get():
            # Si el menú de mejoras está activo, se pasan los eventos a el.
            if self.menu_mejoras.activo:
                mejora_elegida = self.menu_mejoras.manejar_evento(evento)
                if mejora_elegida:
                    self.jugador.aplicar_mejora(mejora_elegida)
                continue  # No procesa eventos de movimiento si está eligiendo carta

            match evento.type:
                case pygame.QUIT:
                    self.en_ejecucion = False
                case pygame.KEYDOWN:
                    match evento.key:
                        case pygame.K_ESCAPE:
                            self.en_ejecucion = False

    def actualizar(self) -> None:
        """Actualiza el estado y la lógica de las entidades del juego."""
        # Si el menú está activo, no se actualiza la lógica del juego
        if self.menu_mejoras.activo:
            return

        self.todos_los_sprites.update()
        self.spawn_enemigos()
        self.manejar_colisiones()

    def dibujar(self) -> None:
        """Renderiza los elementos gráficos en la pantalla."""
        self.pantalla.fill(settings.COLOR_FONDO)
        self.todos_los_sprites.draw(self.pantalla)

        if self.menu_mejoras.activo:
            self.menu_mejoras.dibujar(self.pantalla)

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

        # Balas del jugador impactan balas enemigas
        pygame.sprite.groupcollide(self.balas_jugador, self.balas_enemigos, True, True) # Elimina ambas colisionadas

        # Balas del jugador impactan enemigos
        impactos = pygame.sprite.groupcollide(self.enemigos, self.balas_jugador, False, True) # groupcollide elimina la bala (True) y no al enemigo aún (False) para evaluar su vida
        for enemigo, balas in impactos.items(): # Recorre los enemigos impactados
            for bala in balas: # Recorre las balas que impactaron al enemigo
                if enemigo.recibir_dano(bala.dano): # El enemigo recibe daño
                    # Si el enemigo murió, le da experiencia al jugador
                    if self.jugador.ganar_exp(enemigo.exp_otorgada):
                        # Abre el menú de mejoras y congela el juego
                        self.menu_mejoras.abrir()
                        print(f"¡Subiste al nivel {self.jugador.nivel}!")

        # Balas enemigas impactan al jugador
        if pygame.sprite.spritecollide(self.jugador, self.balas_enemigos, True):
            self.jugador.recibir_dano(1)

        # Choque directo cuerpo a cuerpo (Nave enemiga choca con el jugador)
        enemigos_chocados = pygame.sprite.spritecollide(self.jugador, self.enemigos, True)
        for _ in enemigos_chocados:
            self.jugador.recibir_dano(2)

    def spawn_enemigos(self) -> None:
        ahora = pygame.time.get_ticks()
        segundos_jugados = (ahora - self.tiempo_inicio_juego) // 1000

        # El intervalo se reduce con el tiempo y el nivel (mínimo 280ms para no saturar la CPU)
        # Empieza en 900ms y va bajando gradualmente
        intervalo_actual = max(400, 900 - (segundos_jugados * 2) - (self.jugador.nivel * 40))

        if ahora - self.ultimo_spawn_enemigo >= intervalo_actual:
            self.ultimo_spawn_enemigo = ahora

            # Cantidad de enemigos por tanda según tiempo y nivel:
            if segundos_jugados > 90 or self.jugador.nivel >= 10:
                cantidad = random.randint(2, 3)
            elif segundos_jugados > 40 or self.jugador.nivel >= 6:
                cantidad = random.randint(1, 2)
            else:
                cantidad = 1

            # Probabilidades dinámicas: a más tiempo, más Cazadores y Nodrizas
            peso_dron = max(25, 60 - segundos_jugados // 4)
            peso_cazador = min(45, 25 + segundos_jugados // 6)
            peso_nodriza = min(30, 15 + segundos_jugados // 8)

            # Genera la tanda de enemigos
            for _ in range(cantidad):
                x_azar = random.randint(70, settings.ANCHO_PANTALLA - 70)
                tipo = random.choices(
                    ["dron", "cazador", "nodriza"],
                    weights=[peso_dron, peso_cazador, peso_nodriza]
                )[0]

                match tipo:
                    case "dron":
                        DronEnemigo(x_azar, -40, 3.2, self.balas_enemigos, self.todos_los_sprites, self.enemigos, self.todos_los_sprites)
                    case "cazador":
                        CazadorEnemigo(x_azar, -40, 2.7, self.jugador, self.balas_enemigos, self.todos_los_sprites, self.enemigos, self.todos_los_sprites)
                    case "nodriza":
                        NodrizaEnemiga(x_azar, -55, 1.8, self.balas_enemigos, self.todos_los_sprites, self.enemigos, self.todos_los_sprites)

