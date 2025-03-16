import numpy as np

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