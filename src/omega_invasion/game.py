from omega_invasion.scenes.upgrade_menu import MenuMejoras
from omega_invasion.scenes.game_over_menu import MenuGameOver
from omega_invasion.entities.player import Jugador
from omega_invasion.entities.enemy import DronEnemigo, CazadorEnemigo, NodrizaEnemiga
from omega_invasion.entities.effects import crear_explosion
from omega_invasion.utils.assets import reproducir_sonido

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

        # Menús interactivos
        self.menu_mejoras = MenuMejoras()
        self.menu_game_over = MenuGameOver()
        self.shake_intensidad = 0.0

        # Configurar partida inicial
        self.reiniciar()

    def reiniciar(self) -> None:
        """Restablece el estado de la partida a sus valores iniciales."""
        self.todos_los_sprites.empty()
        self.balas_jugador.empty()
        self.balas_enemigos.empty()
        self.enemigos.empty()

        self.tiempo_inicio_juego = pygame.time.get_ticks()
        self.ultimo_spawn_enemigo = 0
        self.intervalo_spawn_ms = 800
        self.shake_intensidad = 0.0

        # Instanciar jugador centrado abajo (velocidad = 7 px/frame)
        self.jugador = Jugador(
            settings.ANCHO_PANTALLA // 2,
            settings.ALTO_PANTALLA - 80,
            7,
            self.balas_jugador,
            self.todos_los_sprites
        )

        self.menu_mejoras.activo = False
        self.menu_game_over.activo = False

    def manejar_eventos(self) -> None:
        """Procesa la cola de eventos de Pygame."""
        for evento in pygame.event.get():
            # Si el menú de Game Over está activo, procesa sus eventos
            if self.menu_game_over.activo:
                accion = self.menu_game_over.manejar_evento(evento)
                if accion == "reiniciar":
                    self.reiniciar()
                elif accion == "salir":
                    self.en_ejecucion = False
                continue

            # Si el menú de mejoras está activo, se pasan los eventos a él.
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
        # Si algún menú está activo, no se actualiza la lógica del juego
        if self.menu_mejoras.activo or self.menu_game_over.activo:
            return

        # Reducción paulatina de la sacudida de pantalla
        if self.shake_intensidad > 0:
            self.shake_intensidad = max(0.0, self.shake_intensidad - 0.6)

        self.todos_los_sprites.update()
        self.spawn_enemigos()
        self.manejar_colisiones()

    def dibujar(self) -> None:
        """Renderiza los elementos gráficos en la pantalla con soporte para sacudida (screen shake)."""
        self.pantalla.fill(settings.COLOR_FONDO)

        if self.shake_intensidad > 0.1:
            max_offset = max(1, int(self.shake_intensidad))
            offset_x = random.randint(-max_offset, max_offset)
            offset_y = random.randint(-max_offset, max_offset)
            surf_mundo = pygame.Surface((settings.ANCHO_PANTALLA, settings.ALTO_PANTALLA))
            surf_mundo.fill(settings.COLOR_FONDO)
            self.todos_los_sprites.draw(surf_mundo)
            self.pantalla.blit(surf_mundo, (offset_x, offset_y))
        else:
            self.todos_los_sprites.draw(self.pantalla)

        if self.menu_mejoras.activo:
            self.menu_mejoras.dibujar(self.pantalla)
        elif self.menu_game_over.activo:
            self.menu_game_over.dibujar(self.pantalla)

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
        impactos = pygame.sprite.groupcollide(self.enemigos, self.balas_jugador, False, True)
        for enemigo, balas in impactos.items():
            for bala in balas:
                if enemigo.recibir_dano(bala.dano):
                    reproducir_sonido("explosion", volumen=0.25)

                    # Efecto visual de explosión con screen shake según el tipo de nave
                    if isinstance(enemigo, DronEnemigo):
                        tipo = "dron"
                        shake = 3.5
                    elif isinstance(enemigo, CazadorEnemigo):
                        tipo = "cazador"
                        shake = 4.5
                    else:
                        tipo = "nodriza"
                        shake = 8.0

                    crear_explosion(enemigo.rect.center, tipo, self.todos_los_sprites)
                    self.shake_intensidad = max(self.shake_intensidad, shake)

                    # Si el enemigo murió, le da experiencia al jugador
                    if self.jugador.ganar_exp(enemigo.exp_otorgada):
                        reproducir_sonido("subir_nivel")
                        # Abre el menú de mejoras y congela el juego si hay mejoras disponibles
                        self.menu_mejoras.abrir(self.jugador)
                        print(f"¡Subiste al nivel {self.jugador.nivel}!")

        # Balas enemigas impactan al jugador
        balas_impactadas = pygame.sprite.spritecollide(self.jugador, self.balas_enemigos, True)
        for _ in balas_impactadas:
            if self.jugador.recibir_dano(1):
                crear_explosion(self.jugador.rect.center, "jugador", self.todos_los_sprites)
                self.shake_intensidad = 10.0

        # Choque directo cuerpo a cuerpo (Nave enemiga choca con el jugador)
        enemigos_chocados = pygame.sprite.spritecollide(self.jugador, self.enemigos, True)
        for enemigo in enemigos_chocados:
            tipo = "dron" if isinstance(enemigo, DronEnemigo) else ("cazador" if isinstance(enemigo, CazadorEnemigo) else "nodriza")
            crear_explosion(enemigo.rect.center, tipo, self.todos_los_sprites)
            self.shake_intensidad = max(self.shake_intensidad, 6.0)

            if self.jugador.recibir_dano(2):
                crear_explosion(self.jugador.rect.center, "jugador", self.todos_los_sprites)
                self.shake_intensidad = 10.0

        # Si el jugador fue destruido, se abre el menú de fin de partida
        if not self.jugador.alive():
            segundos_jugados = (pygame.time.get_ticks() - self.tiempo_inicio_juego) // 1000
            self.menu_game_over.abrir(
                nivel=self.jugador.nivel,
                tiempo_segundos=segundos_jugados
            )

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

