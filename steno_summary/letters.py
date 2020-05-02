#!/usr/bin/env python3
from typing import Set, Iterator, Optional
import re

""" Database for each letter.

Outline
-------

Store the strokes for each short hand object:

Notes
-----

We don't quite get the steno order right, we might correct for this by using
ordered sets, while overriding the sorting method, for introduction:
https://stackoverflow.com/questions/1653970/does-python-have-an-ordered-set

"""

re_capital_split = re.compile("[A-Z][^A-Z]*")


class Letter:
    left_hand_keys = frozenset(["S", "T", "K", "P", "W", "H", "R", "A", "O"])
    right_hand_keys = frozenset(
        ["E", "U", "F", "R", "P", "B", "L", "G", "T", "S", "D", "Z"]
    )
    cmd_chars = frozenset(["*"])

    def __init__(self, left=None, right=None):
        if left is None and right is None:
            raise ValueError("Either left or right hand size must be provided")
        self.left = self._validate_left(left)
        self.right = self._validate_right(right)

    def _validate_left(self, letters: Optional[str]) -> Set[str]:
        """ Ensure that given keys are in the left hand side of the keyboard. """

        # Pass empty set through without furher processing
        if not letters:
            return set()

        # Ensure that the provided letters are on the left side of the  keyboard
        # or are cmd characters
        letters_upper = [l.upper() for l in letters]
        invalid = [
            l for l in letters_upper if l not in self.left_hand_keys | self.cmd_chars
        ]
        if invalid:
            raise ValueError(f"{invalid} keys not on left hand side of keyboard")
        return set(letters_upper)

    def _validate_right(self, letters: Optional[str]) -> Set[str]:
        """ Ensure that given keys are in the right hand side of the keyboard. """
        if not letters:
            return set()
        letters_upper = [l.upper() for l in letters]
        invalid = [
            l for l in letters_upper if l not in self.right_hand_keys | self.cmd_chars
        ]
        if invalid:
            raise ValueError(f"{invalid} keys not on right hand side of keyboard")
        return set(letters_upper)

    def __str__(self):
        return "".join(self.left) + "".join(self.right)


def split_on_capital(string: str) -> Iterator[str]:
    """ Break a string into lists starting starting with a single captial letter and then
    zero or more lower case letters.

    This will ignore any lowercase letters at the start of the match as these aren't part
    of the expected behaivour, so an Error is raised in this case.
    """
    if string[0].lower() == string[0]:
        raise ValueError(f"Split string should start with capital - {string}")
    return re_capital_split.findall(string)


# TODO: Add both key for the vals, either keep them accented or use lower case keys
# TODO: Extend the letter list
a = Letter(left="A")
b = Letter(left="HR", right="B")
# c =
d = Letter(left="TK", right="D")
e = Letter(right="E")
f = Letter(left="TP", right="F")
g = Letter(left="TPKW", right="G")
h = Letter(left="H")
i = Letter(right="EU")
j = Letter(left="SKWR")
k = Letter(left="K", right="BG")
l = Letter(left="HR", right="L")
m = Letter(left="PH", right="PL")
n = Letter(left="TPH", right="PB")
o = Letter(left="O")
p = Letter(left="P", right="P")
# q
r = Letter(left="R", right="R")
s = Letter(right="S", left="S")
t = Letter(right="T", left="T")
u = Letter(right="U")
v = Letter(left="SR", right="*F")
w = Letter(left="W")
y = Letter(left="KWR")
z = Letter(left="S*", right="Z")
