from dataclasses import dataclass, field
from typing import Union

from resources import NUMBER_OF_FRETS, NOTE_PADDING
from termcolor import colored


@dataclass
class FretboardPrinter:
    fretboard: dict = None
    tuning_id: str = None
    tuning_description: str = None
    a_pitch_hz: Union[int, float] = None

    note_padding: int = field(default_factory=lambda: NOTE_PADDING)
    number_of_frets: int = field(default_factory=lambda: NUMBER_OF_FRETS)

    def _print_header(self):
        # title
        print(colored(
            f"[ {self.tuning_id} | {self.tuning_description} ]", attrs=['reverse', 'bold']),
            f"[ A4={str(self.a_pitch_hz)}Hz ]")
        print()

        # frets dots
        for i in range(self.number_of_frets + 1):
            if i in (3, 5, 7, 9, 15, 17, 19, 21):
                print(' •'.center(self.note_padding) + ' |', end='')
            elif i in (12, 24):
                print('   ••'.center(self.note_padding) + ' |', end='')
            else:
                print(' '.center(self.note_padding) + ' |', end='')
        print()

        # frets indices
        print(' ', end='')
        print(*[str(i).center(self.note_padding) + '|' for i in range(self.number_of_frets + 1)])
        print()

    def print_fretboard(self):
        self._print_header()

        print_streams = {
            'notes': [],
            'frequencies': [],
        }

        for string_id, string_notes in reversed(self.fretboard.items()):
            for note, attributes in string_notes.items():
                color = attributes['color']
                freq_hz = attributes['freq_hz']
                print_streams['notes'].append(
                    colored(' ' + note.center(self.note_padding), color) + '|')
                print_streams['frequencies'].append(
                    colored(freq_hz.rjust(self.note_padding), color) + ' |')
            print_streams['notes'].append('\n')
            print_streams['frequencies'].append('\n')

        print(''.join(print_streams['notes']), end='\n')
        print(''.join(print_streams['frequencies']), end='\n')

    # Todo: Add HTML table render + CSS (elsewhere?). (use DOM lib & pretty-print)
