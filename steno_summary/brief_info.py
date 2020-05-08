#!/usr/bin/env python3
from typing import List, Optional, Set
from steno_summary import letters
from functools import cached_property
import shutil

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
"""

letter_dict = letters.__dict__

left_hand = frozenset(["S", "T", "K", "P", "W", "H", "R", "A", "O"])
right_hand = frozenset(["E", "U", "F", "R", "P", "B", "L", "G", "T", "S", "D", "Z"])


class Brief:
    """ Key stroke summary for a word.

    This allows us to not only display the briefs is a more visual format, but also store
    them in a more intuitive manner. For instance:

        - NOE -> THPOE gives 'now'
        - BACh -> PWAFP gives 'batch'

    A basic shortened summary consists of letter chunks, a capital letter followed by
    optional lower cases letters. Each of these chunks corresponds to a unique sound and
    key series.

    Steno Order
    -----------

    We first attempt to place the stroke on the left hand side of the keyboard; if this is
    not possible, because the chunk does not exist on that side (eg Nk) or the keys are
    already in use by another stroke then we will attempt to place on the right of the
    keyboard and stop adding future briefs to the left hand side.

    The chunks will mostly be naturally assigned to the correct hand, but in ambigous
    cases, "-" may be used to clarify. For instance, a chunk Z may be the single letter
    "-Z" or the shorthand "S*" on the left. We therefore give the right hand command as
    "-Z".
    """

    def __init__(self, name: str, keys: str, tags: Optional[List] = None):
        self.name = name
        self.left_valid = True
        self.keys = keys
        self.left_letters: Set[str] = set()
        self.right_letters: Set[str] = set()
        self.tags = tags if tags is not None else []
        self.starred = False
        self.next_ = None

        letter_list = letters.split_on_capital(keys)
        for num, l in enumerate(letter_list):
            if l.lower() in letter_dict:
                steno_key = letter_dict[l.lower()]
                self._parse_key_stroke(steno_key)
            elif l in ["-", "*"]:
                self._parse_key_stroke(l)
            elif l == "/":
                formatted_keys = "".join(letter_list[num + 1 :])
                self.keys = "".join(letter_list[:num])
                self.next_ = Brief("", formatted_keys)
                break
            else:
                raise ValueError(f"Cannot parse letter {l} is it in letter_dict?")

        # Flatten the next_ items into array
        self.next_items = []
        next_item = self.next_
        while next_item is not None:
            self.next_items.append(next_item)
            next_item = next_item.next_

    def __str__(self):
        return f"Brief: {self.name}\tStroke: {self.keys}"

    def __lt__(self, other):
        """ Sort on the name of Brief. """
        if not isinstance(other, Brief):
            raise NotImplementedError("Sorting not supported for non-Brief objects")
        # return self.name <= other.name
        return self.name <= other.name

    def __len__(self):
        """ Return the number of strokes required for the brief """
        return len(self.next_items) + 1

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
        if key == "*":
            self.starred = True
            return None

        # Attempt to fit on the left then right of the keyboard
        if not (self.fit_on_left(key) or self.fit_on_right(key)):
            raise ValueError(f"Unable to place keystroke - {key}")

    def fit_on_left(self, key: letters.Letter) -> bool:
        """ Attempt to fit the key onto the left hand side of the keyboard.

        If the ``self.left_valid`` flag has been disabled then this will automatically
        fail. Typically this is caused after we add a key to the right hand side.
        """

        # Remove control chars
        # TODO: Will have to deal with letters that have - in them

        # Deal with blank cases
        if not self.left_valid or not key.left:
            return False

        # Remove command chars
        starred = "*" in key.left
        formatted_keys = set(filter(lambda l: l not in ["*", "-"], key.left))

        if formatted_keys <= self.remaining_left:
            # If we are unable to place it in the left we disable it (steno order)
            self.left_letters |= formatted_keys
            if starred:
                self.starred = True
            return True
        return False

    def fit_on_right(self, key) -> bool:
        """ Attempt to fit the key onto the right hand side of the keyboard. """

        # Remove control chars
        # TODO: Will have to deal with letters that have - in them

        # Deal with blank cases
        if not key.right:
            return False

        # Remove command chars
        starred = "*" in key.right
        formatted_keys = set(filter(lambda l: l not in ["*", "-"], key.right))

        if formatted_keys <= self.remaining_right:
            # If we are unable to place it in the left we disable it (steno order)
            self.left_valid = False
            self.right_letters |= formatted_keys
            if starred:
                self.starred = True
            return True
        return False

    @cached_property
    def block(self):
        """ Print out the array while showing the structure of the keyboard. """
        # empty = "□"
        # full = "■"
        # null = "▢"
        empty = "▧"
        null = " "

        left_fmt = {"*": "*" if self.starred else null}
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
        right_bot = f"{right_fmt['E']} {right_fmt['U']}      "

        merge_block = (
            f"{left_top} {right_top}\n"
            f"{left_mid} {right_mid}\n"
            f"{left_bot}   {right_bot}"
        )
        block = f"{self.name:^21}\n" + f"{self.keys:^21}\n" + merge_block
        return block

    def print_block(self):
        print(self.block)


def brief_grid(briefs: List[Brief], width: Optional[int] = None):
    """ Print the briefs in a grid """
    # Calculate the number of strokes we can fit per line
    grid_width = width if width is not None else _get_term_width()
    grid_gap = "  │  "
    block_len = 21 + len(grid_gap)
    blocks_per_line = grid_width // block_len

    # We have to write the lines conncurrently
    lines = ["" for i in range(6)]
    row = ""
    current_pos = 0

    for brief in briefs:
        # Reset the current line if there will be an overflow
        stroke_len = len(brief)
        if stroke_len > blocks_per_line:
            # TODO: Currently we cannot deal with strokes longer than the grid
            continue
        current_pos += stroke_len
        if current_pos > blocks_per_line:
            row += "\n".join(lines)
            row += "\n"
            lines = ["" for i in lines]
            current_pos = stroke_len

        # Add the new block alongside the previous entry
        _append_block(brief, lines, grid_gap)
        for next_word in brief.next_items:
            _append_block(next_word, lines, grid_gap)

    # Process any remaning rows
    if lines[0]:
        row += "\n".join(lines)

    return row


def _append_block(brief: Brief, lines: str, grid_gap: str):
    """ Add the new entry in the cell to the left of the current entry. """
    boundary = "     " if brief.next_items else grid_gap
    strings = brief.block.split("\n")
    for i in range(5):
        lines[i] += strings[i] + boundary

    # Draw the row boundary
    lines[5] += " " * 21 + boundary


def _get_term_width() -> int:
    """ Number of columns in the terminal. """
    return shutil.get_terminal_size().columns


if __name__ == "__main__":
    pass
