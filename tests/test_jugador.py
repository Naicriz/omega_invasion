import pygame
from omega_invasion.entities.player import Jugador, Propulsor


def test_jugador_inicializacion():
    """Verifica la configuración inicial del jugador y su propulsor."""
    grupo_sprites = pygame.sprite.Group()
    grupo_balas = pygame.sprite.Group()

    jugador = Jugador(200, 300, 7, grupo_balas, grupo_sprites)

    assert jugador.hp == 5
    assert jugador.vel == 7
    assert jugador.nivel == 1
    assert jugador.rect.center == (200, 300)
    assert isinstance(jugador.propulsor, Propulsor)
    assert jugador in grupo_sprites
    assert jugador.propulsor in grupo_sprites


def test_jugador_ganar_exp_sube_nivel():
    """Verifica que el jugador acumule experiencia y suba de nivel."""
    grupo_balas = pygame.sprite.Group()
    jugador = Jugador(200, 300, 7, grupo_balas)

    exp_inicial = jugador.exp_siguiente_nivel
    subio = jugador.ganar_exp(exp_inicial - 10)
    assert subio is False
    assert jugador.nivel == 1

    # Supera el umbral
    subio = jugador.ganar_exp(20)
    assert subio is True
    assert jugador.nivel == 2
    assert jugador.exp_siguiente_nivel == int(exp_inicial * 1.5)


def test_jugador_aplicar_mejoras():
    """Verifica que cada mejora modifique las estadísticas correspondientes."""
    grupo_balas = pygame.sprite.Group()
    jugador = Jugador(200, 300, 7, grupo_balas)

    # Cañón
    canon_previo = jugador.nivel_canon
    jugador.aplicar_mejora("canon")
    assert jugador.nivel_canon == canon_previo + 1

    # Cañón Omni
    jugador.aplicar_mejora("canon_omni")
    assert jugador.nivel_canon_omni == 1

    # Cadencia
    cadencia_previa = jugador.cadencia_ms
    jugador.aplicar_mejora("cadencia")
    assert jugador.cadencia_ms < cadencia_previa

    # Daño
    dano_previo = jugador.nivel_dano
    jugador.aplicar_mejora("dano")
    assert jugador.nivel_dano == dano_previo + 1

    # Velocidad
    vel_previa = jugador.vel
    jugador.aplicar_mejora("velocidad")
    assert jugador.vel == vel_previa + 0.6

    # Vida máxima
    hp_previo = jugador.max_hp
    jugador.aplicar_mejora("vida_max")
    assert jugador.max_hp == hp_previo + 1
    assert jugador.hp == hp_previo + 1

    # Escudo
    jugador.aplicar_mejora("escudo")
    assert jugador.escudo_max == 1
    assert jugador.escudo_actual == 1


def test_jugador_disparar_crea_balas():
    """Verifica que disparar cree proyectiles en el grupo de balas."""
    grupo_sprites = pygame.sprite.Group()
    grupo_balas = pygame.sprite.Group()
    jugador = Jugador(200, 300, 7, grupo_balas, grupo_sprites)

    jugador.disparar(grupo_balas)
    assert len(grupo_balas) == 1  # 1 bala frontal básica al nivel 1 de cañón

    # Cooldown activo, no debe disparar de inmediato
    jugador.disparar(grupo_balas)
    assert len(grupo_balas) == 1


def test_jugador_disparo_omni():
    """Verifica que el cañón omni dispare 8 proyectiles adicionales."""
    grupo_sprites = pygame.sprite.Group()
    grupo_balas = pygame.sprite.Group()
    jugador = Jugador(200, 300, 7, grupo_balas, grupo_sprites)
    jugador.nivel_canon_omni = 1
    # Forzar fin de enfriamiento
    jugador.ultimo_disparo = -10000

    jugador.disparar(grupo_balas)
    # 1 bala frontal + 8 balas omnidireccionales = 9 balas
    assert len(grupo_balas) == 9


def test_jugador_destruir_elimina_propulsor():
    """Verifica que al matar o destruir al jugador, el propulsor también muera."""
    grupo_sprites = pygame.sprite.Group()
    grupo_balas = pygame.sprite.Group()
    jugador = Jugador(200, 300, 7, grupo_balas, grupo_sprites)
    propulsor = jugador.propulsor

    assert jugador.alive()
    assert propulsor.alive()

    jugador.destruir()

    assert not jugador.alive()
    assert not propulsor.alive()
