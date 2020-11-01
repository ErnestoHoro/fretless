from fractions import Fraction as frac

"""
sol - A command line music tool

* 24 frets
* When Pitch is first introduced in the Ultimate Music Theory Beginner A, B, C 
  Workbooks, we start with 3 Pitch Range Levels - Low, Middle and High.
"""

NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

PITCH_RANGES_VOICE = {
    ('F2', 'F4'): 'Bass',
    ('A2', 'A4'): 'Baritone',
    ('C3', 'C5'): 'Tenor',
    ('F3', 'F5'): 'Alto (Contralto)',
    ('A3', 'A5'): 'Mezzo-Soprano',
    ('C4', 'C6'): 'Soprano',
}

GUITAR_TUNINGS = {
    'E-A-D-G-B-E': {
        'type': 'standard',
        'description': '',
        'notation': ('E2', 'A2', 'D3', 'G3', 'B3', 'E4'),
    }
}

BASS_TUNINGS = {
    'E-A-D-G': {
        'type': 'standard',
        'description': '',
        'notation': ('E1', 'A1', 'D2', 'G2'),
    }
}

def get_frequency(n):
    frequency = frac(440, 32) * 2 ** frac(n, 12)
    frequency_str = '%.2f' % round(float(frequency), 2)

    return frequency_str


def get_frequency_generator(start=3):
    """start=3 equals C0 to be the first note with 16.352Hz"""
    n = start
    while True:
        yield get_frequency(n)
        n += 1


def get_notes_generator():
    while True:
        for note in NOTES:
            yield note


fretboard_matrix = [ [], [], [], [], [], [] ]
fretboard_matrix_frequencies = [ [], [], [], [], [], [] ]

fretboard_matrix_bass = [ [], [], [], [] ]
fretboard_matrix_frequencies_bass = [ [], [], [], [] ]

def get_notes_index():
    guitar_tuning_notation = GUITAR_TUNINGS['E-A-D-G-B-E']['notation']
    guitar_appender_indices = []

    bass_tuning_notation = BASS_TUNINGS['E-A-D-G']['notation']
    bass_appender_indices = []

    f_gen = get_frequency_generator()
    n_gen = get_notes_generator()

    scale_index = 0
    for i in range(3, 100):
        range_index = str(i - 2).zfill(3)
        if i % 12 == 0:
            scale_index = i // 12

        frequency = next(f_gen)
        note = next(n_gen)

        note_long = f'{note}{scale_index}'

        # create fretboard list of lists
        for i, tuning_key in enumerate(guitar_tuning_notation):
            if note_long == tuning_key:
                guitar_appender_indices.append(i)

        for appender_index in guitar_appender_indices:
            if len(fretboard_matrix[appender_index]) <= 24:
                fretboard_matrix[appender_index].append(note_long)
                fretboard_matrix_frequencies[appender_index].append(frequency)

        # create fretboard list of lists (bass)
        for i, tuning_key in enumerate(bass_tuning_notation):
            if note_long == tuning_key:
                bass_appender_indices.append(i)

        for appender_index in bass_appender_indices:
            if len(fretboard_matrix_bass[appender_index]) <= 24:
                fretboard_matrix_bass[appender_index].append(note_long)
                fretboard_matrix_frequencies_bass[appender_index].append(
                    frequency)

        print(f"i={range_index} "
              f"{frequency.rjust(7)}Hz "
              f"{note.ljust(2)} "
              f"{scale_index}")

    fretboard_matrix.reverse()
    fretboard_matrix_frequencies.reverse()

    fretboard_matrix_bass.reverse()
    fretboard_matrix_frequencies_bass.reverse()


def print_fretboards():
    print(*[f'{str(i).center(7)} |' for i in range(25)])
    print()

    for string in fretboard_matrix:
        print(*[f'{note.center(7)} |' for note in string])

    print()

    for string in fretboard_matrix_frequencies:
        print(*[f'{freq.rjust(7)} |' for freq in string])

    print()

    print(*[f'{str(i).center(7)} |' for i in range(25)])
    print()

    for string in fretboard_matrix_bass:
        print(*[f'{note.center(7)} |' for note in string])

    print()

    for string in fretboard_matrix_frequencies_bass:
        print(*[f'{freq.rjust(7)} |' for freq in string])


if __name__ == '__main__':
    get_notes_index()
    print_fretboards()
