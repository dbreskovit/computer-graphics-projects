import pygame
from OpenGL.GL import *
from src.config import *


def draw_panel_rect(x, y, w, h):
    """Desenha caixa de fundo semitransparente"""
    glDisable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    r, g, b, a = COLOR_HUD_BG
    glColor4f(r / 255, g / 255, b / 255, a / 255)
    glBegin(GL_QUADS)
    glVertex2f(x, y);
    glVertex2f(x + w, y)
    glVertex2f(x + w, y + h);
    glVertex2f(x, y + h)
    glEnd()

    r, g, b, a = COLOR_HUD_BORDER
    glColor4f(r / 255, g / 255, b / 255, a / 255)
    glLineWidth(1.5)
    glBegin(GL_LINE_LOOP)
    glVertex2f(x, y);
    glVertex2f(x + w, y)
    glVertex2f(x + w, y + h);
    glVertex2f(x, y + h)
    glEnd()

    glDisable(GL_BLEND)
    glEnable(GL_TEXTURE_2D)


def draw_raw_text(x, y, text, font, color):
    """Função interna para renderizar a textura do texto"""
    text_surface = font.render(text, True, color)
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    width = text_surface.get_width()
    height = text_surface.get_height()

    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)

    glColor3f(1, 1, 1)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex2f(x, y)
    glTexCoord2f(1, 0)
    glVertex2f(x + width, y)
    glTexCoord2f(1, 1)
    glVertex2f(x + width, y + height)
    glTexCoord2f(0, 1)
    glVertex2f(x, y + height)
    glEnd()

    glDeleteTextures([tex_id])


def draw_text_shadow(x, y, text, font, color=COLOR_HUD_TEXT):
    """Desenha texto com sombra para garantir leitura sem fundo"""
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    draw_raw_text(x + 2, y - 2, text, font, COLOR_HUD_SHADOW)
    draw_raw_text(x, y, text, font, color)

    glDisable(GL_BLEND)


def render_hud(current_focus, fps, is_paused, font_hud, font_title):
    """
    Renderiza o HUD
    """
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, DISPLAY_WIDTH, 0, DISPLAY_HEIGHT, -1, 1)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_CULL_FACE)
    glUseProgram(0)

    commands = HUD_HELP_TEXT

    text_w, text_h = font_hud.size(commands)
    pos_x = (DISPLAY_WIDTH - text_w) // 2
    pos_y = 20

    draw_text_shadow(pos_x, pos_y, commands, font_hud, COLOR_HUD_TEXT)



    status_w, status_h = 250, 90
    sx, sy = DISPLAY_WIDTH - status_w - 20, DISPLAY_HEIGHT - status_h - 20
    draw_panel_rect(sx, sy, status_w, status_h)

    focus_name = "SOL (SISTEMA)" if current_focus is None else f"ALVO: {current_focus.upper()}"
    status_sim = "SIMULAÇÃO: PAUSADA" if is_paused else "SIMULAÇÃO: ATIVA"
    color_sim = (255, 100, 100, 255) if is_paused else (100, 255, 100, 255)

    draw_text_shadow(sx + 10, sy + 60, focus_name, font_title, COLOR_HUD_TITLE)
    draw_text_shadow(sx + 10, sy + 35, status_sim, font_hud, color_sim)
    draw_text_shadow(sx + 10, sy + 10, f"TAXA DE QUADROS: {int(fps)} FPS", font_hud)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)