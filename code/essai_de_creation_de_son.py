import numpy as np
import scipy.io.wavfile as wav
import sounddevice as sd

# Paramètres du son
sampling_rate = 44100  # Fréquence d'échantillonnage (Hz)
duration = 1   # Durée du son en secondes
frequency = 700  # Fréquence de l'onde (en Hz, la note La)

# Générer un tableau de temps
t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)

# Générer l'onde sinusoïdale
sound_wave = np.sin(2 * np.pi * frequency * t)

# Convertir l'onde en entier 16-bit PCM
sound_wave = np.int16(sound_wave * 3000)  # Multiplier par 32767 pour utiliser toute l'échelle des 16-bit

# Sauvegarder le son dans un fichier WAV
wav.write('sine.wav', sampling_rate, sound_wave)


# Jouer le son avec sounddevice
sd.play(sound_wave, samplerate=sampling_rate)

# Attendre que le son se termine avant de continuer
sd.wait()

print("Le son a été joué avec succès.")