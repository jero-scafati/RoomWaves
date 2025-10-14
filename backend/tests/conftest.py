import numpy as np
import pytest


def sintetizar_RI(
    frecuencias: dict,
    fs: int = 44100,
    piso_ruido_db: float = -60.0,
    delay_s: float = 0.5,
):
    t60max = max(v[0] for v in frecuencias.values())
    segundos = 1.2 * t60max
    t = np.arange(0, segundos, 1/fs)
    
    ri = np.zeros_like(t)
    factor = 3 * np.log(10)

    for freq, (t60, A) in frecuencias.items():
        tau_i = factor / t60
        ri += A * np.exp(-tau_i * t) * np.cos(2 * np.pi * freq * t)
       
    rms_ruido = 10 ** (piso_ruido_db / 20)
    ruido = rms_ruido * np.random.randn(len(t))

    ri_ruido = ri + ruido

    delay = rms_ruido * np.random.rand(int(delay_s * fs))
    ri_ruido = np.concatenate((delay, ri_ruido))

    ri_ruido /= np.max(np.abs(ri_ruido))
    
    return {'audio_data': ri_ruido, 'fs': fs}


@pytest.fixture
def synthetic_ri_single_band():
    np.random.seed(42)
    return sintetizar_RI(
        frecuencias={1000: (1.0, 1.0)},
        fs=44100,
        piso_ruido_db=-60.0,
        delay_s=0.1
    )


@pytest.fixture
def synthetic_ri_multi_band():
    np.random.seed(42)
    return sintetizar_RI(
        frecuencias={
            125: (2.8, 1.0),
            250: (2.2, 1.0),
            500: (1.8, 1.0),
            1000: (1.5, 1.0),
            2000: (1.2, 1.0),
            4000: (1.0, 1.0),
        },
        fs=44100,
        piso_ruido_db=-50.0,
        delay_s=0.2
    )


@pytest.fixture
def known_t60_values():
    return {
        '125': 2.8,
        '250': 2.2,
        '500': 1.8,
        '1000': 1.5,
        '2000': 1.2,
        '4000': 1.0,
    }


@pytest.fixture
def known_snr_synthetic():
    np.random.seed(42)
    result = sintetizar_RI(
        frecuencias={1000: (1.0, 1.0)},
        fs=44100,
        piso_ruido_db=-60.0,
        delay_s=0.1
    )
    expected_snr = 60.0
    tolerance = 5.0
    return result, expected_snr, tolerance
