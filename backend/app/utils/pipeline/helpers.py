def to_db_scale(signal):
    import numpy as np
    
    max_abs = np.max(np.abs(signal))
    # Avoid division by zero for silent signals
    norm_signal = np.abs(signal) / max_abs if max_abs > 0 else np.abs(signal)
    # Clip to avoid log(0)
    clipped_signal = np.clip(norm_signal, 1e-10, None)
    return 10 * np.log10(clipped_signal)

def linear_regression(x, y) -> dict:
    import numpy as np
    
    x, y = np.asarray(x), np.asarray(y)
    n = len(x)
    if n == 0:
        return {'slope': 0, 'intercept': 0}
        
    sum_x, sum_y = np.sum(x), np.sum(y)
    sum_xx, sum_xy = np.sum(x * x), np.sum(x * y)
    
    denominator = (n * sum_xx - sum_x**2)
    if denominator == 0:
        return {'slope': -np.inf, 'intercept': 0}

    slope = (n * sum_xy - sum_x * sum_y) / denominator
    intercept = (sum_y - slope * sum_x) / n
    
    return {'slope': slope, 'intercept': intercept}

def linear_regression_in_range(x, y, upper_limit: float, lower_limit: float) -> dict:
    import numpy as np
    
    mask = (y <= upper_limit) & (y >= lower_limit)
    if not np.any(mask):
        return {'slope': -np.inf, 'intercept': 0}
        
    return linear_regression(x[mask], y[mask])