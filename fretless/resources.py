# Todo: Make them CLI/internal defaults.
FREQUENCY_ROUND_DECIMALS = 2
NUMBER_OF_FRETS = 24
NOTE_COLOR_DEFAULT = None
NOTE_PADDING = 8


# Todo: Handle enharmonic representations (sharp/flat).
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
    # Todo: Color codings for scales.
}

"""Note: In MIDI software the middle C can differ from the classical piano specification (C3-C5)."""
C_OCTAVES = {
    'C0': {
        'name_short': 'C͵͵',
        'name_long': 'subcontra',
        'name_alt': '',
    },
    'C1': {
        'name_short': 'C͵',
        'name_long': 'contra',
        'name_alt': '',
    },
    'C2': {
        'name_short': 'C',
        'name_long': 'great',
        'name_alt': "low/cello C, 8' C'",
    },
    'C3': {
        'name_short': 'c',
        'name_long': 'small',
        'name_alt': "tenor C, 4' C",
    },
    'C4': {
        'name_short': 'c′',
        'name_long': 'one-lined',
        'name_alt': 'middle C (classical piano)',
    },
    'C5': {
        'name_short': 'c′′',
        'name_long': 'two-lined',
        'name_alt': 'high/top/treble C',
    },
    'C6': {
        'name_short': 'c′′′',
        'name_long': 'three-lined',
        'name_alt': '(high)/top/soprano C',
    },
    'C7': {
        'name_short': 'c′′′′',
        'name_long': 'four-lined',
        'name_alt': 'double high C',
    },
    'C8': {
        'name_short': 'c′′′′′',
        'name_long': 'five-lined',
        'name_alt': 'triple high C',
    },
    'C9': {
        'name_short': 'c′′′′′′',
        'name_long': 'six-lined',
        'name_alt': 'quadruple high C',
    },
    'C10': {
        'name_short': 'c′′′′′′′',
        'name_long': 'seven-lined',
        'name_alt': 'quintuple high C',
    },
}

PITCH_RANGES_VOICE = {
    ('F2', 'F4'): 'Bass',
    ('A2', 'A4'): 'Baritone',
    ('C3', 'C5'): 'Tenor',
    ('F3', 'F5'): 'Alto (Contralto)',
    ('A3', 'A5'): 'Mezzo-Soprano',
    ('C4', 'C6'): 'Soprano',
}

# Todo: Add human frequency ranges with info (audible, voice-range, etc.)
# Todo: Add intervals with info (see self made music theory docu).
