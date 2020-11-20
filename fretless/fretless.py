import copy
import os
import signal
import sys
from collections.abc import Mapping

import click as click
import colorama
from fretless_printer import FretboardPrinter
from resources import NUMBER_OF_FRETS, NOTE_COLOR_DEFAULT, NOTE_PADDING
from resources_classes import Tunings, COctaves
from termcolor import colored
from tools import get_frequency_generator, get_notes_generator


class Fretless:
    TUNINGS = Tunings()
    C_OCTAVES = COctaves()

    def __init__(self, tuning_id='E-A-D-G-B-E', a_pitch_hz=440, verbose=False):
        colorama.init()

        self.number_of_frets = NUMBER_OF_FRETS
        self.note_color_default = NOTE_COLOR_DEFAULT

        self.tuning_id = tuning_id
        self.a_pitch_hz = a_pitch_hz
        self.verbose = verbose

        self.fretboard_printer = FretboardPrinter()
        self.fretboard = {}

        # (experiment) generic scale (A minor pentatonic)
        # available text colors: red, green, yellow, blue, magenta, cyan, white
        self.colored_notes = {
            # root
            'B': 'red',
            # dim
            'A': 'white',
            'A#': 'white',
            # lower range
            'E2': 'yellow',
            'F#2': 'yellow',
            'G#2': 'yellow',
            'C#3': 'magenta',
            'D3': 'yellow',
            'E3': 'yellow',
            # middle range
            'F#3': 'blue',
            'G#3': 'blue',
            'C#4': 'magenta',
            'D4': 'blue',
            'E4': 'blue',
            # B.B. King Major Blues Box (I) range
            'F#4': 'green',
            'G#4': 'green',
            'C#5': 'magenta',
            'D5': 'green',
            'E5': 'green',
            'F#5': 'green',
            'G#5': 'green',
            'C#6': 'magenta',
            'D6': 'green',
            'E6': 'green',
        }
        # Todo: Create Color-interaction class. (transpose, etc.)
        # Todo: Create analysis class for colored notes collections (intervals, possible
        #  inversions).

    def create_fretboard(self):
        tuning_notation = self.TUNINGS.get_notation(self.tuning_id)
        tuning_description = self.TUNINGS.get_description(self.tuning_id)

        fretboard = {}

        f_gen = get_frequency_generator(a_pitch_hz=self.a_pitch_hz)
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
            note = next(n_gen)
            note_long = f'{note}{index_chromatic_scale}'

            if self.verbose:
                print(f'{index_note=} {note_long=} {freq_in_hz=}')

            # update open string indices by tuning
            for i, note_tuning_open in enumerate(tuning_notation):
                if note_long == note_tuning_open:
                    indices_open_strings.append(i)

            # update fretboard
            for index_string in indices_open_strings:
                if fretboard.get(index_string):
                    note_id = len(fretboard.get(index_string))
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
                        }
                    }
                }
                self._update_dictionary(fretboard, fretboard_update)

        self.fretboard = dict(sorted(fretboard.items()))

        self.fretboard_printer.fretboard = self.fretboard
        self.fretboard_printer.tuning_id = self.tuning_id
        self.fretboard_printer.tuning_description = tuning_description
        self.fretboard_printer.a_pitch_hz = self.a_pitch_hz

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
        elif note_long[:-1] in self.colored_notes:
            return self.colored_notes.get(note_long[:-1])
        else:
            return self.note_color_default

    def main(self):
        self.create_fretboard()
        self.fretboard_printer.print_fretboard()


@click.command(options_metavar='<options>')
@click.option('--a-pitch-hz', default=440, type=int, show_default=True,
              help='A4 reference frequency in Hz. (432, 428)')
@click.option('--print-c-octaves', is_flag=True,
              help='Prints a table showing progression of octaves from C0-C10.')
@click.option('--verbose', is_flag=True,
              help='Will print verbose/debug messages.')
# Todo: Add tuning pass through with single print. Add export option (--save).
def cli(a_pitch_hz, print_c_octaves, verbose):
    """fretless - A command line music tool

    \b
      _|          |    |
     |    __| _ \ __|  |   _ \   __|   __|  ┏ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ┓
     __| |    __/ |    |   __/ \__ \ \__ \  ┃ github.com/ErnestoHoro/fretless ┃
    _|  _|  \___|\__| _| \___| ____/ ____/  ┗ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ┛

    Renders a text based fretboard for different string instruments by tuning.

    \b
    Before you start, please note:
    * correct text rendering requires either
      (a) a wide terminal canvas (size up your window) or
      (b) a horizontally scrollable terminal with disabled line wrap or (...)
    * colors and special symbols might not be well supported by your terminal
    * if terminal configuration is too much for you, try to run from embedded
      ones of IDEs/editors like PyCharm or Visual Studio Code

    Have a good time and fret less.
    """
    def signal_handler():
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    fretless = Fretless(a_pitch_hz=a_pitch_hz, verbose=verbose)

    if print_c_octaves:
        print(fretless.C_OCTAVES)
        sys.exit()

    while True:
        print(fretless.TUNINGS)

        choice_ids = click.Choice(fretless.TUNINGS.choice_ids)
        choice_user = click.prompt('\nPlease select ID', default='0', type=choice_ids)

        fretless.tuning_id = fretless.TUNINGS.get_tuning_id_by_choice_id(choice_id=choice_user)
        fretless.main()
        # Todo: Select color-coding/scale (once they're done).
        # Todo: Press ENTER to continue.
        # Todo: Press S to save to file.
        # Todo: Press H to save to html file.
        # Todo: Press D to save to text + html file.
        # Todo: Press LEFT/RIGHT to transpose color coding by a half step.
        input(colored('PRESS KEY TO CONTINUE\n', attrs=['bold']))


if __name__ == '__main__':
    cli()
