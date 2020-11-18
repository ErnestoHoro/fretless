FREQUENCY_ROUND_DECIMALS = 2
NUMBER_OF_FRETS = 24
NOTE_COLOR_DEFAULT = None
NOTE_PADDING = 7

NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

TUNINGS = {
    'E-A-D-G-B-E': {
        'description': 'standard tuning - guitar',
        'notation': ('E2', 'A2', 'D3', 'G3', 'B3', 'E4'),
    },
    'D-A-D-G-B-E': {
        'description': 'guitar drop-d',
        'notation': ('D2', 'A2', 'D3', 'G3', 'B3', 'E4'),
    },
    'D-A-D-G-B-D': {
        'description': 'guitar double-drop-d',
        'notation': ('D2', 'A2', 'D3', 'G3', 'B3', 'D4'),
    },
    'D-A-D-F#-A-D': {
        'description': 'guitar open-d',
        'notation': ('D2', 'A2', 'D3', 'F#3', 'A3', 'D4'),
    },
    'C-A-D-G-B-E': {
        'description': 'guitar drop-c',
        'notation': ('C2', 'A2', 'D3', 'G3', 'B3', 'E4'),
    },
    'E-A-D-G': {
        'description': 'standard tuning - electric bass, ukulele bass',
        'notation': ('E1', 'A1', 'D2', 'G2'),
    },
    'G-D-A-E': {
        'description': 'standard tuning - violin',
        'notation': ('G3', 'D4', 'A4', 'E4'),
    },
    'G-C-E-A': {
        'description': 'standard tuning - ukulele soprano',
        'notation': ('G4', 'C4', 'E4', 'A4'),
    },
    'D-G-B-E': {
        'description': 'ukulele baritone',
        'notation': ('D3', 'G3', 'B3', 'E4')
    },
}

SCALES = {
    # Todo
}

PITCH_RANGES_VOICE = {
    ('F2', 'F4'): 'Bass',
    ('A2', 'A4'): 'Baritone',
    ('C3', 'C5'): 'Tenor',
    ('F3', 'F5'): 'Alto (Contralto)',
    ('A3', 'A5'): 'Mezzo-Soprano',
    ('C4', 'C6'): 'Soprano',
}

PITCH_INDICES = {
    'C4': 'Middle C',
}
