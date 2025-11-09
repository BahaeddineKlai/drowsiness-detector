import numpy as np
import wave

def generate_beep(frequency=1000, duration=0.5, sample_rate=44100):
    """Génère un bip sonore"""
    t = np.linspace(0, duration, int(sample_rate * duration))
    wave_data = np.sin(2 * np.pi * frequency * t)
    wave_data = (wave_data * 32767).astype(np.int16)
    return wave_data

def create_alert_sound():
    """Crée un fichier audio d'alerte avec des bips répétitifs"""
    sample_rate = 44100
    
    # Créer 3 bips courts
    beep1 = generate_beep(1000, 0.3, sample_rate)
    silence = np.zeros(int(0.2 * sample_rate), dtype=np.int16)
    beep2 = generate_beep(1200, 0.3, sample_rate)
    beep3 = generate_beep(1000, 0.3, sample_rate)
    
    # Assembler les bips
    alert_sound = np.concatenate([beep1, silence, beep2, silence, beep3])
    
    # Sauvegarder en fichier WAV
    with wave.open('alert.wav', 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(alert_sound.tobytes())
    
    print("Fichier audio d'alerte créé: alert.wav")

if __name__ == "__main__":
    create_alert_sound()
