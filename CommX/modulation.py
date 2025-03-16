import numpy as np

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