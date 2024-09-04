import numpy as np
from scipy.io.wavfile import write

def generate_funny_error_tone(filename="nope.wav", sample_rate=44100):
    """
    Generates a funny error tone and saves it to a WAV file.

    :param filename: Name of the output WAV file (default is 'nope.wav').
    :param sample_rate: The sample rate of the audio (default is 44100 Hz).
    """
    # Define the tone parameters
    duration = 0.5  # 0.5 seconds per tone
    frequencies = [300, 450, 150]  # A funny sequence of frequencies
    volume = 0.8  # Volume (0.0 to 1.0)

    # Generate the tone sequence
    audio = np.array([], dtype=np.float32)
    for freq in frequencies:
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        tone = np.sin(freq * 2 * np.pi * t) * volume
        audio = np.concatenate((audio, tone))

    # Ensure that the tone is within the range of -1.0 to 1.0
    audio = np.clip(audio, -1.0, 1.0)

    # Convert to 16-bit data
    audio = (audio * (2**15 - 1)).astype(np.int16)

    # Save the audio to a WAV file
    write(filename, sample_rate, audio)

# Example usage
generate_funny_error_tone()
