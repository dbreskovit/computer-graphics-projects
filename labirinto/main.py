import pygame
import pygame.freetype
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import time
from config import *

vidas = VIDAS_INICIAIS
fase = FASE_INICIAL
jogador_tem_chave = False
jogo_ativo = True
mensagem_vitoria = ""
tempo_mensagem = 0

pygame.freetype.init()
custom_font = pygame.freetype.Font("assets/Minecraft.ttf", 24)

def desenhar_retangulo(x, y, largura, altura, cor):
    glColor3fv(cor)
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + largura, y)
    glVertex2f(x + largura, y + altura)
    glVertex2f(x, y + altura)
    glEnd()

def renderizar_texto(texto, cor=(255, 255, 255)):
    surface, _ = custom_font.render(texto, cor)
    text_data = pygame.image.tostring(surface, "RGBA", True)
    width, height = surface.get_size()

    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)

    return tex_id, width, height

def desenhar_texto(texto, x, y, cor=(255, 255, 255)):
    tex_id, width, height = renderizar_texto(texto, cor)

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, tex_id)

    glColor3f(1, 1, 1)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 1); glVertex2f(x, y)
    glTexCoord2f(1, 1); glVertex2f(x + width, y)
    glTexCoord2f(1, 0); glVertex2f(x + width, y + height)
    glTexCoord2f(0, 0); glVertex2f(x, y + height)
    glEnd()

    glDeleteTextures([tex_id])
    glDisable(GL_TEXTURE_2D)

def desenhar_texto_centralizado(texto, center_x, center_y, cor=(255, 255, 255)):
    tex_id, width, height = renderizar_texto(texto, cor)
    x = center_x - width // 2
    y = center_y - height // 2
    desenhar_texto(texto, x, y, cor)

def desenhar_labirinto(labirinto):
    for i, linha in enumerate(labirinto):
        for j, celula in enumerate(linha):
            cor = COR_PAREDE if celula == 1 else COR_CAMINHO
            desenhar_retangulo(j * TAMANHO_CELULA, i * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA, cor)

def gerar_labirinto_base(n):
    labirinto = [[1 for _ in range(n)] for _ in range(n)]
    pilha = [(1, 1)]
    labirinto[1][1] = 0

    while pilha:
        x, y = pilha[-1]
        vizinhos = []
        for dx, dy in [(0, 2), (0, -2), (2, 0), (-2, 0)]:
            nx, ny = x + dx, y + dy
            if 0 < nx < n - 1 and 0 < ny < n - 1 and labirinto[ny][nx] == 1:
                vizinhos.append((nx, ny))

        if vizinhos:
            nx, ny = random.choice(vizinhos)
            labirinto[ny][nx] = 0
            labirinto[(y + ny) // 2][(x + nx) // 2] = 0
            pilha.append((nx, ny))
        else:
            pilha.pop()
    return labirinto

def adicionar_ramificacoes(labirinto):
    n = len(labirinto)
    for i in range(1, n - 1):
        for j in range(1, n - 1):
            if labirinto[i][j] == 1:
                if random.random() < PORCENTAGEM_REMOCAO_PAREDES:
                    labirinto[i][j] = 0

class Entidade:
    def __init__(self, x, y, cor):
        self.x = x
        self.y = y
        self.cor = cor

    def desenhar(self):
        desenhar_retangulo(self.x * TAMANHO_CELULA, self.y * TAMANHO_CELULA,
                           TAMANHO_CELULA, TAMANHO_CELULA, self.cor)

    def mover(self, dx, dy, labirinto):
        novo_x = self.x + dx
        novo_y = self.y + dy

        if 0 <= novo_y < len(labirinto) and 0 <= novo_x < len(labirinto[0]):
            if labirinto[int(novo_y)][int(novo_x)] == 0:
                self.x = novo_x
                self.y = novo_y
                return True
        return False

class Jogador(Entidade):
    def __init__(self, x, y):
        super().__init__(x, y, COR_JOGADOR)

class Inimigo(Entidade):
    def __init__(self, x, y):
        super().__init__(x, y, COR_INIMIGO)
        self.direcao = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])

    def mover_aleatoriamente(self, labirinto):
        dx, dy = self.direcao
        if not self.mover(dx, dy, labirinto) or random.random() < 0.1:
            self.direcao = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])

def obter_posicao_valida(labirinto, posicoes_ocupadas):
    while True:
        x = random.randint(1, N - 2)
        y = random.randint(1, N - 2)
        if labirinto[y][x] == 0 and (x, y) not in posicoes_ocupadas:
            return x, y

