import pygame
from omega_invasion.entities.effects import (
    ParticulaEstela,
    ParticulaEscombro,
    OndaChoque,
    crear_explosion
)


def test_particula_estela_ciclo_de_vida():
    """Verifica que la partícula de estela se mueva y muera al expirar su tiempo."""
    grupo = pygame.sprite.Group()
    p = ParticulaEstela(100, 100, pygame.Color("cyan"), 0.5, 2.0, 3, 4, grupo)

    assert p in grupo
    assert p.vida == 3

    p.update()
    assert p.vida == 2
    assert p.pos_x > 100
    assert p.pos_y > 100

    p.update()
    p.update()
    assert not p.alive()
    assert p not in grupo


def test_particula_escombro_friccion_y_color():
    """Verifica la desaceleración y ciclo de vida de los escombros de explosión."""
    grupo = pygame.sprite.Group()
    p = ParticulaEscombro(
        50, 50,
        pygame.Color("yellow"),
        pygame.Color("black"),
        5.0,
        -5.0,
        4,
        4,
        grupo
    )

    vel_x_inicial = p.vel_x
    p.update()
    # La velocidad debe reducirse por la fricción espacial
    assert abs(p.vel_x) < abs(vel_x_inicial)

    p.update()
    p.update()
    p.update()
    assert not p.alive()


def test_onda_choque_expansion():
    """Verifica que la onda de choque expanda su radio hasta disiparse."""
    grupo = pygame.sprite.Group()
    onda = OndaChoque(200, 200, 30, pygame.Color("orange"), 3, grupo)

    assert onda.alive()
    onda.update()
    onda.update()
    onda.update()
    assert not onda.alive()


def test_crear_explosion_distintos_tipos():
    """Verifica la creación de explosiones temáticas para cada nave."""
    grupo = pygame.sprite.Group()

    for tipo in ["dron", "cazador", "nodriza", "jugador"]:
        grupo.empty()
        crear_explosion((150, 150), tipo, grupo)
        # Debe haber generado al menos una onda de choque y varias partículas de escombros
        assert len(grupo) >= 10
        # Al actualizar varias veces, deben avanzar y consumirse
        for _ in range(30):
            grupo.update()
        assert len(grupo) == 0
