import unittest
import numpy as np
from CommX.modulation import bpsk_modulate, bpsk_demodulate

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