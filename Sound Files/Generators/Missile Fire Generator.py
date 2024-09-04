import numpy as np
from scipy.io.wavfile import write

def generate_bump_sound(filename="bump.wav", frequency=15, duration=0.4, sample_rate=44100, volume=1.0):
    """
    Generates a loud bump sound with texture and saves it to a WAV file.

    :param filename: Name of the output WAV file (default is 'bump.wav').
    :param frequency: Frequency of the bump sound in Hz (default is 15 Hz).
    :param duration: Duration of the bump sound in seconds (default is 1.0 seconds).
    :param sample_rate: The sample rate of the audio (default is 44100 Hz).
    :param volume: Volume of the bump sound (0.0 to 1.0).
    """
    # Generate the time array
    t = np.linspace(0, duration, int(sample_rate * duration), False)

    # Generate a low-frequency sine wave
    sine_wave = np.sin(2 * np.pi * frequency * t)

    # Generate some texture by adding low-frequency noise
    noise = np.random.normal(0, 0.1, sine_wave.shape)
    textured_bump = sine_wave

    # Apply a quick fade out to make the bump more abrupt
    fade_out = np.linspace(1, 0, int(sample_rate * duration))
    textured_bump *= fade_out

    # Normalize and apply volume
    textured_bump *= volume / np.max(np.abs(textured_bump))

    # Convert to 16-bit PCM format
    audio = (textured_bump * (2**15 - 1)).astype(np.int16)

    # Save the audio to a WAV file
    write(filename, sample_rate, audio)

# Example usage
generate_bump_sound()
