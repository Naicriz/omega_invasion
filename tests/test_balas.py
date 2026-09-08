import pygame
from omega_invasion.entities.bullet import Bala


def test_bala_inicializacion_y_movimiento():
    """Verifica que la bala avance según su vector de velocidad."""
    grupo = pygame.sprite.Group()
    bala = Bala(100, 100, 0.0, -10.0, 2.5, (0, 255, 255), None, grupo)

    assert bala.dano == 2.5
    assert bala.pos.x == 100
    assert bala.pos.y == 100
    assert bala in grupo

    bala.update()
    assert bala.pos.y == 90
    assert bala.rect.centery == 90


def test_bala_sale_de_pantalla_se_elimina():
    """Verifica que al salir del área de pantalla la bala se destruya automáticamente."""
    # Aseguramos que haya superficie de display activa
    superficie = pygame.display.set_mode((400, 400))
    grupo = pygame.sprite.Group()

    # Bala colocada muy arriba, fuera de pantalla
    bala = Bala(200, -50, 0.0, -10.0, 1.0, (255, 0, 0), None, grupo)
    assert bala in grupo

    bala.update()
    assert not bala.alive()
    assert bala not in grupo


def test_bola_energia_inicializacion_y_rotacion():
    """Verifica que BolaEnergia cargue el sprite solar y rote en cada update."""
    from omega_invasion.entities.bullet import BolaEnergia

    pygame.display.set_mode((400, 400))
    grupo = pygame.sprite.Group()
    bola = BolaEnergia(150, 150, 0.0, 5.0, 1, grupo)

    assert bola in grupo
    assert bola.sprite_base is not None
    assert bola.sprite_base.get_width() == 16
    assert bola.sprite_base.get_height() == 16
    angulo_inicial = bola.angulo_rotacion

    bola.update()
    assert bola.angulo_rotacion > angulo_inicial
    assert bola.rect.centery > 150
