# 🚀 Space Invaders - Higor

Uma versão simples e personalizável do clássico *Space Invaders* feita em **Python** com **Pygame**.  
Desenvolvido para aprendizado: movimentação do jogador, inimigos em formação, tiros, colisões, níveis, HUD, sons e trilha.

---

## 🎯 Visão geral
- Jogador controla uma nave na parte inferior e atira nos invasores.
- Inimigos se movem em bloco e descem conforme avançam.
- Existe pontuação, níveis, vidas e sons (tiro, hit, explosão, trilha).
- Feito com código simples para ser fácil de entender e estender.

---

## 🧩 Funcionalidades
- Tela inicial, pausa e tela de Game Over.
- Jogador com limite de vidas e cooldown de tiro.
- Inimigos em grid com movimento em bloco e descida ao atingir a borda.
- Inimigos atiram aleatoriamente (mais frequência conforme o nível).
- Colisões entre projéteis/inimigos e projéteis/jogador.
- Pontuação, HUD (pontuação / vidas / nível).
- Sons: tiro, hit, explosão e trilha de fundo (gerados por script Python opcional).
- Código comentado para facilitar aprendizado.

---

## 📁 Estrutura do projeto
```text
space_invaders/
├── space_invaders.py        # Jogo principal (Pygame)
├── music_generator.py       # (Opcional) gera sons em ./sons/
├── sons/                    # Pasta de sons (criada pelo script)
│   ├── tiro.wav
│   ├── hit.wav
│   ├── explosao.wav
│   └── trilha.wav
└── README.md

▶️ Como executar (passo a passo)

Pré-requisitos

Python 3.8+ (recomendado 3.10+)

Instale dependências:

pip install pygame numpy


Gerar os sons (opcional, mas recomendado)

Rode o script que cria sons retro (gera sons/):

python music_generator.py


Isso gera tiro.wav, hit.wav, explosao.wav e trilha.wav. Se já tiver seus próprios sons, coloque-os em sons/.

Rodar o jogo

python space_invaders.py

⌨️ Controles

← / → : mover a nave à esquerda/direita

Espaço : atirar

P : pausar / despausar

ENTER (na tela inicial) : começar

R (na tela de Game Over) : reiniciar

ESC / E : sair do jogo

🔊 Problemas comuns com áudio

Se ocorrer erro ao carregar a trilha (pygame.error para OGG), gere trilha.wav com o music_generator.py (ele cria WAV compatíveis).

Se um efeito não tocar, verifique se:

O arquivo existe em sons/ com o nome correto.

pygame.mixer está inicializado (o script faz pygame.init() por padrão).

Em alguns sistemas, pygame precisa do SDL/FFmpeg com suporte a certos codecs; usar WAV evita a maioria dos problemas.
