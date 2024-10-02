import numpy as np
import wave
import struct

# Function to generate the waveform of a pulse sound
def generate_pulse(sample_rate, duration, frequency, volume):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    pulse_wave = volume * np.sin(2 * np.pi * frequency * t)
    return pulse_wave

# Parameters
sample_rate = 44100  # CD quality
pulse_duration = 0.1  # Each pulse lasts 0.1 seconds
pulse_frequency = 15  # Frequency for the pulse sound
interval = 0.2       # Time between pulses in seconds
total_duration = 2 # Total duration of the audio
volume = 32767       # Max volume for 16-bit audio

# Generate the first pulse
pulse1 = generate_pulse(sample_rate, pulse_duration, pulse_frequency, volume)

# Generate silence for the interval
silence_duration = interval - pulse_duration
silence = np.zeros(int(sample_rate * silence_duration))

# Generate the second pulse
pulse2 = generate_pulse(sample_rate, pulse_duration, pulse_frequency, volume)

# Create silence for the rest of the audio
remaining_silence_duration = total_duration - (pulse_duration + silence_duration + pulse_duration)
remaining_silence = np.zeros(int(sample_rate * remaining_silence_duration))

# Concatenate the pulses and silence
full_wave = np.concatenate([pulse1, silence, pulse2, remaining_silence])

# Ensure the data is in the correct format for 16-bit PCM WAV file
full_wave = np.int16(full_wave)

# Write the result to a WAV file
file_name = "../eject.wav"
with wave.open(file_name, 'w') as wav_file:
    wav_file.setnchannels(1)  # Mono
    wav_file.setsampwidth(2)  # 2 bytes per sample
    wav_file.setframerate(sample_rate)
    wav_file.writeframes(struct.pack('<' + ('h' * len(full_wave)), *full_wave))

print(f"Audio file '{file_name}' has been generated.")
