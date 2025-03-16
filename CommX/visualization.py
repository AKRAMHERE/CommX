import numpy as np
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