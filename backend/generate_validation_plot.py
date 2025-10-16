import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from app.services.get_parameters import process_impulse_response


def sintetizar_RI(
    frecuencias: dict,
    fs: int = 44100,
    piso_ruido_db: float = -60.0,
    delay_s: float = 0.5,
):
    """
    Genera una respuesta impulsiva sintética con múltiples frecuencias.
    
    Args:
        frecuencias: Diccionario {frecuencia: (t60, amplitud)}
        fs: Frecuencia de muestreo
        piso_ruido_db: Nivel de ruido en dB
        delay_s: Retardo inicial en segundos
    
    Returns:
        Diccionario con 'audio_data' y 'fs'
    """
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


# --- Configuración de la Simulación ---
N_RUNS = 10

# Valores base de T60 para cada frecuencia
BASE_T60_VALUES = {
    '125': 2.8,
    '250': 2.2,
    '500': 1.8,
    '1000': 1.5,
    '2000': 1.2,
    '4000': 1.0,
}

PISO_RUIDO_DB = -50.0

# --- Ejecución de las Simulaciones ---
results = []
for i in range(N_RUNS):
    print(f"Ejecutando simulación {i+1}/{N_RUNS}...")
    
    # Generar valores de T60 ligeramente diferentes para cada iteración (±5% de variación)
    variacion = 0.05
    known_t60_values = {}
    frecuencias_sinteticas = {}
    
    for freq_str, base_t60 in BASE_T60_VALUES.items():
        # Añadir variación aleatoria al T60 "conocido"
        varied_t60 = base_t60 * (1 + np.random.uniform(-variacion, variacion))
        known_t60_values[freq_str] = varied_t60
        frecuencias_sinteticas[int(freq_str)] = (varied_t60, 1.0)
    
    # Generar una nueva RI sintética en cada iteración
    synthetic_ri = sintetizar_RI(
        frecuencias=frecuencias_sinteticas,
        fs=44100,
        piso_ruido_db=PISO_RUIDO_DB,
        delay_s=0.2
    )
    
    # Procesar la RI para obtener los parámetros
    params = process_impulse_response(
        ri=synthetic_ri['audio_data'],
        fs=synthetic_ri['fs'],
        filter_type=1,  # Filtro de octava
        smoothing_window_ms=50
    )['parameters']
    
    # Calcular y almacenar el error porcentual
    for freq, expected_t60 in known_t60_values.items():
        if freq in params:
            t20 = params[freq]['T60_from_T20']
            t30 = params[freq]['T60_from_T30']
            
            error_t20 = ((t20 - expected_t60) / expected_t60) * 100
            error_t30 = ((t30 - expected_t60) / expected_t60) * 100
            
            results.append({'Frecuencia': f'{int(freq)} Hz', 'Error (%)': error_t20, 'Parámetro': 'T20'})
            results.append({'Frecuencia': f'{int(freq)} Hz', 'Error (%)': error_t30, 'Parámetro': 'T30'})

print("Simulaciones completadas.")

# --- Procesamiento y Visualización de Resultados ---
df = pd.DataFrame(results)

# 1. Imprimir estadísticas
print("\nResumen Estadístico del Error Porcentual:")
summary = df.groupby(['Parámetro', 'Frecuencia'])['Error (%)'].agg(['mean', 'std']).reset_index()
print(summary)

# 2. Generar el Boxplot
plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(14, 7))

# Ordenar las frecuencias correctamente
freq_order = ['125 Hz', '250 Hz', '500 Hz', '1000 Hz', '2000 Hz', '4000 Hz']
sns.boxplot(data=df, x='Frecuencia', y='Error (%)', hue='Parámetro', ax=ax, palette='viridis', order=freq_order)

#ax.set_title('Distribución del Error Porcentual en la Validación Sintética (10 Realizaciones)', fontsize=16)
ax.set_xlabel('Banda de Frecuencia', fontsize=20)
ax.set_ylabel('Error Porcentual (%)', fontsize=20)
ax.legend(title='Parámetro',fontsize=18)
ax.grid(True, which='both', linestyle='--', linewidth=0.5)
ax.tick_params(axis='x', labelsize=16)  
ax.tick_params(axis='y', labelsize=16)
# Ajustar escala del eje Y para mostrar mejor los errores pequeños
ax.set_ylim(-2, 2)
ax.axhline(y=0, color='red', linestyle='--', linewidth=1, alpha=0.5, label='Error = 0%')

plt.tight_layout()

# Guardar el gráfico
plt.savefig('figura_10_boxplot_validacion.png')
print("\nGráfico guardado como 'figura_10_boxplot_validacion.png'")
plt.show()
