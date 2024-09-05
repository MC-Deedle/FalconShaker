import numpy as np
from scipy.io.wavfile import write
from scipy.signal import sawtooth

# Parameters for the sound wave
sample_rate = 44100  # Samples per second (standard for audio)
duration = 1.0  # Total duration in seconds
bass_frequency = 30  # Bass frequency in Hz (for deep bass tone of the gun)
amplitude = 32767  # Maximum amplitude for 16-bit PCM
decay_rate = 0  # Decay rate for the exponential function

# Time array for the entire duration
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# Generate the bass sound with a sawtooth wave and exponential decay
bass_waveform = amplitude * sawtooth(2 * np.pi * bass_frequency * t) * np.exp(-decay_rate * t)

# Normalize the bass waveform to the range of int16
bass_waveform = np.int16(bass_waveform)

# Generate varied impact sounds (randomized frequencies between 150 Hz and 170 Hz)
num_impacts = 12  # Number of impacts to simulate
impact_waveform = np.zeros_like(bass_waveform)

for _ in range(num_impacts):
    # Randomize the impact sound frequency and duration
    impact_freq = np.random.uniform(10, 20)  # Frequency range for composite material impact
    impact_duration = np.random.uniform(0.05, 0.2)  # Random short burst duration in seconds
    impact_amplitude = np.random.uniform(0.7, 0.9) * amplitude  # Lower amplitude for variability

    # Time array for this specific impact sound
    t_impact = np.linspace(0, impact_duration, int(sample_rate * impact_duration), endpoint=False)

    # Generate the impact sound with a sawtooth wave
    impact_sound = impact_amplitude * sawtooth(2 * np.pi * impact_freq * t_impact) * np.exp(-decay_rate * t_impact)

    # Normalize the impact sound to int16
    impact_sound = np.int16(impact_sound)

    # Randomize the start time of this impact sound within the total duration
    start_index = np.random.randint(0, len(bass_waveform) - len(impact_sound))

    # Add the impact sound to the main waveform
    impact_waveform[start_index:start_index + len(impact_sound)] += impact_sound

# Combine bass and impact waveforms
combined_waveform = bass_waveform + impact_waveform

# Ensure combined waveform is within int16 range
combined_waveform = np.clip(combined_waveform, -amplitude, amplitude)

# Save the sound wave to a .wav file
write('../ImpactDamage.wav', sample_rate, combined_waveform)

print("Sound file 'ImpactDamage.wav' generated and saved.")
