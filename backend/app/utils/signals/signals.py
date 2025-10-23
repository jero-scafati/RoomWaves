from io import BytesIO  
import base64

def generar_sweep_inverse(duracion,fs=44100 ,f_inferior=20 ,f_superior=20000):
    import numpy as np
    """
    Genera un barrido logarítmico de frecuencias (sine sweep) y un filtro inverso, entre f_inferior y f_superior.

    Parámetros
    ----------
    duracion : float
        Duración del barrido en segundos.
    fs : int, opcional
        Frecuencia de muestreo en Hz. Por defecto es 44100 Hz.
    f_inferior : float, opcional
        Frecuencia inferior del barrido en Hz. Por defecto es 20 Hz.
    f_superior : float, opcional
        Frecuencia superior del barrido en Hz. Por defecto es 20000 Hz.

    Returns
    -------
    sweep : np.ndarray
        Señal generada del barrido logarítmico normalizada.

    inverse_sweep : np.ndarray
        Señal generada del barrido logarítmico inverso normalizada.
    
    fs : int
        Frecuencia de muestreo utilizada.

    Ejemplo
    -------
    Generar un barrido logarítmico de frecuencias entre 20 Hz y 20000 Hz durante 10 segundos:

        sweep, inverse, fs = generar_sweep_inverse(10)
    """
    R = np.log(f_superior/f_inferior)
    muestras = int(duracion * fs)
    L = duracion/R
    K = L * 2 * np.pi * f_inferior

    #Generacion de vectores con numpy
    t = np.linspace(0, duracion, muestras, endpoint=False)
    sweep = np.sin(K * (np.exp(t/L) - 1 ))
    #Generacion de vectores con numpy
    m_t = f_inferior/((K/L) *(np.exp(t/L)))
    m_t *= sweep[::-1]
    inverse_sweep = m_t

    # Normalización, para evitar saturacion al reproducir
    sweep /= np.max(np.abs(sweep))
    inverse_sweep /= np.max(np.abs(inverse_sweep))

    return sweep.astype(np.float32), inverse_sweep.astype(np.float32), fs

def wav_to_b64(signal, fs):
    from soundfile import write
    buf = BytesIO()
    write(buf, signal, fs, format='WAV')
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('ascii')

def get_ir_from_deconvolution(
    recording,
    inverse_filter,
    fs: int,
    start_margin_ms: float = 20.0,
    duration_factor: float = 4.0
) -> dict | None:
    import numpy as np
    from scipy.signal import hilbert
    
    try:
        n_linear = len(recording) + len(inverse_filter) - 1
        n_fft = 1 << int(np.ceil(np.log2(n_linear)))

        fft_rec = np.fft.fft(recording, n=n_fft)
        fft_inv = np.fft.fft(inverse_filter, n=n_fft)

        ir_full_complex = np.fft.ifft(fft_rec * fft_inv)
        ir_full = np.real(ir_full_complex)
        ir_full = ir_full[:n_linear]

        if len(ir_full) == 0 or np.all(ir_full == 0):
            return None

        peak_index = np.argmax(np.abs(ir_full))
        peak_value = np.abs(ir_full[peak_index])

        if peak_value < 1e-9:
            max_abs = np.max(np.abs(ir_full))
            if max_abs > 1e-9:
                ir_full /= max_abs
            return {'audio_data': ir_full, 'fs': fs}

        start_samples = int(start_margin_ms * fs / 1000)
        start_index = max(0, peak_index - start_samples)

        analytic_signal = hilbert(ir_full[peak_index:])
        envelope = np.abs(analytic_signal)
        envelope_db = 20 * np.log10(envelope / peak_value + 1e-9)

        valid_indices = np.where((envelope_db >= -35) & (envelope_db <= -5))[0]
        
        if len(valid_indices) > int(0.05 * fs):
            time_vals = valid_indices / fs
            db_vals = envelope_db[valid_indices]
            
            try:
                slope = np.polyfit(time_vals, db_vals, 1)[0]
                if slope < 0:
                    estimated_t60 = -60.0 / slope
                    estimated_t60 = np.clip(estimated_t60, 0.1, 10.0)
                else:
                    estimated_t60 = 1.0
            except:
                estimated_t60 = 1.0
        else:
            estimated_t60 = 1.0

        ir_duration = estimated_t60 * duration_factor
        end_index = peak_index + int(ir_duration * fs)
        end_index = min(end_index, len(ir_full))

        if end_index <= start_index:
            start_index = 0
            end_index = len(ir_full)

        trimmed_ir = ir_full[start_index:end_index]

        max_abs_trimmed = np.max(np.abs(trimmed_ir))
        if max_abs_trimmed > 1e-9:
            trimmed_ir /= max_abs_trimmed

        return {'audio_data': trimmed_ir, 'fs': fs}

    except Exception as e:
        print(f"Error during deconvolution and trimming: {e}")
        import traceback
        traceback.print_exc()
        return None