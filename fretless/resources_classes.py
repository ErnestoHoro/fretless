from dataclasses import dataclass, field
from typing import Union

from resources import C_OCTAVES, TUNINGS

"""Class wrapping configurations from resources.py in Python dataclasses.

Mainly targets to encapsulate the creation of formatted string representations for end user views 
(STDOUT or text file). 
"""


@dataclass
class Tunings:
    # Todo: Should be frozen. Should be singleton?
    content: dict = field(default_factory=lambda: TUNINGS)
    choice_ids: list = None

    def __post_init__(self):
        self._update_choice_ids()

    def _update_choice_ids(self):
        """Creates a list of indices for a prompt selection.

        Note: For 'click.Choice(['str'])' all items must be of type str.
        """
        tuning_ids = list(self.content)
        choice_ids = [str(i) for i in range(0, len(tuning_ids))]

        self.choice_ids = choice_ids

    def get_tuning_id_by_choice_id(self, choice_id: Union[int, str]):
        """Returns tuning_id (e.g. 'E-A-D-G-B-E') by choice_id (e.g. '0', '1').

        This method allows for an integer based selection of tunings with a CLI.
        """
        return list(self.content)[int(choice_id)]

    def get_notation(self, tuning_id: str):
        return self.content[tuning_id]['notation']

    def get_description(self, tuning_id: str):
        return self.content[tuning_id]['description']

    def __str__(self):
        """Returns a table of available tunings."""
        formatted_lines = [
            f'{"ID".ljust(4)}'
            f'{"TuningID".ljust(14)}'
            f'{"Notation".ljust(24)}'
            f'Description'
        ]

        for index, (tuning_id, attributes) in enumerate(self.content.items()):
            notation = ' '.join(attributes['notation'])

            formatted_lines.append(
                f'{str(index).ljust(4)}'
                f'{tuning_id.ljust(14)}'
                f'{notation.ljust(24)}'
                f'{attributes["description"]}'
            )

        return '\n'.join(formatted_lines)


@dataclass
class COctaves:
    content: dict = field(default_factory=lambda: C_OCTAVES)

    def __str__(self):
        formatted_lines = []

        header = 'Index'.ljust(7) + \
                 'Notation'.ljust(12) + \
                 'Verbal'.ljust(16) + \
                 'Alternative'
        formatted_lines.append(header)

        for k, v in self.content.items():
            formatted_lines.append(
                f'{k.ljust(7)}'
                f'{v["name_short"].ljust(12)}'
                f'{v["name_long"].ljust(16)}'
                f'{v["name_alt"]}'
            )

        return '\n'.join(formatted_lines)
