#!/usr/bin/env python3
from typing import Set, Iterator, Optional, List
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

re_capital_split = re.compile(r"[A-Z\-\*/][^A-Z\-\*/]*")


class Letter:
    left_hand_keys = frozenset(["S", "T", "K", "P", "W", "H", "R", "A", "O"])
    right_hand_keys = frozenset(
        ["E", "U", "F", "R", "P", "B", "L", "G", "T", "S", "D", "Z"]
    )
    cmd_chars = frozenset(["*"])

    def __init__(self, left=None, right=None, both=False):
        """Add the stroke for the letter on the left and right hand side of the keyboard.

        By default, these are taken to be separate events: for instance, "F" may by given
        by either "TP" or "-F".

        However when the ``Both`` flag is used, the sides must be struct together,
        as is seen in the case of vowels: for instance the vowel sound "aw" is struck as
        "AU".

        """
        if left is None and right is None:
            raise ValueError("Either left or right hand size must be provided")
        self.left = self._validate_left(left)
        self.right = self._validate_right(right)
        self.both = both

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


class DualSideLetter(Letter):
    """Some letters, mostly long vowels, require that we stroke on both sides of the
    keyboard.
    """


def split_on_capital(string: str) -> List[str]:
    """Break a string into lists starting starting with a single captial letter and then
    zero or more lower case letters.

    This will ignore any lowercase letters at the start of the match as these aren't part
    of the expected behaivour, so an Error is raised in this case.

    Here is a misspelled word
    """
    if not string:
        return string
    first = string[0]
    if first.lower() == first and first not in ["-"]:
        raise ValueError(f"Split string should start with capital - {string}")
    return re_capital_split.findall(string)


a = Letter(left="A")
b = Letter(left="PW", right="B")
d = Letter(left="TK", right="D")
e = Letter(right="E")
f = Letter(left="TP", right="F")
g = Letter(left="TPKW", right="G")
h = Letter(left="H")
i = Letter(right="EU")
j = Letter(left="SKWR", right="PLBG")
k = Letter(left="K", right="BG")
l = Letter(left="HR", right="L")
m = Letter(left="PH", right="PL")
n = Letter(left="TPH", right="PB")
o = Letter(left="O")
p = Letter(left="P", right="P")
q = Letter(left="KW")
r = Letter(left="R", right="R")
s = Letter(right="S", left="S")
t = Letter(right="T", left="T")
u = Letter(right="U")
v = Letter(left="SR", right="*F")
w = Letter(left="W")
y = Letter(left="KWR")
x = Letter(right="BGS")
z = Letter(left="S*", right="Z")

ch = Letter(left="KH", right="FP")
th = Letter(left="TH", right="*T")
ng = Letter(right="PBG")
nk = Letter(right="*PBG")
mp = Letter(right="*PL")
# mp = Letter(right="FRP")
oo = Letter(left="AO")
sh = Letter(left="SH", right="RB")
shs = Letter(right="RBS")

aw = Letter(left="A", right="U", both=True)
ea = Letter(left="A", right="E", both=True)
aa = Letter(left="A", right="EU", both=True)
ow = Letter(left="O", right="U", both=True)
oi = Letter(left="O", right="EU", both=True)
ee = Letter(left="AO", right="E", both=True)
uu = Letter(left="AO", right="U", both=True)
ii = Letter(left="AO", right="EU", both=True)

com = Letter(left="K")
con = Letter(left="K")
kshun = Letter(right="BGS")
ment = Letter(right="PLT")
nch = Letter(right="FRPB")
rch = Letter(right="FRPB")
rve = Letter(right="FRB")
shun = Letter(right="GS")
ent = Letter(left="SPW")
ds = Letter(left="STK")
