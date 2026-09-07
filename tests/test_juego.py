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

