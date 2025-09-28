# space_invaders.py
# Space Invaders simplificado em Pygame
# Recursos:
# - Tela inicial, jogo e tela de game over
# - Jogador que se move e atira
# - Inimigos em grid que se movem em bloco e descem
# - Colisões (projéteis vs inimigos, inimigo vs jogador)
# - Pontuação, vidas e níveis (velocidade aumenta com progresso)
# - Sons (trilha, tiro, hit, explosão)
# - Comentários explicativos em cada parte

import pygame
import random
import os
import math
import sys

# ========== Configurações ==========
LARGURA, ALTURA = 800, 600
FPS = 60

PLAYER_SPEED = 6
BULLET_SPEED = -10
ENEMY_X_GAP = 60
ENEMY_Y_GAP = 50
ENEMY_MOVE_DELAY = 30  # frames entre passos horizontais (reduz com nível)
ENEMY_ROWS = 4
ENEMY_COLS = 8

ASSET_FOLDER = "sons"

# ========== Inicialização ==========
pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Space Invaders - Higor")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("Consolas", 24)
BIG_FONT = pygame.font.SysFont("Consolas", 48)


# ========== Carregar sons (com fallback silencioso) ==========
def load_sound(path):
    try:
        return pygame.mixer.Sound(path)
    except Exception:
        print(f"Aviso: não foi possível carregar o som {path}. Usando silêncio.")
        return None


def play_sound(snd):
    if snd:
        snd.play()


# tenta carregar sons gerados pelo music_generator.py
TIRO_SND = load_sound(os.path.join(ASSET_FOLDER, "tiro.wav"))
HIT_SND = load_sound(os.path.join(ASSET_FOLDER, "hit.wav"))
EXPLO_SND = load_sound(os.path.join(ASSET_FOLDER, "explosao.wav"))
# trilha como música (mixer.music)
TRILHA_PATH = os.path.join(ASSET_FOLDER, "trilha.wav")
if os.path.exists(TRILHA_PATH):
    try:
        pygame.mixer.music.load(TRILHA_PATH)
    except Exception as e:
        print("Aviso: não foi possível carregar trilha:", e)

# ========== Classes do Jogo ==========


