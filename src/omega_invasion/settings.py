import pygame

SCREEN_WIDTH: int = 1280
SCREEN_HEIGHT: int = 1280
FPS: int = 60
BG_COLOR: pygame.Color = pygame.Color("gray8")

# Constantes en español
ANCHO_PANTALLA: int = SCREEN_WIDTH
ALTO_PANTALLA: int = SCREEN_HEIGHT
COLOR_FONDO: pygame.Color = BG_COLOR

# --- Stats iniciales ---
HP_MAX: float = 5.0
HP_ACTUAL: float = 5.0

# --- Sistema de Niveles y Experiencia ---
NVL_ACTUAL: int = 1
EXP_ACTUAL: float = 0.0
EXP_SIGUIENTE: float = 115.0

# --- Sistema de Niveles y Experiencia ---
NVL_CANON: int = 1
NVL_CANON_OMNI: int = 0
NVL_CADENCIA: int = 1
NVL_DANO: float = 1.0
NVL_VELOCIDAD: int = 1
ESCUDO_MAX: int = 0
ESCUDO_ACTUAL: int = 0
