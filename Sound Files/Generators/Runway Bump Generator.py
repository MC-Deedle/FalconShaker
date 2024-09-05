import numpy as np
from scipy.io import wavfile

# Parameters for the sine wave
frequency = 4        # Frequency in Hertz
duration = 0.5       # Duration in seconds
sampling_rate = 44100  # Samples per second (standard for high-quality audio)

# Generate the time values for the sine wave
t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)

# Generate the sine wave
amplitude = 1  # Amplitude of the sine wave (0.5 for half the max volume)
sine_wave = amplitude * np.sin(2 * np.pi * frequency * t)

# Convert the sine wave to 16-bit PCM format
sine_wave_pcm = np.int16(sine_wave * 32767)

# Save the sine wave as a WAV file
wavfile.write("../RunwayBump.wav", sampling_rate, sine_wave_pcm)

print("Half-second 4 Hz sine wave saved as 4Hz_Sine_Wave.wav")
