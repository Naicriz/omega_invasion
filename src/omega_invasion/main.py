import sys
from omega_invasion.game import Juego


def principal() -> None:
    """Punto de entrada del juego."""
    juego = Juego()
    juego.ejecutar()
    sys.exit(0)


# Alias para retrocompatibilidad
main = principal

if __name__ == "__main__":
    principal()
