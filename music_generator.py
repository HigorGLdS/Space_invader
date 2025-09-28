# music_generator.py
# Gera arquivos WAV simples (retrô) para usar em Space Invaders:
# - trilha.wav (loop simples)
# - tiro.wav (efeito de tiro curto)
# - explosao.wav (burst de ruído)
# - hit.wav (blip curto)

import os
import wave
import numpy as np


os.makedirs("sons", exist_ok=True)

SAMPLERATE = 44100


def salvar_wav(nome, audio, samplerate=SAMPLERATE):
    """Salva um array numpy int16 em um arquivo WAV."""
    with wave.open(nome, "w") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(samplerate)
        f.writeframes(audio.tobytes())
    print(f"Gerado: {nome}")


def seno(freq, dur, vol=0.5):
    t = np.linspace(0, dur, int(SAMPLERATE * dur), False)
    onda = np.sin(2 * np.pi * freq * t) * vol
    return (onda * 32767).astype(np.int16)


def quadrada(freq, dur, vol=0.5):
    t = np.linspace(0, dur, int(SAMPLERATE * dur), False)
    onda = np.sign(np.sin(2 * np.pi * freq * t)) * vol
    return (onda * 32767).astype(np.int16)


def ruido(dur, vol=0.5):
    n = int(SAMPLERATE * dur)
    onda = np.random.normal(0, 1, n) * vol
    onda = np.clip(onda, -1, 1)
    return (onda * 32767).astype(np.int16)


# 1) tiro.wav - efeito curto (quadrado descendente de pitch)
def gerar_tiro():
    partes = []
    freqs = [1200, 900, 700]
    for f in freqs:
        partes.append(quadrada(f, 0.03, vol=0.5))
    audio = np.concatenate(partes)
    salvar_wav("sons/tiro.wav", audio)


# 2) hit.wav - blip curto (seno)
def gerar_hit():
    audio = seno(1000, 0.08, vol=0.6)
    salvar_wav("sons/hit.wav", audio)


# 3) explosao.wav - burst de ruído com decay
def gerar_explosao():
    n = int(SAMPLERATE * 0.5)
    base = np.random.normal(0, 1, n)
    # aplicar envelope decay
    env = np.linspace(1, 0, n)
    onda = base * env * 0.9
    audio = np.int16(np.clip(onda, -1, 1) * 32767)
    salvar_wav("sons/explosao.wav", audio)


# 4) trilha.wav - loop simples (sequência de tones 8-bit-like)
def gerar_trilha():
    notas = [440, 550, 660, 880, 660, 550, 440, 330]  # sequência simples
    partes = []
    for n in notas:
        partes.append(quadrada(n, 0.2, vol=0.18))
        # repetir a sequência algumas vezes para criar ~ aúdio maior
        audio = np.tile(np.concatenate(partes), 8)
        salvar_wav("sons/trilha.wav", audio)


if __name__ == "__main__":
    gerar_tiro()
    gerar_hit()
    gerar_explosao()
    gerar_trilha()
    print("Todos os sons foram gerados em ./sons")
