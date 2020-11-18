from dataclasses import dataclass, field

from resources import C_OCTAVES, TUNINGS

"""Class wrapping configurations from resources.py in Python dataclasses.

Mainly targets to encapsulate the creation of formatted string representations for end user views 
(STDOUT or text file). 
"""


@dataclass
class COctaves:
    content: dict = field(default_factory=lambda: C_OCTAVES)

    def __str__(self, with_header=True):
        formatted_lines = []

        if with_header:
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


@dataclass
class Tunings:
    content: dict = field(default_factory=lambda: TUNINGS)

    def __str__(self, with_header=True):
        formatted_lines = []

        if with_header:
            header = 'TuningID'.ljust(14) + \
                     'Notation'.ljust(24) + \
                     'Description'
            formatted_lines.append(header)

        for tuning_id, attributes in self.content.items():
            notation = ' '.join(attributes['notation'])

            formatted_lines.append(
                f'{tuning_id.ljust(14)}'
                f'{notation.ljust(24)}'
                f'{attributes["description"]}'
            )

        return '\n'.join(formatted_lines)
