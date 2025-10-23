def nextpow2(x: float) -> int:
    import numpy as np
    """Calculates the next power of 2 greater than or equal to x."""
    return int(2**np.ceil(np.log2(x)))

def octave_smooth_fast(f, mag_db, bands_per_oct: int = 24):
    import numpy as np
    
    mask_pos = f > 0
    f_pos = f[mask_pos]
    mag_db_pos = mag_db[mask_pos]

    n_octaves = np.log2(f_pos[-1] / 20)
    n_centers = max(10, int(np.ceil(bands_per_oct * n_octaves)))

    centers = np.geomspace(20, f_pos[-1], n_centers)
    k = 2 ** (1.0 / (2.0 * bands_per_oct))

    mag_lin = 10**(mag_db_pos / 20.0)
    centers_rms = np.zeros_like(centers)
    
    for i, c in enumerate(centers):
        lo = c / k
        hi = c * k
        i0 = np.searchsorted(f_pos, lo, side='left')
        i1 = np.searchsorted(f_pos, hi, side='right')
        if i1 <= i0:
            idx = np.argmin(np.abs(f_pos - c))
            centers_rms[i] = mag_lin[idx]
        else:
            window_vals = mag_lin[i0:i1]
            centers_rms[i] = np.sqrt(np.mean(window_vals**2))

    centers_db = 20.0 * np.log10(np.clip(centers_rms, 1e-12, None))
    
    interp_vals = np.interp(np.log10(f_pos), np.log10(centers), centers_db,
                            left=centers_db[0], right=centers_db[-1])

    mag_smooth_db = np.full_like(mag_db, -120.0)
    mag_smooth_db[mask_pos] = interp_vals
    return mag_smooth_db


def get_frequency_data(
    y,
    sr: int,
    bands_per_oct: int = 24,
    max_nfft: int = 262144
) -> dict[str, list[float]]:
    import numpy as np
    from scipy.fft import rfft, rfftfreq
    
    nfft = min(nextpow2(len(y)) * 4, max_nfft)

    H = rfft(y, n=nfft)
    f = rfftfreq(nfft, 1.0 / sr)

    mag_db = 20.0 * np.log10(np.abs(H) + 1e-16)

    fmin = 20
    fmax = sr / 2.0
    
    mag_smooth_db = octave_smooth_fast(
        f, mag_db, bands_per_oct=bands_per_oct
    )

    mask = (f >= fmin) & (f <= fmax)
    
    return {
        "frequencies": f[mask].tolist(), 
        "magnitudes": mag_smooth_db[mask].tolist()
    }
