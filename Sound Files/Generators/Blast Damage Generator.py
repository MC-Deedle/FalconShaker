import numpy as np
from scipy.io.wavfile import write

# Parameters for the sound wave
sample_rate = 44100  # Samples per second (standard for audio)
duration = 4  # Duration in seconds
bass_frequency = 30  # Bass frequency in Hz (deep bass tone)
amplitude = 32767  # Maximum amplitude for 16-bit PCM
decay_rate = 3.0  # Decay rate for the exponential function

# Time array
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# Generate the bass explosion sound with exponential decay
bass_waveform = amplitude * np.sin(2 * np.pi * bass_frequency * t) * np.exp(-decay_rate * t)

# Normalize the bass waveform to the range of int16
bass_waveform = np.int16(bass_waveform)

# Generate shrapnel bouncing sounds (randomized higher frequencies)
num_shrapnel_sounds = 10  # Number of shrapnel impacts
shrapnel_waveform = np.zeros_like(bass_waveform)

for _ in range(num_shrapnel_sounds):
    # Randomize the shrapnel sound frequency and duration
    shrapnel_freq = np.random.uniform(100, 200)  # High-frequency range for shrapnel
    shrapnel_duration = np.random.uniform(0.01, 0.1)  # Short burst duration
    shrapnel_amplitude = np.random.uniform(0.1, 0.3) * amplitude  # Lower amplitude

    # Time array for this specific shrapnel sound
    t_shrapnel = np.linspace(0, shrapnel_duration, int(sample_rate * shrapnel_duration), endpoint=False)

    # Generate the shrapnel sound
    shrapnel_sound = shrapnel_amplitude * np.sin(2 * np.pi * shrapnel_freq * t_shrapnel)

    # Normalize the shrapnel sound
    shrapnel_sound = np.int16(shrapnel_sound)

    # Randomize the start time of this shrapnel sound within the total duration
    start_index = np.random.randint(0, len(bass_waveform) - len(shrapnel_sound))

    # Add the shrapnel sound to the main waveform
    shrapnel_waveform[start_index:start_index + len(shrapnel_sound)] += shrapnel_sound

# Combine bass and shrapnel waveforms
combined_waveform = bass_waveform + shrapnel_waveform

# Ensure combined waveform is within int16 range
combined_waveform = np.clip(combined_waveform, -amplitude, amplitude)

# Save the sound wave to a .wav file
write('../BlastDamage.wav', sample_rate, combined_waveform)

print("Sound file 'missile_explosion_with_shrapnel.wav' generated and saved.")
