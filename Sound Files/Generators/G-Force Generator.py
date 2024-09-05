import numpy as np
import scipy.io.wavfile as wav

# Parameters
sample_rate = 44100  # CD-quality sample rate
duration = 10  # Total duration of the sound in seconds
freq_start = 27  # Frequency for the first and last quarters (Hz)
freq_mid = 25  # Frequency for the middle two quarters (Hz)
fade_duration = 2  # Duration of frequency fade in seconds

# Time vector for the entire duration
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# Time vectors for different segments
quarter_duration = duration / 4
fade_samples = int(sample_rate * fade_duration)

# Generate frequency modulation
def generate_fade_window(fade_duration, sample_rate):
    fade_samples = int(sample_rate * fade_duration)
    fade_in = np.linspace(0, 1, fade_samples)
    fade_out = np.linspace(1, 0, fade_samples)
    return fade_in, fade_out

fade_in, fade_out = generate_fade_window(fade_duration, sample_rate)

# Generate the waveform
wave = np.zeros_like(t)

# First quarter: 30 Hz
end_first_quarter = int(sample_rate * quarter_duration)
wave[:end_first_quarter] = np.sin(2 * np.pi * freq_start * t[:end_first_quarter])

# Transition to 25 Hz: Fade out 30 Hz and fade in 25 Hz
fade_end = end_first_quarter + fade_samples
wave[end_first_quarter:fade_end] = (
    np.sin(2 * np.pi * freq_start * t[end_first_quarter:fade_end]) * fade_out +
    np.sin(2 * np.pi * freq_mid * t[end_first_quarter:fade_end]) * fade_in
)

# Middle two quarters: 25 Hz
end_mid = int(sample_rate * (3 * quarter_duration))
wave[fade_end:end_mid] = np.sin(2 * np.pi * freq_mid * t[fade_end:end_mid])

# Transition back to 30 Hz: Fade out 25 Hz and fade in 30 Hz
fade_end = end_mid + fade_samples
wave[end_mid:fade_end] = (
    np.sin(2 * np.pi * freq_mid * t[end_mid:fade_end]) * fade_out +
    np.sin(2 * np.pi * freq_start * t[end_mid:fade_end]) * fade_in
)

# Final quarter: 30 Hz
wave[fade_end:] = np.sin(2 * np.pi * freq_start * t[fade_end:])

# Normalize the signal to avoid clipping
wave = wave / np.max(np.abs(wave))

# Convert to 16-bit PCM format
sound_data = np.int16(wave * 32767)

# Save the sound file as gForce.wav
output_file = '../gForce.wav'
wav.write(output_file, sample_rate, sound_data)

print(f"Sound file '{output_file}' generated successfully as 'gForce.wav'.")
