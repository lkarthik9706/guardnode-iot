import numpy as np

WINDOW_SECONDS = 5.0  # Configurable observation window in seconds
MIN_OBSERVATION_WINDOWS = 2
MAX_RATE_HISTORY = 100

def compute_window_rate(packet_count: int, window_seconds: float = WINDOW_SECONDS) -> float:
    """
    Computes packet arrival rate for a single fixed observation window.
    packet_rate = number_of_packets_in_window / WINDOW_SECONDS
    """
    if window_seconds <= 0:
        return 0.0
    return round(float(packet_count) / float(window_seconds), 2)

def compute_lightweight_features(rates_history: list):
    """
    Computes packet rate summary features from a list/deque of completed window rates.
    
    Returns:
        mean_packet_rate (float)
        median_packet_rate (float)
        max_packet_rate (float)
        
    Feature Order:
        [mean_packet_rate, median_packet_rate, max_packet_rate]
    """
    if not rates_history or len(rates_history) == 0:
        return 0.0, 0.0, 0.0

    rates = [float(r) for r in rates_history]
    mean_rate = float(np.mean(rates))
    median_rate = float(np.median(rates))
    max_rate = float(np.max(rates))

    return round(mean_rate, 2), round(median_rate, 2), round(max_rate, 2)