class Player:
    """Classe do jogador (nave)."""
    def __init__(self):
        self.image = pygame.Surface((50, 30), pygame.SRCALPHA)
        # desenha uma nave simples triangular
        pygame.draw.polygon(self.image, (0, 200, 255), [(0, 30), (25, 0), (50, 30)])
        self.rect = self.image.get_rect(midbottom=(LARGURA // 2, ALTURA - 30))
        self.speed = PLAYER_SPEED
        self.lives = 3
        self.cooldown = 0  # frames até poder atirar novamente

    def move(self, dx):
        self.rect.x += dx * self.speed
        # limita aos limites da tela
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > LARGURA:
            self.rect.right = LARGURA

    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    def shoot(self):
        if self.cooldown == 0:
            self.cooldown = 12  # frames de recarga
            play_sound(TIRO_SND)
            return Bullet(self.rect.centerx, self.rect.top, BULLET_SPEED, owner="player")
        return None

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Enemy:
    """Classe para um inimigo individual."""
    def __init__(self, x, y, kind=0):
        self.kind = kind  # tipo influencia cor / pontuação
        w, h = 40, 28
        self.image = pygame.Surface((w, h))
        colors = [(0, 255, 0), (255, 165, 0), (255, 100, 100), (180, 100, 255)]
        self.image.fill(colors[kind % len(colors)])
        self.rect = self.image.get_rect(topleft=(x, y))
        self.alive = True

    def draw(self, surface):
        if self.alive:
            surface.blit(self.image, self.rect)


class Bullet:
    """Projétil (do jogador ou inimigo)."""
    def __init__(self, x, y, speed, owner="player"):
        self.x = x
        self.y = y
        self.speed = speed
        self.owner = owner
        self.rect = pygame.Rect(x-3, y-8, 6, 12)

    def update(self):
        self.y += self.speed
        self.rect.y = self.y

    def draw(self, surface):
        color = (255, 255, 0) if self.owner == "player" else (255, 80, 80)
        pygame.draw.rect(surface, color, self.rect)


# ========== Funções auxiliares ==========
def criar_inimigos(rows=ENEMY_ROWS, cols=ENEMY_COLS):
    """Cria uma grid de inimigos e retorna lista."""
    arr = []
    start_x = 100
    start_y = 60
    for r in range(rows):
        row = []
        for c in range(cols):
            x = start_x + c * ENEMY_X_GAP
            y = start_y + r * ENEMY_Y_GAP
            row.append(Enemy(x, y, kind=r))
        arr.append(row)
    return arr


def desenhar_texto(surface, texto, tamanho, x, y, cor=(255, 255, 255)):
    f = pygame.font.SysFont("Consolas", tamanho)
    surf = f.render(texto, True, cor)
    surface.blit(surf, (x, y))


# ========== Lógica do JOGO ==========]
def jogo():
    # Instâncias
    player = Player()
    enemies = criar_inimigos()
    bullets = []  # projéteis (player + enemies)
    enemy_direction = 1  # 1 = direita, -1 = esquerda
    enemy_timer = 0
    enemy_move_delay = ENEMY_MOVE_DELAY
    score = 0
    level = 1
    frames = 0

    # iniciar trilha
    try:
        pygame.mixer.music.play(-1)
    except:
        pass

    running = True
    while running:
        clock.tick(FPS)
        frames += 1

        # ---------- Eventos ----------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # teclas de controle
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_p:
                    pause()  # pausar o jogo
                if event.key == pygame.K_SPACE:
                    b = player.shoot()
                    if b:
                        bullets.append(b)

        # movimento contínuo do jogador (setas)
        keys = pygame.key.get_pressed()
        dx = 0
        if keys[pygame.K_LEFT]:
            dx = -1
        if keys[pygame.K_RIGHT]:
            dx = 1
        player.move(dx)
        player.update()

        # ---------- Atualizar inimigos (movimento em bloco) ----------
        enemy_timer += 1
        if enemy_timer >= enemy_move_delay:
            enemy_timer = 0
            # descobrir limites da frota para saber se deve descer
            leftmost = min((enemy.rect.left for row in enemies for enemy in row if enemy.alive), default=0)
            rightmost = max((enemy.rect.right for row in enemies for enemy in row if enemy.alive), default=LARGURA)
            hit_edge = (rightmost >= LARGURA - 10 and enemy_direction == 1) or (leftmost <= 10 and enemy_direction == -1)
            if hit_edge:
                # descer
                for row in enemies:
                    for enemy in row:
                        enemy.rect.y += 20
                enemy_direction *= -1
            else:
                # mover horizontalmente
                for row in enemies:
                    for enemy in row:
                        enemy.rect.x += 10 * enemy_direction

        # inimigos atiram aleatoriamente (mais chance quanto menor o número de inimigos)
        if random.random() < 0.01 + (0.002 * (level-1)):
            alive_enemies = [e for row in enemies for e in row if e.alive]
            if alive_enemies:
                shooter = random.choice(alive_enemies)
                bullets.append(Bullet(shooter.rect.centerx, shooter.rect.bottom, abs(BULLET_SPEED) // 2, owner="enemy"))

        # ---------- Atualizar projéteis ----------
        for b in bullets[:]:
            b.update()
            # remove projétil fora da tela
            if b.y < -50 or b.y > ALTURA + 50:
                bullets.remove(b)
                continue

            if b.owner == "player":
                # checar colisão com inimigos
                for row in enemies:
                    for enemy in row:
                        if enemy.alive and enemy.rect.colliderect(b.rect):
                            enemy.alive = False
                            play_sound(HIT_SND)
                            play_sound(EXPLO_SND)
                            try:
                                bullets.remove(b)
                            except ValueError:
                                pass
                            score += 50
            else:
                # projectile do inimigo atinge o jogador?
                if player.rect.colliderect(b.rect):
                    play_sound(EXPLO_SND)
                    bullets.remove(b)
                    player.lives -= 1
                    # respawn temporário ou pequeno recuo; aqui simplificamos
                    if player.lives <= 0:
                        # game over
                        pygame.mixer.music.stop()
                        return score

        # ---------- Verificar se todos inimigos mortos => próximo nível ----------
        all_dead = all(not enemy.alive for row in enemies for enemy in row)
        if all_dead:
            # subir de nível: recriar inimigos, aumentar velocidade
            level += 1
            enemies = criar_inimigos(rows=ENEMY_ROWS + min(2, level-1), cols=ENEMY_COLS)
            # acelera movimento e frequência de tiro
            enemy_move_delay = max(6, ENEMY_MOVE_DELAY - (level-1)*3)
            # bônus de pontuação por completar nivel
            score += 200
            # pequena pausa e som
            play_sound(HIT_SND)

        # ---------- Desenho ----------
        tela.fill((8, 8, 30))  # fundo escuro
        # HUD
        desenhar_texto(tela, f"Pontos: {score}", 20, 10, 10)
        desenhar_texto(tela, f"Vidas: {player.lives}", 20, 10, 40)
        desenhar_texto(tela, f"Nível: {level}", 20, LARGURA - 120, 10)

        # desenhar player
        player.draw(tela)

        # desenhar inimigos
        for row in enemies:
            for enemy in row:
                enemy.draw(tela)

        # desenhar projéteis
        for b in bullets:
            b.draw(tela)

        pygame.display.flip()

    return 0


# ========== Tela inicial / Pause / Game Over ==========
def tela_inicial():
    tela.fill((8, 8, 30))
    title = BIG_FONT.render("SPACE INVADERS", True, (200, 200, 255))
    instr = FONT.render("Pressione ENTER para jogar | E para sair", True, (200, 200, 255))
    tela.blit(title, title.get_rect(center=(LARGURA//2, ALTURA//2 - 40)))
    tela.blit(instr, instr.get_rect(center=(LARGURA//2, ALTURA//2 + 20)))
    pygame.display.flip()
    # esperar decisão do usuário
    waiting = True
    while waiting:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
                elif event.key == pygame.K_e:
                    pygame.quit()
                    sys.exit()


def pause():
    # simples tela de pausa
    paused = True
    pausa_txt = BIG_FONT.render("PAUSED", True, (255, 255, 255))
    tela.blit(pausa_txt, pausa_txt.get_rect(center=(LARGURA//2, ALTURA//2)))
    pygame.display.flip()
    while paused:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
                elif event.key == pygame.K_e:
                    pygame.quit()
                    sys.exit()


def tela_game_over(score):
    tela.fill((8, 8, 30))
    go = BIG_FONT.render("GAME OVER", True, (255, 80, 80))
    s = FONT.render(f"Sua pontuação: {score}", True, (255, 255, 255))
    r = FONT.render("Pressione R para jogar novamente | ESC para sair", True, (200, 200, 200))
    tela.blit(go, go.get_rect(center=(LARGURA//2, ALTURA//2 - 40)))
    tela.blit(s, s.get_rect(center=(LARGURA//2, ALTURA//2 + 10)))
    tela.blit(r, r.get_rect(center=(LARGURA//2, ALTURA//2 + 60)))
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    return True
                elif event.key == pygame.K_e:
                    pygame.quit()
                    sys.exit()
    return False


# ========== Utilitários ==========
def desenhar_texto(superficie, texto, tam, x, y):
    font = pygame.font.SysFont("Consolas", tam)
    surf = font.render(texto, True, (255, 255, 255))
    superficie.blit(surf, (x,y))


# ========== Loop principal ==========
if __name__ == "__main__":
    # mostra tela inicial
    while True:
        tela_inicial()
        # play trilha se disponível
        if os.path.exists(TRILHA_PATH):
            try:
                pygame.mixer.music.play(-1)
            except:
                pass
        pontos = jogo()
        pygame.mixer.music.stop()
        reiniciar = tela_game_over(pontos)
        if not reiniciar:
            break
