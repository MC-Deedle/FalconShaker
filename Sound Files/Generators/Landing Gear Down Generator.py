import numpy as np
from scipy.io.wavfile import write

# Parameters for the sound
duration = 4  # duration of the sound in seconds
sample_rate = 44100  # samples per second
start_freq = 95  # starting frequency in Hz (A4 note)
end_freq = 85  # ending frequency in Hz (A5 note)
transition_duration = 0.25  # duration of frequency transition in seconds
hold_duration = 2.8  # duration to hold the starting frequency in seconds

# Calculate the number of samples for each segment
n_hold_samples = int(hold_duration * sample_rate)
n_transition_samples = int(transition_duration * sample_rate)
n_end_samples = int(duration * sample_rate) - n_hold_samples - n_transition_samples

# Time arrays for each segment
t_hold = np.linspace(0, hold_duration, n_hold_samples, endpoint=False)
t_transition = np.linspace(0, transition_duration, n_transition_samples, endpoint=False)
t_end = np.linspace(0, duration - hold_duration - transition_duration, n_end_samples, endpoint=False)

# Generate the sine wave segments
hold_wave = np.sin(2 * np.pi * start_freq * t_hold)
transition_wave = np.sin(2 * np.pi * (start_freq + (end_freq - start_freq) * (t_transition / transition_duration)) * t_transition)
end_wave = np.sin(2 * np.pi * end_freq * t_end)

# Concatenate all parts of the wave
full_wave = np.concatenate((hold_wave, transition_wave, end_wave))

# Normalize to 16-bit range and convert to int16
full_wave_int16 = np.int16(full_wave / np.max(np.abs(full_wave)) * 32767)

# Save to file
output_filename = "../gearTransitionDown.wav"
write(output_filename, sample_rate, full_wave_int16)

print(f"Sound file '{output_filename}' has been generated.")
