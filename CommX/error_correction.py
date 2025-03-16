import numpy as np

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