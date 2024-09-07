import numpy as np
import scipy.io.wavfile as wav

# Parameters
sample_rate = 44100  # CD-quality sample rate
duration = 10*9.5  # Total duration of the sound in seconds
freq1 = 10  # Frequency of the first sine wave (Hz)
freq2 = 9.5  # Frequency of the second sine wave (Hz)

# Time vector
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# Generate the two sine waves
sine_wave1 = np.sin(2 * np.pi * freq1 * t)  # 15 Hz sine wave
sine_wave2 = np.sin(2 * np.pi * freq2 * t)  # 20 Hz sine wave

# Combine the two waves
combined_wave = sine_wave1 + sine_wave2

# Normalize the signal to avoid clipping
combined_wave = combined_wave / np.max(np.abs(combined_wave))

# Convert to 16-bit PCM format
sound_data = np.int16(combined_wave * 32767)

# Save the sound file as 'stall.wav'
output_file = 'stall.wav'
wav.write(output_file, sample_rate, sound_data)

print(f"Sound file '{output_file}' generated successfully.")
