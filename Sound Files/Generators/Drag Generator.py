import numpy as np
import scipy.io.wavfile as wavfile
from math import gcd


def lcm(x, y, z):
    """Calculates the least common multiple of two numbers."""
    return abs(x * y * z) // gcd(x, y, z)


def generate_sine_wave(freq, duration, sample_rate=44100):
    """Generates a sine wave of a given frequency and duration."""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = 0.5 * np.sin(2 * np.pi * freq * t)
    return wave


def create_concurrent_sound_file(frequency1, frequency2, frequency3, output_file='AirBakeDrag.wav'):
    """Generates a sound file with two sine waves playing concurrently."""
    sample_rate = 44100  # CD quality audio

    # Calculate the least common multiple of the periods (1/frequency)
    period1 = 1 / frequency1
    period2 = 1 / frequency2
    period3 = 1 / frequency3
    lcm_period = lcm(int(period1 * 1000), int(period2 * 1000), int(period3 * 1000)) / 1000  # Find LCM in seconds

    # Set the duration to be a multiple of both periods (at least 10 seconds)
    duration = lcm_period

    # Generate the two sine waves
    wave1 = generate_sine_wave(frequency1, duration, sample_rate)
    wave2 = generate_sine_wave(frequency2, duration, sample_rate)
    wave3 = generate_sine_wave(frequency3, duration, sample_rate)
    # Combine the two sine waves by adding them together
    combined_wave = wave1 + wave2 + wave3

    # Normalize the combined wave to the 16-bit range
    combined_wave = np.int16(combined_wave / np.max(np.abs(combined_wave)) * 32767)


# Write the combined wave to a WAV file
    wavfile.write("../AirBrakeDrag.wav", sample_rate, combined_wave)
    print(f"Sound file {output_file} generated successfully!")

# Example of usage
frequency1 = 35
frequency2 = 29
frequency3 = 40
create_concurrent_sound_file(frequency1, frequency2, frequency3)