def reiniciar_nivel(labirinto_atual):
    global jogador, inimigos, chave, destino, jogador_tem_chave

    posicoes_ocupadas = set()

    px, py = obter_posicao_valida(labirinto_atual, posicoes_ocupadas)
    posicoes_ocupadas.add((px, py))
    jogador = Jogador(px, py)

    cx, cy = obter_posicao_valida(labirinto_atual, posicoes_ocupadas)
    posicoes_ocupadas.add((cx, cy))
    chave = (cx, cy)

    dx, dy = obter_posicao_valida(labirinto_atual, posicoes_ocupadas)
    posicoes_ocupadas.add((dx, dy))
    destino = (dx, dy)

    inimigos = []
    for _ in range(NUM_INIMIGOS):
        ix, iy = obter_posicao_valida(labirinto_atual, posicoes_ocupadas)
        posicoes_ocupadas.add((ix, iy))
        inimigos.append(Inimigo(ix, iy))

    jogador_tem_chave = False

def novo_jogo():
    global fase
    fase += 1
    labirinto = gerar_labirinto_base(N)
    adicionar_ramificacoes(labirinto)
    reiniciar_nivel(labirinto)
    return labirinto

def main():
    global vidas, jogador_tem_chave, fase, mensagem_vitoria, tempo_mensagem, jogo_ativo

    pygame.init()
    pygame.mixer.init()
    pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Labirinto Neon")

    try:
        som_chave = pygame.mixer.Sound('assets/key_sound.wav')
        som_vitoria = pygame.mixer.Sound('assets/win_sound.wav')
        som_derrota = pygame.mixer.Sound('assets/lose_sound.wav')
    except pygame.error as e:
        print(f"Aviso: Não foi possível carregar os arquivos de som: {e}")
        som_chave = som_vitoria = som_derrota = type('DummySound', (), {'play': lambda: None})()

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, LARGURA_TELA, ALTURA_TELA, 0)
    glMatrixMode(GL_MODELVIEW)

    labirinto = gerar_labirinto_base(N)
    adicionar_ramificacoes(labirinto)
    reiniciar_nivel(labirinto)

    while jogo_ativo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jogo_ativo = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    jogador.mover(-1, 0, labirinto)
                elif event.key == pygame.K_RIGHT:
                    jogador.mover(1, 0, labirinto)
                elif event.key == pygame.K_UP:
                    jogador.mover(0, -1, labirinto)
                elif event.key == pygame.K_DOWN:
                    jogador.mover(0, 1, labirinto)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        desenhar_labirinto(labirinto)

        if not jogador_tem_chave:
            desenhar_retangulo(chave[0] * TAMANHO_CELULA, chave[1] * TAMANHO_CELULA,
                               TAMANHO_CELULA, TAMANHO_CELULA, COR_CHAVE)

        cor_destino = COR_DESTINO_COM_CHAVE if jogador_tem_chave else COR_DESTINO_SEM_CHAVE
        desenhar_retangulo(destino[0] * TAMANHO_CELULA, destino[1] * TAMANHO_CELULA,
                           TAMANHO_CELULA, TAMANHO_CELULA, cor_destino)

        jogador.desenhar()
        for inimigo in inimigos:
            inimigo.mover_aleatoriamente(labirinto)
            inimigo.desenhar()

        desenhar_texto(f"Vidas: {vidas}", 10, 25, (255, 255, 255))
        desenhar_texto(f"Fase: {fase}", 150, 25, (255, 255, 255))

        if not jogador_tem_chave and (jogador.x, jogador.y) == chave:
            jogador_tem_chave = True
            som_chave.play()

        for inimigo in inimigos:
            if (jogador.x, jogador.y) == (inimigo.x, inimigo.y):
                vidas -= 1
                som_derrota.play()
                if vidas > 0:
                    reiniciar_nivel(labirinto)
                else:
                    desenhar_texto_centralizado("FIM DE JOGO", LARGURA_TELA / 2, ALTURA_TELA / 2)
                    pygame.display.flip()
                    time.sleep(3)
                    jogo_ativo = False

        if jogador_tem_chave and (jogador.x, jogador.y) == destino:
            som_vitoria.play()
            mensagem_vitoria = f"Fase {fase} Completa!"
            tempo_mensagem = time.time()
            labirinto = novo_jogo()

        if mensagem_vitoria and time.time() - tempo_mensagem < 2:
            desenhar_texto_centralizado(mensagem_vitoria, LARGURA_TELA / 2, ALTURA_TELA / 2)
        else:
            mensagem_vitoria = ""

        pygame.display.flip()
        pygame.time.wait(100)

    pygame.quit()


if __name__ == "__main__":
    main()