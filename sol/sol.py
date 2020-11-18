import copy
from collections.abc import Mapping

import click as click
import colorama
import resources_classes
from resources import TUNINGS, NUMBER_OF_FRETS, NOTE_COLOR_DEFAULT, NOTE_PADDING
from termcolor import colored
from tools import get_frequency_generator, get_notes_generator


class Sol:

    def __init__(self, verbose=False, tuning='E-A-D-G-B-E'):
        colorama.init()

        # assign defaults
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

        # (experiment) generic scale (A major)
        self.colored_notes = {
            'A': 'red',
            'B': 'green',
            'C#': 'green',
            'D': 'green',
            'E': 'green',
            'F#': 'green',
            'G#': 'green',
        }

        # (experiment) generic scale (A minor pentatonic)
        self.colored_notes = {
            'A': 'red',
            'C': 'green',
            'D': 'green',
            'D#': 'blue',
            'E': 'green',
            'F': 'blue',
            'G': 'green',
        }

        self.tuning = tuning
        self.tuning_notation = self.tunings[tuning]['notation']
        self.tuning_description = self.tunings[tuning]['description']

        self.fretboard = {}

    def create_fretboard(self, tuning_notation):
        # Todo: Create them as Dicts rather than Lists.
        #       Add: :highlight-color, :special-sign, ':special-meaning', etc.
        #       Add: Additional methods to alternate attributes.
        #       Add: ~~Kinda full barre matches or something...
        #       Add: Map rather real life alternative notes (B♭/b instead of A#). -> look them up
        f_gen = get_frequency_generator()
        n_gen = get_notes_generator()

        indices_open_strings = []
        index_chromatic_scale = 0
        # octaves C0 to C10 (C-1 is ignored)
        for index_note in range(132):
            # update octave/chromatic index (e.g. A0)
            if index_note % 12 == 0:
                index_chromatic_scale = index_note // 12

            # get note and attributes
            freq_in_hz = next(f_gen)
            note = next(n_gen)  # Todo: Convert pitch to real-life type (sharp AND flat notation).
            note_long = f'{note}{index_chromatic_scale}'

            # index_note=0 note_long='C0' freq_in_hz='16.35' (1st)
            # print(f'{index_note=} {note_long=} {freq_in_hz=}')  # Todo: Add logger.debug().

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
                            'freq_hz': freq_in_hz,
                            'color': self._get_color(note_long),
                            'pitch': self._get_pitch(note_long),
                        }
                    }
                }
                self._update_dictionary(self.fretboard, fretboard_update)

        self.fretboard = dict(sorted(self.fretboard.items()))
        # print(self.fretboard)

    def _update_dictionary(self, dict_base, dict_update):
        """Update nested dictionary with another dictionary."""
        for key, value in dict_update.items():
            value_base = dict_base.get(key)
            if isinstance(value, Mapping) and isinstance(value_base, Mapping):
                self._update_dictionary(value_base, value)  # recursive call
            else:
                dict_base[key] = copy.deepcopy(value)

    def _get_color(self, note_long):
        # Todo: Add secondary parameters, e.g. frequency range (or add get_highlight,
        #  get_background, etc.).
        # Todo: Match global if not endswith digit.
        if note_long in self.colored_notes:
            return self.colored_notes.get(note_long)
        elif note_long[:-1] in self.colored_notes:
            return self.colored_notes.get(note_long[:-1])
        else:
            return self.note_color_default

    @staticmethod
    def _get_pitch(note_long):
        if any((char in '#') for char in note_long):
            return 'sharp'
        elif any((char in 'b') for char in note_long):
            return 'flat'
        else:
            return ''

    def _print_fretboard_header(self):
        # title
        print(colored(f"[ {self.tuning} | {self.tuning_description} ]", attrs=['reverse', 'bold']))
        print()

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
                print(colored(freq_hz.rjust(self.note_padding), color) + ' |', end=' ')
            print()

        print()

        # pitch
        for string_id, string_notes in reversed(self.fretboard.items()):
            for _, attributes in string_notes.items():
                pitch = attributes['pitch']
                color = attributes['color']
                print(colored(pitch.center(self.note_padding), color) + ' |', end=' ')
            print()

    @classmethod
    def print_tunings(cls):
        """Prints tunings available for rendering a fretboard."""
        print(resources_classes.Tunings().__str__())

    @classmethod
    def print_c_octaves(cls):
        """Prints a table showing progression of octaves from C0-C10."""
        print(resources_classes.COctaves().__str__())

    def main(self):
        self.create_fretboard(self.tuning_notation)
        self.print_fretboard()


# -- command line interface & user documentation -----------------------------------------------/100

@click.command(options_metavar='<options>')
@click.option('--print-tunings', is_flag=True,
              help='Prints tunings available for rendering a fretboard.')
@click.option('--print-c-octaves', is_flag=True,
              help='Prints a table showing progression of octaves from C0-C10.')
@click.option('--verbose', is_flag=True,
              help='Will print verbose/debug messages.')
def cli(print_tunings, print_c_octaves, verbose):
    """sol - A command line music tool

    Renders a text based fretboard.
    """
    if verbose:
        click.echo(f'Passed arguments: {print_tunings=} {print_c_octaves=}')

    if print_tunings:
        Sol().print_tunings()

    if print_c_octaves:
        Sol().print_c_octaves()

    if not any((print_tunings, print_c_octaves)):
        Sol(verbose).main()


if __name__ == '__main__':
    cli()
