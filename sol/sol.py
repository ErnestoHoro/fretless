import copy
from collections.abc import Mapping

import colorama
from resources import TUNINGS, NUMBER_OF_FRETS, NOTE_COLOR_DEFAULT, NOTE_PADDING
from termcolor import colored
from tools import get_frequency_generator, get_notes_generator

"""
sol - A command line music tool
"""


class Sol:

    def __init__(self, tuning='E-A-D-G-B-E'):
        self.tunings = TUNINGS
        self.number_of_frets = NUMBER_OF_FRETS
        self.note_color_default = NOTE_COLOR_DEFAULT
        self.note_padding = NOTE_PADDING

        # available text colors: red, green, yellow, blue, magenta, cyan, white
        self.colored_notes = {
            'F2': 'green',
            'C3': 'red',
            'A#4': 'yellow',
            'G4': 'cyan',
        }

        self.tuning_notation = self.tunings[tuning]['notation']
        self.fretboard = {}

    def create_fretboard(self, tuning_notation):
        # Todo: Create them as Dicts rather than Lists.
        #       Add: :highlight-color, :special-sign, ':special-meaning', etc.
        #       Add: Additional methods to alternate attributes.
        #       Add: ~~Kinda full barre matches or something...
        #       Add: Map rather real life alternative notes (Bb instead of A#). -> look them up
        f_gen = get_frequency_generator()
        n_gen = get_notes_generator()

        indices_open_strings = []
        index_chromatic_scale = 0
        for index_note in range(3, 100):
            # update chromatic index (e.g. A0)
            if index_note % 12 == 0:
                index_chromatic_scale = index_note // 12

            # get note and attributes
            frequency_in_hz = next(f_gen)
            note = next(n_gen)
            note_long = f'{note}{index_chromatic_scale}'

            # update open string indices by tuning
            for i, note_tuning_open in enumerate(tuning_notation):
                if note_long == note_tuning_open:
                    indices_open_strings.append(i)

            # update fretboard
            for index_string in indices_open_strings:
                if self.fretboard.get(index_string):
                    note_id = len(self.fretboard.get(index_string))
                else:
                    note_id = 0

                if not note_id <= self.number_of_frets:
                    continue

                fretboard_update = {
                    index_string: {
                        note_long: {
                            'note_id': note_id,
                            'freq_hz': frequency_in_hz,
                            'color': self._get_color(note_long),
                        }
                    }
                }
                self._update_dictionary(self.fretboard, fretboard_update)

        self.fretboard = dict(sorted(self.fretboard.items()))

    def _update_dictionary(self, dict_base, dict_update):
        """Update nested dictionary with another dictionary."""
        for key, value in dict_update.items():
            value_base = dict_base.get(key)
            if isinstance(value, Mapping) and isinstance(value_base, Mapping):
                self._update_dictionary(value_base, value)  # recursive call
            else:
                dict_base[key] = copy.deepcopy(value)

    def _get_color(self, note_long):
        if note_long in self.colored_notes:
            return self.colored_notes.get(note_long)
        else:
            return self.note_color_default

    def _print_fretboard_header(self):
        # frets dots
        for i in range(self.number_of_frets + 1):
            if i in (3, 5, 7, 9, 15, 17, 19, 21):
                print('•'.center(self.note_padding) + ' |', end=' ')
            elif i in (12, 24):
                print('••'.center(self.note_padding) + ' |', end=' ')
            else:
                print(' '.center(self.note_padding) + ' |', end=' ')
        print()

        # frets indices
        print(*[str(i).center(self.note_padding) + ' |' for i in range(self.number_of_frets + 1)])
        print()

    def print_fretboard(self):
        colorama.init()

        # header
        self._print_fretboard_header()

        # notes
        for string_id, string_notes in reversed(self.fretboard.items()):
            for note, attributes in string_notes.items():
                color = attributes['color']
                print(colored(note.center(self.note_padding), color) + ' |', end=' ')
            print()

        print()

        # frequencies
        for string_id, string_notes in reversed(self.fretboard.items()):
            for _, attributes in string_notes.items():
                freq_hz = attributes['freq_hz']
                color = attributes['color']
                print(colored(freq_hz.center(self.note_padding), color) + ' |', end=' ')
            print()

    def main(self):
        self.create_fretboard(self.tuning_notation)
        self.print_fretboard()
