import pygame
from omega_invasion.entities.base import NaveBase


def test_nave_base_inicializacion():
    """Verifica que los atributos base de una nave se configuren correctamente."""
    grupo = pygame.sprite.Group()
    nave = NaveBase(100, 200, 10, 5, 250, grupo)

    assert nave.hp == 10
    assert nave.max_hp == 10
    assert nave.pos.x == 100
    assert nave.pos.y == 200
    assert nave.vel == 5
    assert nave.cadencia_ms == 250
    assert nave in grupo


def test_nave_base_recibir_dano_sobrevive():
    """Verifica que recibir daño menor a la vida restante reste vida y retorne False."""
    nave = NaveBase(0, 0, 10, 5, 100)
    murio = nave.recibir_dano(4)

    assert murio is False
    assert nave.hp == 6


def test_nave_base_recibir_dano_muere():
    """Verifica que recibir daño letal reduzca la vida a 0, retorne True y llame a destruir/kill."""
    grupo = pygame.sprite.Group()
    nave = NaveBase(0, 0, 5, 5, 100, grupo)
    murio = nave.recibir_dano(10)

    assert murio is True
    assert nave.hp == 0
    assert not nave.alive()
    assert nave not in grupo


def test_nave_base_cadencia_disparo():
    """Verifica que puede_disparar respete el intervalo en milisegundos."""
    nave = NaveBase(0, 0, 5, 5, 50)
    # Primer disparo es permitido
    assert nave.puede_disparar() is True
    # Inmediatamente después debe estar en cooldown
    assert nave.puede_disparar() is False


def test_nave_base_dano_posterior_a_muerte_retorna_false():
    """Verifica que una nave ya muerta no devuelva True ni reduzca hp negativo ante impactos múltiples."""
    nave = NaveBase(0, 0, 5, 5, 100)
    assert nave.recibir_dano(5) is True
    assert nave.hp == 0
    # Segundo impacto en el mismo frame o posterior
    assert nave.recibir_dano(5) is False
    assert nave.hp == 0
