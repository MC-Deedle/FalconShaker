import numpy as np
import wave
import struct

# Function to generate a sawtooth wave
def generate_sawtooth(sample_rate, frequency, duration, amplitude):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    sawtooth_wave = amplitude * (2 * (t * frequency - np.floor(1/2 + t * frequency)))
    return sawtooth_wave

# Parameters
sample_rate = 44100  # Sample rate in Hz
frequency = 100       # Frequency of the sawtooth wave in Hz
duration = 5.0       # Duration in seconds
amplitude = 32767     # Max amplitude for 16-bit audio

# Generate the sawtooth wave
sawtooth_wave = generate_sawtooth(sample_rate, frequency, duration, amplitude)

# Ensure the data is in the correct format for a 16-bit PCM WAV file
sawtooth_wave = np.int16(sawtooth_wave)

# Write the result to a WAV file
file_name = "../Cannon100hz.wav"
with wave.open(file_name, 'w') as wav_file:
    wav_file.setnchannels(1)  # Mono
    wav_file.setsampwidth(2)  # 2 bytes per sample
    wav_file.setframerate(sample_rate)
    wav_file.writeframes(struct.pack('<' + ('h' * len(sawtooth_wave)), *sawtooth_wave))

print(f"Audio file '{file_name}' has been generated.")
