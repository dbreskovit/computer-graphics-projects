from enum import Enum

# Janela
DISPLAY_WIDTH = 1200
DISPLAY_HEIGHT = 800
CAPTION = "Computação Gráfica - Sistema Solar(dbreskovit)"

# Física
TIME_SCALE = 0.5
EARTH_YEAR = 365.25
EARTH_DAY = 1.0

# Cores do HUD (R, G, B, A)
COLOR_HUD_TEXT = (255, 255, 255, 255)
COLOR_HUD_TITLE = (0, 255, 255, 255)
COLOR_HUD_BG = (0, 0, 0, 150)
COLOR_HUD_BORDER = (0, 200, 255, 200)
COLOR_HUD_SHADOW = (0, 0, 0, 255)

HUD_HELP_TEXT = "[W/S] Zoom   |   [SETAS] Câmera   |   [ESPAÇO] Tempo   |   [0] Sol   |   [1-8] Selecionar   |   [H] Interface"

# Arquivos
FONT_PATH = "assets/Orbitron-Bold.ttf"

class Textures(Enum):
    SUN = "assets/2k_sun.jpg"
    MERCURY = "assets/2k_mercury.jpg"
    VENUS = "assets/2k_venus_atmosphere.jpg"
    EARTH = "assets/2k_earth.jpg"
    MOON = "assets/2k_moon.jpg"
    MARS = "assets/2k_mars.jpg"
    JUPITER = "assets/2k_jupiter.jpg"
    SATURN = "assets/2k_saturn.jpg"
    URANUS = "assets/2k_uranus.jpg"
    NEPTUNE = "assets/2k_neptune.jpg"
    STARS = "assets/8k_stars_milky_way.jpg"
    SATURN_RING = "assets/2k_saturn_ring_alpha.png"