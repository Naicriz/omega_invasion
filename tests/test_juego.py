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


def test_propulsor_acoplado_jugador():
    """Verifica que el propulsor esté inicializado, acoplado debajo de la nave y en el orden correcto de dibujo."""
    juego = Juego()
    jugador = juego.jugador
    propulsor = jugador.propulsor

    assert propulsor is not None
    assert propulsor in juego.todos_los_sprites
    assert propulsor.rect.midtop == (jugador.rect.centerx, jugador.rect.bottom - 4)

    # El propulsor se debe dibujar antes que la nave (por debajo)
    sprites = list(juego.todos_los_sprites.sprites())
    assert sprites.index(propulsor) < sprites.index(jugador)


def test_colision_balas_mutuas():
    """Verifica que las balas del jugador y de los enemigos se destruyan mutuamente al chocar."""
    from omega_invasion.entities.bullet import Bala

    juego = Juego()
    bala_j = Bala(100, 100, 0, -1, 1, (0, 0, 0), None, juego.balas_jugador)
    bala_e = Bala(100, 100, 0, 1, 1, (0, 0, 0), None, juego.balas_enemigos)

    juego.manejar_colisiones()

    assert not bala_j.alive()
    assert not bala_e.alive()


def test_colision_bala_jugador_impacta_enemigo():
    """Verifica que una bala del jugador dañe al enemigo y la bala sea destruida."""
    from omega_invasion.entities.bullet import Bala
    from omega_invasion.entities.enemy import DronEnemigo

    juego = Juego()
    enemigo = DronEnemigo(100, 100, 1, juego.balas_enemigos, juego.todos_los_sprites, juego.enemigos)
    bala_j = Bala(100, 100, 0, -1, 1, (0, 0, 0), None, juego.balas_jugador)

    juego.manejar_colisiones()

    assert not bala_j.alive()
    assert not enemigo.alive()


def test_colision_bala_enemiga_dano_jugador():
    """Verifica que una bala enemiga reste vida al jugador y se destruya."""
    from omega_invasion.entities.bullet import Bala

    juego = Juego()
    hp_previo = juego.jugador.hp
    bala_e = Bala(juego.jugador.rect.centerx, juego.jugador.rect.centery, 0, 1, 1, (0, 0, 0), None, juego.balas_enemigos)

    juego.manejar_colisiones()

    assert not bala_e.alive()
    assert juego.jugador.hp == hp_previo - 1


def test_colision_cuerpo_a_cuerpo_enemigo_con_jugador():
    """Verifica que el impacto físico de un enemigo reste 2 puntos de vida al jugador y destruya la nave enemiga."""
    from omega_invasion.entities.enemy import DronEnemigo

    juego = Juego()
    hp_previo = juego.jugador.hp
    enemigo = DronEnemigo(juego.jugador.rect.centerx, juego.jugador.rect.centery, 1, juego.balas_enemigos, juego.todos_los_sprites, juego.enemigos)

    juego.manejar_colisiones()

    assert not enemigo.alive()
    assert juego.jugador.hp == hp_previo - 2


def test_spawn_enemigos():
    """Verifica que spawn_enemigos genere entidades en el grupo de enemigos."""
    juego = Juego()
    juego.ultimo_spawn_enemigo = -10000
    enemigos_antes = len(juego.enemigos)

    juego.spawn_enemigos()

    assert len(juego.enemigos) > enemigos_antes


def test_actualizar_pausado_con_menu():
    """Verifica que actualizar() no mueva las entidades cuando el menú de mejoras está activo."""
    juego = Juego()
    juego.menu_mejoras.activo = True

    pos_y_inicial = juego.jugador.pos.y
    juego.actualizar()

    assert juego.jugador.pos.y == pos_y_inicial


def test_muerte_jugador_activa_game_over():
    """Verifica que el menú de Game Over se abra automáticamente cuando el jugador muere."""
    from omega_invasion.entities.bullet import Bala

    juego = Juego()
    assert juego.menu_game_over.activo is False

    # Disparar daño letal al jugador
    for _ in range(5):
        Bala(juego.jugador.rect.centerx, juego.jugador.rect.centery, 0, 1, 1, (0, 0, 0), None, juego.balas_enemigos)

    juego.manejar_colisiones()

    assert not juego.jugador.alive()
    assert juego.menu_game_over.activo is True


def test_juego_reiniciar():
    """Verifica que reiniciar() restaure las entidades, grupos, HP y desactive menús."""
    from omega_invasion.entities.enemy import DronEnemigo

    juego = Juego()
    # Simular partida avanzada con entidades y menú de Game Over
    DronEnemigo(100, 100, 1, juego.balas_enemigos, juego.todos_los_sprites, juego.enemigos)
    juego.jugador.hp = 1
    juego.menu_game_over.activo = True

    juego.reiniciar()

    assert juego.jugador.alive()
    assert juego.jugador.hp == 5
    assert len(juego.enemigos) == 0
    assert juego.menu_game_over.activo is False
    assert juego.menu_mejoras.activo is False


def test_juego_reiniciar_segundos_y_upgrades():
    """Verifica que al reiniciar la partida se reinicie el tiempo jugado (0s) y todas las mejoras del jugador."""
    juego = Juego()

    # Simular progreso de partida y mejoras acumuladas
    juego.acumulador_ms_juego = 75000
    juego.segundos_jugados = 75
    juego.jugador.aplicar_mejora("canon")
    juego.jugador.aplicar_mejora("canon_omni")
    juego.jugador.aplicar_mejora("cadencia")
    juego.jugador.aplicar_mejora("velocidad")
    juego.jugador.aplicar_mejora("vida_max")
    juego.jugador.aplicar_mejora("escudo")
    juego.jugador.nivel = 6

    # Simular menú de mejoras con opciones cargadas
    juego.menu_mejoras.abrir(juego.jugador)
    assert len(juego.menu_mejoras.opciones) > 0

    # Reiniciar la partida (como tras game over)
    juego.reiniciar()

    # Verificaciones de tiempo jugado
    assert juego.segundos_jugados == 0
    assert juego.acumulador_ms_juego == 0

    # Verificaciones de upgrades y stats del jugador
    assert juego.jugador.nivel == 1
    assert juego.jugador.nivel_canon == 1
    assert juego.jugador.nivel_canon_omni == 0
    assert juego.jugador.nivel_cadencia == 1
    assert juego.jugador.nivel_dano == 1.0
    assert juego.jugador.nivel_velocidad == 1
    assert juego.jugador.nivel_vida_max == 0
    assert juego.jugador.escudo_max == 0
    assert juego.jugador.escudo_actual == 0
    assert juego.jugador.hp == 5.0
    assert juego.jugador.max_hp == 5.0
    assert juego.jugador.vel == 7.0
    assert juego.jugador.cadencia_ms == 400.0

    # Menú de mejoras limpio
    assert juego.menu_mejoras.activo is False
    assert len(juego.menu_mejoras.opciones) == 0
    assert juego.menu_mejoras.jugador_actual is None


def test_tiempo_no_avanza_durante_menus():
    """Verifica que el tiempo acumulado de juego no avance mientras un menú está activo."""
    juego = Juego()
    juego.menu_game_over.activo = True
    acumulador_antes = juego.acumulador_ms_juego

    # Simular varios ticks
    juego.actualizar()
    juego.actualizar()

    assert juego.acumulador_ms_juego == acumulador_antes


