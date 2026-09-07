import pygame
from omega_invasion.entities.enemy import DronEnemigo, CazadorEnemigo, NodrizaEnemiga
from omega_invasion.entities.player import Jugador


def test_dron_enemigo_movimiento_y_salida_pantalla():
    """Verifica que el dron enemigo avance y se destruya al cruzar el límite inferior."""
    pygame.display.set_mode((400, 400))
    grupo_balas = pygame.sprite.Group()
    grupo_sprites = pygame.sprite.Group()

    dron = DronEnemigo(200, 100, 5.0, grupo_balas, grupo_sprites)

    assert dron.hp == 1
    assert dron.exp_otorgada == 25
    assert dron.pos.y == 100

    dron.update()
    assert dron.pos.y > 100  # Avanzó hacia abajo

    # Al colocarse debajo de la pantalla se debe autoeliminar
    dron.rect.top = 450
    dron.update()
    assert not dron.alive()


def test_cazador_enemigo_persigue_jugador():
    """Verifica que el cazador ajuste su movimiento horizontal hacia la posición X del jugador."""
    pygame.display.set_mode((600, 600))
    grupo_balas = pygame.sprite.Group()
    grupo_sprites = pygame.sprite.Group()

    jugador = Jugador(400, 500, 7, grupo_balas, grupo_sprites)
    # Cazador a la izquierda del jugador
    cazador = CazadorEnemigo(200, 100, 4.0, jugador, grupo_balas, grupo_sprites)

    pos_x_inicial = cazador.pos.x
    cazador.update()

    # Debe moverse hacia la derecha (hacia X=400)
    assert cazador.pos.x > pos_x_inicial


def test_nodriza_enemiga_atributos_y_disparo():
    """Verifica la vida blindada de la nodriza y su capacidad de disparo."""
    grupo_balas = pygame.sprite.Group()
    grupo_sprites = pygame.sprite.Group()

    nodriza = NodrizaEnemiga(200, 100, 2.0, grupo_balas, grupo_sprites)

    assert nodriza.hp == 6
    assert nodriza.exp_otorgada == 75
    assert nodriza.pos.y == 100

    nodriza.ultimo_disparo = -10000
    # Al forzar cadencia debe disparar doble bala
    nodriza.update()
    assert len(grupo_balas) >= 2


def test_enemigos_sprites_pixel_art():
    """Verifica que los tres enemigos usen sus respectivos sprites pixel art."""
    grupo_balas = pygame.sprite.Group()
    grupo_sprites = pygame.sprite.Group()

    dron = DronEnemigo(100, 100, 3.0, grupo_balas, grupo_sprites)
    cazador = CazadorEnemigo(100, 100, 3.0, None, grupo_balas, grupo_sprites)
    nodriza = NodrizaEnemiga(100, 100, 2.0, grupo_balas, grupo_sprites)

    assert dron.image.get_size() == (36, 36)
    assert cazador.image.get_size() == (38, 38)
    assert nodriza.image.get_size() == (56, 42)
    # Verificar que no sean superficies vacías
    assert any(dron.image.get_at((18, y))[3] > 0 for y in range(36))
    assert any(cazador.image.get_at((19, y))[3] > 0 for y in range(38))
    assert any(nodriza.image.get_at((28, y))[3] > 0 for y in range(42))

