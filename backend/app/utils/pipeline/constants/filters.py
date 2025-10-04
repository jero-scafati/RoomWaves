"""
Module containing constants related to audio filters.

This module defines the standard center frequencies and parameters for
octave and third-octave filters according to the IEC 61260 standard.
"""

# Standard center frequencies for octave filters (Hz)
OCTAVE_FREQUENCIES = [
    125, 250, 500, 1000, 2000, 4000, 8000
]

# Standard center frequencies for third-octave filters (Hz)
THIRD_OCTAVE_FREQUENCIES = [
    125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600,
    2000, 2500, 3150, 4000, 5000, 6300, 8000
]

# Bandwidth factors (G)
BANDWIDTH_FACTOR_OCTAVE = 1.0 / 2.0         # 1/1 octave
BANDWIDTH_FACTOR_THIRD_OCTAVE = 1.0 / 6.0   # 1/3 octave