#!/usr/bin/env python3
from typing import Set, Iterator, Optional

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


class Letter:
    left_hand_keys = frozenset(["S", "T", "K", "P", "W", "H", "R", "A", "O"])
    right_hand_keys = frozenset(
        ["*", "E", "U", "F", "R", "P", "B", "L", "G", "T", "S", "D", "Z"]
    )

    def __init__(self, left=None, right=None):
        if left is None and right is None:
            raise ValueError("Either left or right hand size must be provided")
        self.left = self._validate_left(left)
        self.right = self._validate_right(right)

    def _validate_left(self, letters: Optional[str]) -> Set[str]:
        """ Ensure that given keys are in the left hand side of the keyboard. """
        if not letters:
            return set()
        letters_upper = [l.upper() for l in letters]
        invalid = [l for l in letters_upper if l not in self.left_hand_keys]
        if invalid:
            raise ValueError(f"{invalid} keys not on left hand side of keyboard")
        return set(letters_upper)

    def _validate_right(self, letters: Optional[str]) -> Set[str]:
        """ Ensure that given keys are in the right hand side of the keyboard. """
        if not letters:
            return set()
        letters_upper = [l.upper() for l in letters]
        invalid = [l for l in letters_upper if l not in self.right_hand_keys]
        if invalid:
            raise ValueError(f"{invalid} keys not on right hand side of keyboard")
        return set(letters_upper)

    def __str__(self):
        return "".join(self.left) + "".join(self.right)


# TODO: Add both key for the vals, either keep them accented or use lower case keys
# TODO: Extend the letter list
a = Letter(left="A")
b = Letter(left="HR", right="B")
d = Letter(left="TK", right="D")
e = Letter(right="E")
f = Letter(left="TP", right="F")
g = Letter(left="TPKW", right="G")
i = Letter(right="EU")
h = Letter(left="H")
j = Letter(left="SKWR")
k = Letter(left="K", right="BG")
l = Letter(left="HR", right="L")
m = Letter(left="PH", right="PL")
n = Letter(left="TPH", right="PB")
o = Letter(left="O")
p = Letter(left="P", right="P")
r = Letter(left="R", right="R")
s = Letter(right="S", left="S")
t = Letter(right="T", left="T")
u = Letter(right="U")
v = Letter(left="SR", right="*F")
w = Letter(left="W")
y = Letter(left="KWR")
z = Letter(right="Z")
