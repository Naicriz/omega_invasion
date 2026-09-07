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
    """Verifica que el cañón omni empiece con 2 direcciones e incremente de 2 en 2 hasta 8."""
    grupo_sprites = pygame.sprite.Group()
    grupo_balas = pygame.sprite.Group()
    jugador = Jugador(200, 300, 7, grupo_balas, grupo_sprites)

    # Nivel 1: 1 frontal + 2 omni = 3 balas
    jugador.nivel_canon_omni = 1
    jugador.ultimo_disparo = -10000
    jugador.disparar(grupo_balas)
    assert len(grupo_balas) == 3

    # Nivel 2: 1 frontal + 4 omni = 5 balas
    grupo_balas.empty()
    jugador.nivel_canon_omni = 2
    jugador.ultimo_disparo = -10000
    jugador.disparar(grupo_balas)
    assert len(grupo_balas) == 5

    # Nivel 3: 1 frontal + 6 omni = 7 balas
    grupo_balas.empty()
    jugador.nivel_canon_omni = 3
    jugador.ultimo_disparo = -10000
    jugador.disparar(grupo_balas)
    assert len(grupo_balas) == 7

    # Nivel 4: 1 frontal + 8 omni = 9 balas
    grupo_balas.empty()
    jugador.nivel_canon_omni = 4
    jugador.ultimo_disparo = -10000
    jugador.disparar(grupo_balas)
    assert len(grupo_balas) == 9


def test_jugador_limite_mejoras():
    """Verifica la consulta de niveles y si una mejora puede seguir aplicándose."""
    grupo_balas = pygame.sprite.Group()
    jugador = Jugador(200, 300, 7, grupo_balas)

    # Cañón inicia en 1, máx 4
    assert jugador.nivel_de_mejora("canon") == 1
    assert jugador.puede_mejorar("canon", 4) is True

    jugador.aplicar_mejora("canon")  # 2
    jugador.aplicar_mejora("canon")  # 3
    jugador.aplicar_mejora("canon")  # 4
    assert jugador.nivel_de_mejora("canon") == 4
    assert jugador.puede_mejorar("canon", 4) is False

    # Omni inicia en 0, máx 4
    assert jugador.nivel_de_mejora("canon_omni") == 0
    assert jugador.puede_mejorar("canon_omni", 4) is True
    for _ in range(4):
        jugador.aplicar_mejora("canon_omni")
    assert jugador.nivel_de_mejora("canon_omni") == 4
    assert jugador.puede_mejorar("canon_omni", 4) is False


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


def test_jugador_escudo_absorbe_dano():
    """Verifica que el escudo activo absorba el daño sin restar puntos de vida (HP)."""
    grupo_balas = pygame.sprite.Group()
    jugador = Jugador(200, 300, 7, grupo_balas)

    jugador.escudo_max = 2
    jugador.escudo_actual = 2
    hp_inicial = jugador.hp

    # Primer golpe: lo absorbe el escudo
    murio = jugador.recibir_dano(1)
    assert murio is False
    assert jugador.escudo_actual == 1
    assert jugador.hp == hp_inicial

    # Segundo golpe: se agota el escudo
    murio = jugador.recibir_dano(1)
    assert murio is False
    assert jugador.escudo_actual == 0
    assert jugador.hp == hp_inicial

    # Tercer golpe: ya no hay escudo, resta vida
    murio = jugador.recibir_dano(1)
    assert murio is False
    assert jugador.escudo_actual == 0
    assert jugador.hp == hp_inicial - 1


def test_jugador_escudo_visual():
    """Verifica que la burbuja visual del escudo siga la nave y se elimine al morir."""
    grupo_sprites = pygame.sprite.Group()
    grupo_balas = pygame.sprite.Group()
    jugador = Jugador(200, 300, 7, grupo_balas, grupo_sprites)
    escudo_vis = jugador.escudo_visual

    assert escudo_vis is not None
    assert escudo_vis.rect.center == jugador.rect.center
    assert escudo_vis in grupo_sprites

    # Con escudo activo, update genera la burbuja gráfica
    jugador.escudo_actual = 1
    escudo_vis.update()
    assert escudo_vis.image.get_width() > 0

    # Al destruir la nave, el escudo visual también muere
    jugador.destruir()
    assert not escudo_vis.alive()


def test_jugador_inclinacion_lateral_y_estela(monkeypatch):
    """Verifica la inclinación lateral (banking) y la generación de partículas de estela."""
    from collections import defaultdict
    from omega_invasion.entities.effects import ParticulaEstela

    pygame.display.set_mode((400, 400))
    grupo_sprites = pygame.sprite.Group()
    grupo_balas = pygame.sprite.Group()
    jugador = Jugador(200, 200, 5, grupo_balas, grupo_sprites)

    # Simular tecla izquierda presionada
    teclas = defaultdict(bool)
    teclas[pygame.K_LEFT] = True
    monkeypatch.setattr(pygame.key, "get_pressed", lambda: teclas)

    jugador.update()
    assert jugador.angulo_inclinacion > 0  # Inclinación positiva (izquierda)

    # Simular tecla derecha presionada
    teclas.clear()
    teclas[pygame.K_RIGHT] = True
    for _ in range(5):
        jugador.update()
    assert jugador.angulo_inclinacion < 0  # Inclinación negativa (derecha)

    # Comprobar que se hayan emitido partículas de estela en el grupo
    particulas = [s for s in grupo_sprites if isinstance(s, ParticulaEstela)]
    assert len(particulas) > 0
