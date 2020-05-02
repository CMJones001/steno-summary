#!/usr/bin/env python3
from typing import List, Optional, Set
from steno_summary import letters

""" The Brief object holds and displays the keystrokes for a brief.

Outline
-------

This is plan to store briefs in a more visual format, which will in the future
allow for searching and filtering. We have made a particular choice to record a
shorthand notation with the brief, for instance, the key for "family" is stroked
as TPAEPL however the breif can be shorted handed to FAM

The object has two stores, one for each hand, first we attempt to place the
letter on the left hand side before moving onto the right. Once we have placed
something in the right hand column we disable the left hand store in order to
emulate the steno order.

Plans
-----

TODO: Steno order: This doesn't really respect the steno order too well, we
      should address this better. Mostly this effects the cannonical outup and
      occassionally requires an additional "-" in the brief description. Might
      be enough to sort the hands separately?

TODO: Tags: We have added some basic support for tags that can be used to filter
      results, for instance to only include the punctuation. This may be made as
      an enum?

TODO: Add command line argument for adding and searching breifs.

TODO: Multistroke commands

TODO: Allow lowercase letters to disamibiguate groups?

"""

letter_dict = letters.__dict__

left_hand = frozenset(["S", "T", "K", "P", "W", "H", "R", "A", "O"])
right_hand = frozenset(["E", "U", "F", "R", "P", "B", "L", "G", "T", "S", "D", "Z"])


class Brief:
    def __init__(self, name: str, keys: str, tags: Optional[List] = None):
        self.name = name
        self.left_valid = True
        self.keys = keys
        self.left_letters: Set[str] = set()
        self.right_letters: Set[str] = set()
        self.tags = tags if tags is not None else []

        for l in keys:
            l = l.lower()
            if l in letter_dict:
                steno_key = letter_dict[l.lower()]
                self._parse_key_stroke(steno_key)
            elif l == "-":
                self._parse_key_stroke(l)
            else:
                raise ValueError(f"Cannot parse letter {l} is it in letter_dict?")

    def __str__(self):
        return f"Brief: {self.name}\tStroke: {self.keys}"

    def __lt__(self, other):
        """ Sort on the name of Brief. """
        if not isinstance(other, Brief):
            raise NotImplementedError("Sorting not supported for non-Brief objects")
        return self.name <= other.name

    @property
    def cannonical(self):
        """ The key squence without abreviations. """
        return "".join(self.left_letters | self.right_letters)

    @property
    def remaining_left(self):
        """" Letters that are not used on the left hand side. """
        return left_hand - set(self.left_letters)

    @property
    def remaining_right(self):
        """" Letters that are not used on the right hand side. """
        return right_hand - set(self.right_letters)

    @property
    def short(self):
        """ Minimal form, used for parsing with external programs (colums). """
        return f"{self.name}_{self.keys}"

    @property
    def tsv(self):
        """ Tab separated values to save into dictionary. """
        return f"{self.name}\t{self.keys}\t{self.cannonical}\n"

    def _parse_key_stroke(self, key):
        """ Attempt to add a letter to the letter store """
        # Dash is not key stroke but shows that we should move side
        if key == "-":
            self.left_valid = False
            return None

        if self.left_valid and key.left and key.left <= self.remaining_left:
            # Attempt to add to left hand side
            self.left_letters |= key.left
        elif key.right and key.right <= self.remaining_right:
            # If we are unable to place it in the left we disable it (steno order)
            self.left_valid = False
            self.right_letters |= key.right
        else:
            raise ValueError(f"Unable to place keystroke - {key}")

    def print_block(self):
        """ Print out the array while showing the structure of the keyboard. """
        # empty = "□"
        # full = "■"
        # null = "▢"
        empty = "▧"
        null = " "

        left_fmt = {"*": null}
        for key in left_hand:
            left_fmt[key] = key if key in self.left_letters else empty

        right_fmt = {"*": null}
        for key in right_hand:
            right_fmt[key] = key if key in self.right_letters else empty

        left_top = " ".join(left_fmt[k] for k in "STPH*")
        left_mid = " ".join(left_fmt[k] for k in "SKWR*")
        left_bot = f"{' '*4}{left_fmt['A']} {left_fmt['O']}  "

        right_top = " ".join(right_fmt[k] for k in "*FPLTD")
        right_mid = " ".join(right_fmt[k] for k in "*RBGSZ")
        right_bot = f"{right_fmt['E']} {right_fmt['U']} "

        merge_block = (
            f"{left_top} {right_top}\n"
            f"{left_mid} {right_mid}\n"
            f"{left_bot}   {right_bot}"
        )
        print(f"{self.name:^21}")
        print(f"{self.keys:^21}")
        print(merge_block)
        print()


if __name__ == "__main__":
    pass
