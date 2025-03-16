import numpy as np

def sine_wave(frequency: float, duration: float, sample_rate: float) -> np.ndarray:
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    return np.sin(2 * np.pi * frequency * t)

def square_wave(frequency: float, duration: float, sample_rate: float) -> np.ndarray:
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    return np.sign(np.sin(2 * np.pi * frequency * t))

def chirp(start_freq: float, end_freq: float, duration: float, sample_rate: float) -> np.ndarray:
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    k = (end_freq - start_freq) / duration
    return np.sin(2 * np.pi * (start_freq * t + 0.5 * k * t ** 2))

def random_binary_sequence(length: int) -> np.ndarray:
    return np.random.randint(0, 2, length)

def text_to_binary(text: str) -> np.ndarray:
    binary_str = ''.join(format(ord(char), '08b') for char in text)
    return np.array([int(bit) for bit in binary_str])