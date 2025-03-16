import numpy as np
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