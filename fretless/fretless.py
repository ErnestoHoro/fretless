import copy
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

    def __init__(self, tuning_id='E-A-D-G-B-E', verbose=False):
        colorama.init()

        self.number_of_frets = NUMBER_OF_FRETS
        self.note_color_default = NOTE_COLOR_DEFAULT
        self.note_padding = NOTE_PADDING

        self.tuning_id = tuning_id
        self.tuning_notation = self.TUNINGS.get_notation(tuning_id)
        self.tuning_description = self.TUNINGS.get_description(tuning_id)

        self.verbose = verbose

        self.fretboard_printer = FretboardPrinter()
        self.fretboard = {}

        # (experiment) generic scale (A minor pentatonic)
        # available text colors: red, green, yellow, blue, magenta, cyan, white
        self.colored_notes = {
            'A': 'red',
            'C': 'green',
            'D': 'green',
            'D#': 'blue',
            'E': 'green',
            'F': 'blue',
            'G': 'green',
        }

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
                        }
                    }
                }
                self._update_dictionary(self.fretboard, fretboard_update)

        self.fretboard = dict(sorted(self.fretboard.items()))

        self.fretboard_printer.fretboard = self.fretboard
        self.fretboard_printer.tuning_id = self.tuning_id
        self.fretboard_printer.tuning_description = self.tuning_description

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

    def main(self):
        self.create_fretboard(self.tuning_notation)
        self.fretboard_printer.print_fretboard()


# -- command line interface & user documentation -----------------------------------------------/100

@click.command(options_metavar='<options>')
@click.option('--print-c-octaves', is_flag=True,
              help='Prints a table showing progression of octaves from C0-C10.')
@click.option('--verbose', is_flag=True,
              help='Will print verbose/debug messages.')
# Todo: Add export option (--save). Ensure color sequences are removed.
def cli(print_c_octaves, verbose):
    """fretless - A command line music tool

    \b
      _|          |    |
     |    __| _ \ __|  |   _ \   __|   __|  ┏ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ┓
     __| |    __/ |    |   __/ \__ \ \__ \  ┃ github.com/ErnestoHoro/fretless ┃
    _|  _|  \___|\__| _| \___| ____/ ____/  ┗ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ┛

    Renders a text based fretboard for different string instruments by a given tuning (id).

    \b
    Render options included:
    * exact notes (e.g. C4, D#5)
    * frequencies (rounding option)
    * context specific customizable colorized print
      (e.g. C#4 and all B in yellow, by scale or similar)

    Have a good time and fret less.
    """
    fretless = Fretless(verbose=verbose)

    if print_c_octaves:
        print(fretless.C_OCTAVES)
        sys.exit()

    while True:
        print(fretless.TUNINGS)

        choice_ids = click.Choice(fretless.TUNINGS.choice_ids)
        choice_user = click.prompt('\nPlease select ID', default='0', type=choice_ids)

        fretless.tuning_id = fretless.TUNINGS.get_tuning_id_by_choice_id(choice_id=choice_user)
        fretless.main()

        input(colored('PRESS KEY TO CONTINUE\n', attrs=['bold']))


if __name__ == '__main__':
    cli()
