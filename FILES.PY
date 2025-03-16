import os
import sys
from pathlib import Path
import traceback

# Define the base directory
base_dir = Path("comm_engineering")

# Define the structure and content of each file
structure = {
    base_dir: {
        "__init__.py": """from .signals import sine_wave, square_wave, chirp, random_binary_sequence, text_to_binary
from .modulation import bpsk_modulate, bpsk_demodulate, qpsk_modulate, qpsk_demodulate
from .channels import awgn
from .error_correction import hamming_encode, hamming_decode
from .visualization import plot_time_domain, plot_frequency_domain, plot_constellation
from .metrics import calculate_ber
from .simulation import CommunicationSystem

__all__ = [
    'sine_wave', 'square_wave', 'chirp', 'random_binary_sequence', 'text_to_binary',
    'bpsk_modulate', 'bpsk_demodulate', 'qpsk_modulate', 'qpsk_demodulate',
    'awgn', 'hamming_encode', 'hamming_decode',
    'plot_time_domain', 'plot_frequency_domain', 'plot_constellation',
    'calculate_ber', 'CommunicationSystem'
]
""",
        "signals.py": """import numpy as np

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
""",
        "modulation.py": """import numpy as np

def bpsk_modulate(binary_sequence: np.ndarray, carrier_freq: float, sample_rate: float, bit_duration: float) -> np.ndarray:
    t = np.arange(0, len(binary_sequence) * bit_duration, 1 / sample_rate)
    carrier = np.sin(2 * np.pi * carrier_freq * t)
    modulated = np.zeros_like(t)
    for i, bit in enumerate(binary_sequence):
        start = int(i * bit_duration * sample_rate)
        end = int((i + 1) * bit_duration * sample_rate)
        modulated[start:end] = carrier[start:end] if bit == 1 else -carrier[start:end]
    return modulated

def bpsk_demodulate(received_signal: np.ndarray, carrier_freq: float, sample_rate: float, bit_duration: float) -> np.ndarray:
    num_bits = int(len(received_signal) / (sample_rate * bit_duration))
    demodulated = np.zeros(num_bits, dtype=int)
    t = np.arange(0, bit_duration, 1 / sample_rate)
    carrier = np.sin(2 * np.pi * carrier_freq * t)
    for i in range(num_bits):
        start = int(i * bit_duration * sample_rate)
        end = int((i + 1) * bit_duration * sample_rate)
        correlation = np.sum(received_signal[start:end] * carrier[:end - start])
        demodulated[i] = 1 if correlation > 0 else 0
    return demodulated

def qpsk_modulate(binary_sequence: np.ndarray, carrier_freq: float, sample_rate: float, bit_duration: float) -> np.ndarray:
    if len(binary_sequence) % 2 != 0:
        raise ValueError("Binary sequence length must be even for QPSK.")
    symbols = [(binary_sequence[i], binary_sequence[i + 1]) for i in range(0, len(binary_sequence), 2)]
    t = np.arange(0, len(symbols) * bit_duration, 1 / sample_rate)
    carrier_i = np.sin(2 * np.pi * carrier_freq * t)
    carrier_q = np.cos(2 * np.pi * carrier_freq * t)
    modulated = np.zeros_like(t, dtype=float)
    for i, (b1, b2) in enumerate(symbols):
        start = int(i * bit_duration * sample_rate)
        end = int((i + 1) * bit_duration * sample_rate)
        phase = {(0, 0): np.pi / 4, (0, 1): 3 * np.pi / 4, (1, 0): -np.pi / 4, (1, 1): -3 * np.pi / 4}
        theta = phase[(b1, b2)]
        modulated[start:end] = carrier_i[start:end] * np.cos(theta) + carrier_q[start:end] * np.sin(theta)
    return modulated

def qpsk_demodulate(received_signal: np.ndarray, carrier_freq: float, sample_rate: float, bit_duration: float) -> np.ndarray:
    num_symbols = int(len(received_signal) / (sample_rate * bit_duration))
    demodulated = np.zeros(num_symbols * 2, dtype=int)
    t = np.arange(0, bit_duration, 1 / sample_rate)
    carrier_i = np.sin(2 * np.pi * carrier_freq * t)
    carrier_q = np.cos(2 * np.pi * carrier_freq * t)
    for i in range(num_symbols):
        start = int(i * bit_duration * sample_rate)
        end = int((i + 1) * bit_duration * sample_rate)
        i_component = np.sum(received_signal[start:end] * carrier_i[:end - start])
        q_component = np.sum(received_signal[start:end] * carrier_q[:end - start])
        b1 = 1 if i_component < 0 else 0
        b2 = 1 if q_component < 0 else 0
        demodulated[2 * i] = b1
        demodulated[2 * i + 1] = b2
    return demodulated
""",
        "channels.py": """import numpy as np

def awgn(signal: np.ndarray, snr_db: float) -> np.ndarray:
    if np.iscomplexobj(signal):
        noise_real = np.random.normal(0, 1, signal.shape)
        noise_imag = np.random.normal(0, 1, signal.shape)
        noise = noise_real + 1j * noise_imag
        signal_power = np.mean(np.abs(signal) ** 2)
        noise_power = signal_power / (10 ** (snr_db / 10))
        noise *= np.sqrt(noise_power / 2)
    else:
        noise = np.random.normal(0, 1, signal.shape)
        signal_power = np.mean(signal ** 2)
        noise_power = signal_power / (10 ** (snr_db / 10))
        noise *= np.sqrt(noise_power)
    return signal + noise
""",
        "error_correction.py": """import numpy as np

def hamming_encode(data: np.ndarray) -> np.ndarray:
    if len(data) % 4 != 0:
        raise ValueError("Data length must be a multiple of 4.")
    G = np.array([[1, 0, 0, 0, 1, 1, 0],
                  [0, 1, 0, 0, 1, 0, 1],
                  [0, 0, 1, 0, 0, 1, 1],
                  [0, 0, 0, 1, 1, 1, 1]], dtype=int)
    encoded = []
    for i in range(0, len(data), 4):
        block = data[i:i + 4]
        encoded_block = (block @ G) % 2
        encoded.extend(encoded_block)
    return np.array(encoded)

def hamming_decode(received: np.ndarray) -> np.ndarray:
    if len(received) % 7 != 0:
        raise ValueError("Received data length must be a multiple of 7.")
    H = np.array([[1, 0, 1, 0, 1, 0, 1],
                  [0, 1, 1, 0, 0, 1, 1],
                  [0, 0, 0, 1, 1, 1, 1]], dtype=int)
    decoded = []
    for i in range(0, len(received), 7):
        block = received[i:i + 7]
        syndrome = (H @ block) % 2
        error_pos = int(''.join(map(str, syndrome)), 2)
        if error_pos != 0:
            block[error_pos - 1] ^= 1
        decoded.extend(block[:4])
    return np.array(decoded)
""",
        "visualization.py": """import numpy as np
import matplotlib.pyplot as plt

def plot_time_domain(signal: np.ndarray, sample_rate: float, title: str = 'Time Domain Signal') -> None:
    t = np.arange(len(signal)) / sample_rate
    plt.plot(t, signal)
    plt.title(title)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.show()

def plot_frequency_domain(signal: np.ndarray, sample_rate: float, title: str = 'Frequency Domain Signal') -> None:
    freq = np.fft.fftfreq(len(signal), 1 / sample_rate)
    spectrum = np.fft.fft(signal)
    plt.plot(freq, np.abs(spectrum))
    plt.title(title)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.grid(True)
    plt.show()

def plot_constellation(signal: np.ndarray, title: str = 'Constellation Diagram') -> None:
    plt.scatter(np.real(signal), np.imag(signal))
    plt.title(title)
    plt.xlabel('In-phase')
    plt.ylabel('Quadrature')
    plt.grid(True)
    plt.show()
""",
        "metrics.py": """import numpy as np

def calculate_ber(original: np.ndarray, received: np.ndarray) -> float:
    if len(original) != len(received):
        raise ValueError("Original and received sequences must have the same length.")
    errors = np.sum(original != received)
    return errors / len(original)
""",
        "simulation.py": """import numpy as np
from .signals import random_binary_sequence
from .modulation import bpsk_modulate, bpsk_demodulate, qpsk_modulate, qpsk_demodulate
from .channels import awgn
from .error_correction import hamming_encode, hamming_decode
from .metrics import calculate_ber

class CommunicationSystem:
    def __init__(self, modulation_type: str, snr_db: float, carrier_freq: float,
                 sample_rate: float, bit_duration: float, use_error_correction: bool = False):
        if modulation_type not in ['bpsk', 'qpsk']:
            raise ValueError("Modulation type must be 'bpsk' or 'qpsk'.")
        self.modulation_type = modulation_type
        self.snr_db = snr_db
        self.carrier_freq = carrier_freq
        self.sample_rate = sample_rate
        self.bit_duration = bit_duration
        self.use_error_correction = use_error_correction

    def generate_signal(self, length: int) -> np.ndarray:
        return random_binary_sequence(length)

    def modulate(self, signal: np.ndarray) -> np.ndarray:
        if self.modulation_type == 'bpsk':
            return bpsk_modulate(signal, self.carrier_freq, self.sample_rate, self.bit_duration)
        else:
            return qpsk_modulate(signal, self.carrier_freq, self.sample_rate, self.bit_duration)

    def add_channel_effects(self, modulated_signal: np.ndarray) -> np.ndarray:
        return awgn(modulated_signal, self.snr_db)

    def demodulate(self, received_signal: np.ndarray) -> np.ndarray:
        if self.modulation_type == 'bpsk':
            return bpsk_demodulate(received_signal, self.carrier_freq, self.sample_rate, self.bit_duration)
        else:
            return qpsk_demodulate(received_signal, self.carrier_freq, self.sample_rate, self.bit_duration)

    def run_simulation(self, data_length: int) -> dict:
        if self.modulation_type == 'qpsk' and data_length % 2 != 0:
            data_length += 1
        original_signal = self.generate_signal(data_length)
        if self.use_error_correction:
            if data_length % 4 != 0:
                pad = 4 - (data_length % 4)
                original_signal = np.pad(original_signal, (0, pad), mode='constant')
            signal_to_modulate = hamming_encode(original_signal)
        else:
            signal_to_modulate = original_signal
        modulated = self.modulate(signal_to_modulate)
        received = self.add_channel_effects(modulated)
        demodulated = self.demodulate(received)
        if self.use_error_correction:
            decoded = hamming_decode(demodulated)
            final_signal = decoded[:data_length]
        else:
            final_signal = demodulated[:data_length]
        ber = calculate_ber(original_signal, final_signal)
        return {
            'original_signal': original_signal,
            'modulated_signal': modulated,
            'received_signal': received,
            'demodulated_signal': final_signal,
            'ber': ber
        }
""",
    },
    base_dir / "tests": {
        "test_modulation.py": """import unittest
import numpy as np
from comm_engineering.modulation import bpsk_modulate, bpsk_demodulate

class TestModulation(unittest.TestCase):
    def test_bpsk(self):
        binary_sequence = np.array([0, 1, 0, 1])
        carrier_freq = 1000
        sample_rate = 10000
        bit_duration = 0.01
        modulated = bpsk_modulate(binary_sequence, carrier_freq, sample_rate, bit_duration)
        demodulated = bpsk_demodulate(modulated, carrier_freq, sample_rate, bit_duration)
        np.testing.assert_array_equal(binary_sequence, demodulated)

if __name__ == '__main__':
    unittest.main()
"""
    },
    base_dir.parent: {
        "setup.py": """from setuptools import setup, find_packages

setup(
    name='comm_engineering',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.19.0',
        'scipy>=1.5.0',
        'matplotlib>=3.3.0',
    ],
    author='Your Name',
    author_email='your.email@example.com',
    description='A Python package for communication engineering simulation and engineering.',
    url='https://github.com/yourusername/comm_engineering',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
"""
    }
}

