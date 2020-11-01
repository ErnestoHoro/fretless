import copy

from resources import TUNINGS
from tools import get_frequency_generator, get_notes_generator

"""
sol - A command line music tool
"""


class Sol:

    def __init__(self):
        self.tunings = TUNINGS

    @staticmethod
    def create_fretboard_matrices(tuning):
        matrix_fretboard_notes = [[] for _ in range(len(tuning))]
        matrix_fretboard_frequencies = copy.deepcopy(matrix_fretboard_notes)

        f_gen = get_frequency_generator()
        n_gen = get_notes_generator()

        indices_open_strings = []

        index_chromatic_scale = 0
        for index_note in range(3, 100):
            # update chromatic index (e.g. A0)
            if index_note % 12 == 0:
                index_chromatic_scale = index_note // 12

            frequency_in_hz = next(f_gen)
            note = next(n_gen)
            note_long = f'{note}{index_chromatic_scale}'

            # update open string indices
            for i, note_tuning_open in enumerate(tuning):
                if note_long == note_tuning_open:
                    indices_open_strings.append(i)

            # populate matrices (to a maximum of 25 notes per string)
            for index_string in indices_open_strings:
                if len(matrix_fretboard_notes[index_string]) <= 24:
                    matrix_fretboard_notes[index_string].append(note_long)
                    matrix_fretboard_frequencies[index_string].append(frequency_in_hz)

        matrix_fretboard_notes.reverse()
        matrix_fretboard_frequencies.reverse()

        return matrix_fretboard_notes, matrix_fretboard_frequencies

    def print_fretboards(self):
        for tuning_id, tuning_attributes in self.tunings.items():
            # title
            print(f"[ {tuning_id} | {tuning_attributes['description']} ]")
            print()

            # fret dots
            for i in range(25):
                if i in (3, 5, 7, 9, 15, 17, 19, 21):
                    print('•'.center(7) + ' |', end=' ')
                elif i in (12, 24):
                    print('••'.center(7) + ' |', end=' ')
                else:
                    print(' '.center(7) + ' |', end=' ')
            print()

            # fret number
            print(*[str(i).center(7) + ' |' for i in range(25)])
            print()

            # notes
            for string in tuning_attributes['fretboard-notes']:
                print(*[note.center(7) + ' |' for note in string])
            print()

            # frequencies
            for string in tuning_attributes['fretboard-frequencies']:
                print(*[freq.rjust(7) + ' |' for freq in string])
            print()

    def main(self):
        for tuning_id, tuning_attributes in self.tunings.items():
            tuning = tuning_attributes['notation']
            matrix_fretboard_notes, matrix_fretboard_frequencies = \
                self.create_fretboard_matrices(tuning)

            self.tunings[tuning_id]['fretboard-notes'] = matrix_fretboard_notes
            self.tunings[tuning_id]['fretboard-frequencies'] = matrix_fretboard_frequencies


if __name__ == '__main__':
    sol = Sol()
    sol.main()
    sol.print_fretboards()
