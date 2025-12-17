import random
import os

from src.config import *
from src.shaders import compile_sun_shader
from src.graphics import *
from src.ui import render_hud


def init_opengl():
    glViewport(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (DISPLAY_WIDTH / DISPLAY_HEIGHT), 0.1, 3000.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)


def main():
    pygame.init()
    pygame.font.init()

    # Fontes
    if os.path.exists(FONT_PATH):
        font_hud = pygame.font.Font(FONT_PATH, 12)
        font_title = pygame.font.Font(FONT_PATH, 14)
    else:
        font_hud = pygame.font.SysFont('Arial', 12)
        font_title = pygame.font.SysFont('Arial', 14, bold=True)

    # Janela
    pygame.display.gl_set_attribute(pygame.GL_DEPTH_SIZE, 24)
    pygame.display.gl_set_attribute(pygame.GL_DOUBLEBUFFER, 1)
    pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
    pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)
    screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), DOUBLEBUF | OPENGL)
    pygame.display.set_caption(CAPTION)

    init_opengl()
    sun_shader_program = compile_sun_shader()

    print("Carregando texturas...")
    tex_sol = load_texture(Textures.SUN.value)
    tex_stars = load_texture(Textures.STARS.value)
    tex_moon = load_texture(Textures.MOON.value)
    tex_ring_sat = load_texture(Textures.SATURN_RING.value)

    # Dados dos Planetas
    planets = [
        {"name": "Mercurio", "dist": 7.0, "rad": 0.38, "tex": Textures.MERCURY, "o_speed": 4.14, "r_speed": 0.017},
        {"name": "Venus", "dist": 12.0, "rad": 0.95, "tex": Textures.VENUS, "o_speed": 1.62, "r_speed": -0.004},
        {"name": "Terra", "dist": 18.0, "rad": 1.00, "tex": Textures.EARTH, "o_speed": 1.00, "r_speed": 1.00,
         "moon": True},
        {"name": "Marte", "dist": 24.0, "rad": 0.53, "tex": Textures.MARS, "o_speed": 0.53, "r_speed": 0.97},
        {"name": "Jupiter", "dist": 45.0, "rad": 2.50, "tex": Textures.JUPITER, "o_speed": 0.08, "r_speed": 2.4},
        {"name": "Saturno", "dist": 70.0, "rad": 2.10, "tex": Textures.SATURN, "o_speed": 0.03, "r_speed": 2.2,
         "ring": tex_ring_sat},
        {"name": "Urano", "dist": 95.0, "rad": 1.50, "tex": Textures.URANUS, "o_speed": 0.01, "r_speed": -1.4},
        {"name": "Netuno", "dist": 120.0, "rad": 1.45, "tex": Textures.NEPTUNE, "o_speed": 0.006, "r_speed": 1.5},
    ]

    for p in planets:
        p["tex_id"] = load_texture(p["tex"].value)
        p["angle"] = random.uniform(0, 360)

    camera_zoom = -150.0
    camera_rot_x = 30.0
    camera_rot_y = 0.0
    focus_target = None
    is_paused = False
    show_hud = True
    sim_time = 0

    clock = pygame.time.Clock()
    running = True

    while running:
        dt = clock.tick(60)
        fps = clock.get_fps()

        for event in pygame.event.get():
            if event.type == QUIT: running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: running = False
                if event.key == K_0: focus_target = None; camera_zoom = -150.0
                if event.key == K_1: focus_target = 0
                if event.key == K_2: focus_target = 1
                if event.key == K_3: focus_target = 2
                if event.key == K_4: focus_target = 3
                if event.key == K_5: focus_target = 4
                if event.key == K_6: focus_target = 5
                if event.key == K_7: focus_target = 6
                if event.key == K_8: focus_target = 7

                if event.key == K_SPACE: is_paused = not is_paused
                if event.key == K_h: show_hud = not show_hud

                if event.key in [K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8]:
                    idx = focus_target
                    camera_zoom = -(planets[idx]['rad'] * 5.0 + 3.0)

        if not is_paused:
            sim_time += dt

        keys = pygame.key.get_pressed()
        if keys[K_LEFT]: camera_rot_y -= 1.5
        if keys[K_RIGHT]: camera_rot_y += 1.5
        if keys[K_UP]: camera_rot_x -= 1.5
        if keys[K_DOWN]: camera_rot_x += 1.5
        if keys[K_w]: camera_zoom += 2.0
        if keys[K_s]: camera_zoom -= 2.0
        if camera_zoom > -2: camera_zoom = -2

        glClearColor(0.01, 0.01, 0.01, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glEnable(GL_LIGHTING)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)

        glTranslatef(0, 0, camera_zoom)
        glRotate(camera_rot_x, 1, 0, 0)
        glRotate(camera_rot_y, 0, 1, 0)

        # Foco da Câmera
        if focus_target is not None:
            target_p = planets[focus_target]
            rad_angle = math.radians(target_p["angle"])
            tx = target_p["dist"] * math.cos(rad_angle)
            tz = -target_p["dist"] * math.sin(rad_angle)
            glTranslatef(-tx, 0, -tz)

        glLightfv(GL_LIGHT0, GL_POSITION, [0.0, 0.0, 0.0, 1.0])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.08, 0.08, 0.08, 1.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.8, 1.8, 1.8, 1.0])

        # Skybox
        glPushMatrix()
        glRotate(sim_time * 0.002, 0, 1, 0)
        draw_skybox(tex_stars)
        glPopMatrix()

        # Sol
        glPushMatrix()
        if sun_shader_program:
            glUseProgram(sun_shader_program)
            time_loc = glGetUniformLocation(sun_shader_program, "uTime")
            glUniform1f(time_loc, (sim_time * 0.001) % 1000.0)
            glUniform1i(glGetUniformLocation(sun_shader_program, "tex"), 0)
        else:
            glMaterialfv(GL_FRONT, GL_EMISSION, [1.0, 1.0, 1.0, 1.0])

        glRotate(90, 1, 0, 0)
        draw_body_with_texture(3.5, tex_sol, emission=True)
        glUseProgram(0)
        glPopMatrix()

        # Planetas
        for p in planets:
            draw_orbit(p["dist"])

            glPushMatrix()

            if not is_paused:
                p["angle"] += p["o_speed"] * TIME_SCALE

            glRotate(p["angle"], 0, 1, 0)
            glTranslatef(p["dist"], 0, 0)

            glPushMatrix()
            glRotate(23.5, 0, 0, 1)
            rot_val = (sim_time * 0.1 * p["r_speed"] * TIME_SCALE)
            glRotate(rot_val, 0, 1, 0)
            glRotate(90, 1, 0, 0)
            glColor3f(1, 1, 1)
            draw_body_with_texture(p["rad"], p["tex_id"])
            glPopMatrix()

            if "ring" in p:
                glPushMatrix()
                glRotate(25, 0, 0, 1)
                draw_realistic_ring(p["rad"] * 1.3, p["rad"] * 2.3, p["ring"])
                glPopMatrix()

            if "moon" in p:
                glPushMatrix()
                moon_ang = (sim_time * 0.8 * TIME_SCALE)
                glRotate(moon_ang, 0, 1, 0)
                glTranslatef(p["rad"] + 0.8, 0, 0)
                draw_body_with_texture(0.15, tex_moon)
                glPopMatrix()

            glPopMatrix()

        # Condicional do HUD
        if show_hud:
            f_name = planets[focus_target]["name"] if focus_target is not None else None
            render_hud(f_name, fps, is_paused, font_hud, font_title)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()