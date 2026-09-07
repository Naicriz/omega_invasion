
from pathlib import Path
import pygame

# Rutas relativas seguras
RUTA_BASE = Path(__file__).resolve().parent.parent.parent.parent / "assets" / "sprites" / "spaceships"
RUTA_NAVES = RUTA_BASE / "ships"
RUTA_HOJAS = RUTA_BASE / "ships"

_SPRITES = {}
_ANIMACIONES = {}

def inicializar_assets() -> None:
    """Carga y prepara todos los sprites y animaciones en memoria."""
    global _SPRITES, _ANIMACIONES
    if _SPRITES:
        return

    # 1. Cargar Nave Gris del jugador (escala 3x para pixel-art nítido de 48x48)
    ruta_nave = RUTA_NAVES / "green.png"
    if ruta_nave.exists():
        img_nave = pygame.image.load(str(ruta_nave)).convert_alpha()
        _SPRITES["jugador"] = pygame.transform.scale(img_nave, (48, 48))
    else:
        # Fallback procedural si no encontrara la imagen
        surf = pygame.Surface((44, 44), pygame.SRCALPHA)
        pygame.draw.polygon(surf, (0, 220, 255), [(22, 0), (44, 40), (22, 30), (0, 40)])
        _SPRITES["jugador"] = surf

    # 2. Cargar Proyectiles desde la hoja de proyectiles
    ruta_proyectiles = RUTA_HOJAS / "projectiles.png"
    if ruta_proyectiles.exists():
        hoja = pygame.image.load(str(ruta_proyectiles)).convert_alpha()
        
        # Proyectil Azul de Plasma (Jugador frontal)
        sub_azul = hoja.subsurface((100, 0, 300, 500))
        _SPRITES["bala_azul"] = pygame.transform.scale(sub_azul, (12, 22))

        # Proyectil Verde / Esmeralda (Cañón Omni)
        sub_verde = hoja.subsurface((100, 500, 300, 500))
        _SPRITES["bala_omni"] = pygame.transform.scale(sub_verde, (14, 20))

        # Proyectil Naranja / Rojo (Enemigos)
        sub_rojo = hoja.subsurface((600, 0, 300, 500))
        _SPRITES["bala_roja"] = pygame.transform.scale(sub_rojo, (12, 22))

    # 3. Cargar Animación del Propulsor (thruster.gif)
    ruta_thruster = RUTA_NAVES / "thruster.gif"
    if ruta_thruster.exists():
        anim_raw = pygame.image.load_animation(str(ruta_thruster))
        # Escala 3x (24x24) para alinear perfectamente con el ancho de la tobera de la nave
        _ANIMACIONES["thruster"] = [
            (pygame.transform.scale(surf, (24, 24)), dur)
            for surf, dur in anim_raw
        ]

def obtener_sprite(clave: str) -> pygame.Surface:
    """Devuelve el sprite en caché."""
    if not _SPRITES:
        inicializar_assets()
    return _SPRITES[clave]

def obtener_animacion(clave: str) -> list[tuple[pygame.Surface, float]]:
    """Devuelve la lista de tuplas (superficie, duracion_ms) de una animación en caché."""
    if not _SPRITES:
        inicializar_assets()
    return _ANIMACIONES.get(clave, [])
