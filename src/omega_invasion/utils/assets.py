
from pathlib import Path
import pygame

# Rutas relativas seguras
RUTA_ASSETS = Path(__file__).resolve().parent.parent.parent.parent / "assets"
RUTA_BASE = RUTA_ASSETS / "sprites" / "spaceships"
RUTA_NAVES = RUTA_BASE / "ships"
RUTA_HOJAS = RUTA_BASE / "ships"
RUTA_FUENTES = RUTA_ASSETS / "fonts"
RUTA_AUDIO = RUTA_ASSETS / "audio"

_SPRITES = {}
_ANIMACIONES = {}
_FUENTES: dict[int, pygame.font.Font] = {}
_SONIDOS: dict[str, pygame.mixer.Sound] = {}

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
        pygame.draw.polygon(surf, pygame.Color("deepskyblue"), [(22, 0), (44, 40), (22, 30), (0, 40)])
        _SPRITES["jugador"] = surf

    # 2. Cargar Proyectiles desde la hoja de proyectiles
    ruta_proyectiles = RUTA_HOJAS / "projectiles.png"
    if ruta_proyectiles.exists():
        hoja = pygame.image.load(str(ruta_proyectiles)).convert_alpha()
        
        # Proyectil Azul de Plasma (Jugador frontal)
        sub_azul = hoja.subsurface((100, 0, 300, 500))
        _SPRITES["bala_azul"] = pygame.transform.scale(sub_azul, (12, 22))

        # Proyectil Verde / Esmeralda (Cañón Omni - Balas más pequeñas y compactas)
        sub_verde = hoja.subsurface((100, 500, 300, 500))
        _SPRITES["bala_omni"] = pygame.transform.scale(sub_verde, (8, 12))

        # Proyectil Naranja / Rojo (Enemigos)
        sub_rojo = hoja.subsurface((600, 0, 300, 500))
        _SPRITES["bala_roja"] = pygame.transform.scale(sub_rojo, (12, 22))

    # 3. Cargar Naves Enemigas en Pixel Art
    # Dron (Ágil, rojo)
    ruta_dron = RUTA_NAVES / "dron.png"
    if ruta_dron.exists():
        img_dron = pygame.image.load(str(ruta_dron)).convert_alpha()
        _SPRITES["dron"] = pygame.transform.scale(img_dron, (36, 36))
    else:
        surf = pygame.Surface((36, 36), pygame.SRCALPHA)
        pygame.draw.polygon(surf, pygame.Color("crimson"), [(18, 36), (0, 0), (18, 10), (36, 0)])
        _SPRITES["dron"] = surf

    # Cazador (Interceptor violeta)
    ruta_cazador = RUTA_NAVES / "cazador.png"
    if ruta_cazador.exists():
        img_cazador = pygame.image.load(str(ruta_cazador)).convert_alpha()
        _SPRITES["cazador"] = pygame.transform.scale(img_cazador, (38, 38))
    else:
        surf = pygame.Surface((38, 38), pygame.SRCALPHA)
        pygame.draw.polygon(surf, pygame.Color("darkviolet"), [(19, 38), (0, 6), (19, 14), (38, 6)])
        _SPRITES["cazador"] = surf

    # Nodriza (Nave pesada acorazada)
    ruta_nodriza = RUTA_NAVES / "nodriza.png"
    if ruta_nodriza.exists():
        img_nodriza = pygame.image.load(str(ruta_nodriza)).convert_alpha()
        _SPRITES["nodriza"] = pygame.transform.scale(img_nodriza, (56, 42))
    else:
        surf = pygame.Surface((56, 42), pygame.SRCALPHA)
        pygame.draw.polygon(surf, pygame.Color("orange"), [(28, 42), (0, 12), (14, 0), (42, 0), (56, 12)])
        pygame.draw.polygon(surf, pygame.Color("gold"), [(28, 30), (14, 10), (42, 10)])
        _SPRITES["nodriza"] = surf

    # 4. Cargar Animación del Propulsor (thruster.gif)
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

def obtener_fuente(tamano: int) -> pygame.font.Font:
    """Devuelve la fuente pixel art Press Start 2P con fallback seguro."""
    if tamano in _FUENTES:
        return _FUENTES[tamano]

    ruta_fuente = RUTA_FUENTES / "PressStart2P-Regular.ttf"
    if ruta_fuente.exists():
        fuente = pygame.font.Font(str(ruta_fuente), tamano)
    else:
        fuente = pygame.font.SysFont("Courier", tamano, bold=True)

    _FUENTES[tamano] = fuente
    return fuente

def reproducir_sonido(nombre: str, volumen: float = 0.45) -> None:
    """Reproduce un efecto de sonido retro si el mixer está disponible."""
    if not pygame.mixer.get_init():
        return

    if nombre not in _SONIDOS:
        ruta_audio = RUTA_AUDIO / f"{nombre}.wav"
        if ruta_audio.exists():
            try:
                snd = pygame.mixer.Sound(str(ruta_audio))
                _SONIDOS[nombre] = snd
            except Exception:
                return
        else:
            return

    sonido = _SONIDOS.get(nombre)
    if sonido:
        sonido.set_volume(volumen)
        sonido.play()
