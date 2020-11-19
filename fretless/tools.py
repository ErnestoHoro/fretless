from fractions import Fraction as frac

from resources import FREQUENCY_ROUND_DECIMALS, NOTES


def get_frequency(n, a_pitch_hz: int = 440):
    frequency = frac(a_pitch_hz, 32) * 2 ** frac(n, 12)
    frequency_format = f'%.{FREQUENCY_ROUND_DECIMALS}f'
    frequency_str = frequency_format % round(float(frequency), FREQUENCY_ROUND_DECIMALS)

    return frequency_str


def get_frequency_generator(start=3, a_pitch_hz: int = 440):
    """start=3 equals C0 to be the first note with 16.352Hz with A4=440Hz concert pitch"""
    n = start
    while True:
        yield get_frequency(n, a_pitch_hz)
        n += 1


def get_notes_generator():
    while True:
        for note in NOTES:
            yield note