# Function to create directories and files with error handling
def create_structure(structure):
    try:
        for directory, files in structure.items():
            # Create directory
            try:
                directory.mkdir(parents=True, exist_ok=True)
                print(f"Created directory: {directory}")
            except PermissionError as e:
                print(f"Error: Permission denied to create directory {directory}: {e}")
                sys.exit(1)
            except OSError as e:
                print(f"Error: Failed to create directory {directory}: {e}")
                sys.exit(1)

            # Create each file in the directory
            for filename, content in files.items():
                file_path = directory / filename
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content.strip())
                    print(f"Created: {file_path}")
                except PermissionError as e:
                    print(f"Error: Permission denied to write file {file_path}: {e}")
                    sys.exit(1)
                except IOError as e:
                    print(f"Error: Failed to write file {file_path}: {e}")
                    sys.exit(1)
                except Exception as e:
                    print(f"Unexpected error while writing {file_path}: {e}")
                    traceback.print_exc()
                    sys.exit(1)

        print("Directory structure and files created successfully!")
    except Exception as e:
        print(f"Critical error in create_structure: {e}")
        traceback.print_exc()
        sys.exit(1)

# Main execution with error handling
if __name__ == "__main__":
    try:
        # Verify current working directory is writable
        if not os.access(os.getcwd(), os.W_OK):
            print(f"Error: No write permission in current directory: {os.getcwd()}")
            sys.exit(1)

        create_structure(structure)
    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Exiting gracefully...")
        sys.exit(0)
    except Exception as e:
        print(f"Unexpected error during execution: {e}")
        traceback.print_exc()
        sys.exit(1)