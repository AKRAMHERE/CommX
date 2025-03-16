import numpy as np

def calculate_ber(original: np.ndarray, received: np.ndarray) -> float:
    if len(original) != len(received):
        raise ValueError("Original and received sequences must have the same length.")
    errors = np.sum(original != received)
    return errors / len(original)