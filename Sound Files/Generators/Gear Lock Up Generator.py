import numpy as np
from scipy.io.wavfile import write

# Parameters for the sound
duration = 0.6  # duration of the entire sound in seconds
sample_rate = 44100  # samples per second
pulse_frequency = 35  # frequency of the sawtooth wave pulse in Hz
pulse_duration = 0.15  # duration of each pulse in seconds
gap_between_pulses = 0.2  # time gap between the pulses in seconds

# Calculate the total number of samples
total_samples = int(sample_rate * duration)

# Generate time array
t = np.linspace(0, duration, total_samples, endpoint=False)

# Generate the sawtooth wave for one pulse
pulse_samples = int(sample_rate * pulse_duration)
pulse_t = np.linspace(0, pulse_duration, pulse_samples, endpoint=False)
saw_wave = 2 * (pulse_frequency * pulse_t % 1) - 1

# Initialize the final wave array with silence (zeros)
final_wave = np.zeros(total_samples)

# Calculate the start indices for the pulses
first_pulse_start = 0
second_pulse_start = int(sample_rate * (pulse_duration + gap_between_pulses))

# Insert the sawtooth pulses into the final wave array
final_wave[first_pulse_start:first_pulse_start + pulse_samples] = saw_wave
final_wave[second_pulse_start:second_pulse_start + pulse_samples] = saw_wave

# Normalize to 16-bit range and convert to int16
final_wave_int16 = np.int16(final_wave / np.max(np.abs(final_wave)) * 32767)

# Save to file
output_filename = "../gearLockUp.wav"
write(output_filename, sample_rate, final_wave_int16)

print(f"Sound file '{output_filename}' has been generated.")
